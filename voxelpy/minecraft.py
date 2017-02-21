import zlib
import struct
import numpy as np

BYTES_CHUNK = 4096

def load_region(path):
    chunks = {}
    with open(path, mode='rb') as file:
        fileContent = file.read(BYTES_CHUNK)
        chunk_entries = {}
        for i in range(1024):
            cur_index = 4*i
            offset = bytes_to_int(fileContent, cur_index, 3)
            chunk_count = int.from_bytes([fileContent[cur_index + 3]], 'big')
            chunk_entries[offset] = (chunk_count, i)
        file.read(BYTES_CHUNK)  # Dump timestamps
        chunkoffset = 2
        cont = file.read(BYTES_CHUNK)

        while cont != "" and chunkoffset <= max(chunk_entries.keys()):
            if chunkoffset in chunk_entries:
                chunk_count = chunk_entries[chunkoffset]
            else:
                cont = file.read(BYTES_CHUNK)
                chunkoffset += 1
                continue
            chunk_size = bytes_to_int(cont, 0, 4)

            index = 5
            compressed = b''
            while chunk_size > 0:
                compressed += cont[index:index + chunk_size]
                cont = file.read(BYTES_CHUNK)
                chunk_size -= BYTES_CHUNK - index
                index = 0
                chunkoffset += 1

            chunk = zlib.decompress(compressed)
            chunks[chunk_count[1]] = chunk

    npchunks = {}
    print('Parsing and storing blocks from NBT data')
    print('This will take some time')
    for chunk in chunks.values():
        nbt_tag = parse_NBT(chunk)
        lvl = nbt_tag['Level']
        chunkx = lvl['xPos']
        chunkz = lvl['zPos']
        sections = lvl['Sections']
        npchunk = np.zeros((16, 256, 16), dtype='b')
        for section in sections:
            blocks = section['Blocks']
            chunky = section['Y']
            for y in range(16):
                for z in range(16):
                    for x in range(16):
                        blockpos = 256 * y + 16 * z + x
                        blockId = blocks[blockpos]
                        npchunk[x][y + 16 * chunky][z] = blockId
            npchunks[(chunkx, chunkz)] = npchunk
    return npchunks


def parse_NBT(bytes):
    return parse_NBT_tag(bytes[3:])[0]

# Returns a dictionary and index offset
def parse_NBT_tag(bytes):
    tag = {}
    index = 0
    while index < len(bytes):
        tagtype = bytes_to_int(bytes, index, 1)
        if tagtype == 0:
            return tag, index + 1  # TODO: Check the + 1
        str_len = bytes_to_int(bytes, index + 1, 2)
        tag_name = bytes[index + 3:index + 3 + str_len].decode('utf-8')
        index += 3 + str_len

        if tagtype == 9:
            list_type = bytes_to_int(bytes, index, 1)
            list_len = bytes_to_int(bytes, index + 1, 4)
            index += 5
            tag_list = [0] * list_len
            for i in range(list_len):
                payload, offset = parse_NBT_type(list_type, bytes, index)
                tag_list[i] = payload
                index += offset
            tag[tag_name] = tag_list
        else:
            payload, offset = parse_NBT_type(tagtype, bytes, index)
            tag[tag_name] = payload
            index += offset
    return tag, index


def parse_NBT_type(tagtype, bytes, index):
    if tagtype == 1:
        return bytes_to_int(bytes, index, 1, True), 1
    elif tagtype == 2:
        return bytes_to_int(bytes, index, 2, True), 2
    elif tagtype == 3:
        return bytes_to_int(bytes, index, 4, True), 4
    elif tagtype == 4:
        return bytes_to_int(bytes, index, 8, True), 8
    elif tagtype == 5:
        return struct.unpack('f', bytes[index:index + 4]), 4
    elif tagtype == 6:
        return struct.unpack('d', bytes[index:index + 8]), 8
    elif tagtype == 7:
        basize = bytes_to_int(bytes, index, 4)
        index += 4
        byte_array = [0] * basize
        for i in range(basize):
            byte_array[i] = bytes_to_int(bytes, index, 1, True)
            index += 1
        return byte_array, basize + 4
    elif tagtype == 8:
        strln = bytes_to_int(bytes, index, 2)
        index += 2
        return bytes[index:index+strln].decode('utf-8'), 2 + strln
    elif tagtype == 10:
        return parse_NBT_tag(bytes[index:])
    elif tagtype == 11:
        basize = bytes_to_int(bytes, index, 4)
        index += 4
        byte_array = [0] * basize
        for i in range(basize):
            byte_array[i] = bytes_to_int(bytes, index, 4, True)
            index += 4
        return byte_array, 4 * basize + 4


def bytes_to_int(bytes, index, length, signed=False):
    b = [bytes[i] for i in range(index, index + length)]
    return int.from_bytes(b, 'big', signed=signed)