import binascii
import re

from gems import Gem
from user import User


def process_user(filename: str):
    data = None
    with open(filename, "rb") as f:
        data = f.read()
    data = binascii.hexlify(data)
    if not data.startswith(b"41000000000000"):
        return False
    return data, extract_user_info(data)


def process_gems(filename: str):
    data = None
    with open(filename, "rb") as f:
        data = f.read()
    data = binascii.hexlify(data)
    if not data.startswith(b"41000000000000"):
        return False
    return data, extract_gems(data)


def extract_gems(data: bytes):
    all_gems = []
    gem_possibilities = [b"0100000001000000", b"0100000002000000", b"0100000004000000", b"0100000008000000",
                         b"010000003f000000", b"0200000001000000", b"0200000002000000", b"0200000004000000",
                         b"0200000008000000", b"020000003f000000"]
    total_gems = 0
    index = min([data.find(x, 0, 1000) - 16 for x in gem_possibilities if data.find(x, 0, 1000) - 16 > 0])
    while True:
        gem_data = data[index: index + 56]
        if any(x in gem_data for x in gem_possibilities):
            if gem_data[17] == 49:
                new_gem = Gem(gem_data)
                all_gems.append(new_gem)
                total_gems += 1
            index += 80
        else:
            break
    print("Total gems found: {}".format(total_gems))
    return all_gems


def extract_user_info(data: bytes):
    pattern = b""
    for i in range(25):
        pattern += binascii.hexlify(int.to_bytes(65 + i, byteorder="little", length=1)) + b"(.{30})"
    found_data = re.search(pattern, data)
    index = found_data.start() - 1272
    if not index > 0:
        return False
    user_data = data[index: index + 370]
    print("User data loaded!")
    return User(user_data)


# if __name__ == '__main__':
#     with open("./data.txt", "r") as f:
#         lines = f.read().splitlines()
#         print("{")
#         for line in lines:
#             line_list = line.split(",")
#             for i in range(int(len(line_list)/2)):
#                 print(
#                     "b'"
#                     + binascii.hexlify(int.to_bytes(int(line_list[i*2]), byteorder="little", length=4)).decode("utf-8")
#                     + "'"
#                     + ":\""
#                     + line_list[(i*2)+1]
#                     + "\","
#                 )
#         print("}")
