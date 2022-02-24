import binascii
import re

from gems import Gem
from user import User


def process_file(filename: str):
    data = None
    with open(filename, "rb") as f:
        data = f.read()
    data = binascii.hexlify(data)
    if not data.startswith(b"41000000000000"):
        return False
    return data, extract_gems(data), extract_user_info(data)


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
        pattern += binascii.hexlify(int.to_bytes(65+i, byteorder="little", length=1))+b"(.{30})"
    found_data = re.search(pattern, data)
    index = found_data.start()-1272
    if not index > 0:
        return False
    user_data = data[index: index+370]
    print("User data loaded!")
    return User(user_data)


def main(filename: str):
    data, all_gems, user = process_file(filename)
    if not all_gems:
        print("Failed to load gems!")
    if not user:
        print("Failed to load user!")
    print(user.get_original_stats())
    user.set_echoes(4294967295)
    print(user.get_modified_stats())
    user.apply_changes(data, filename)


if __name__ == '__main__':
    main("userdata000x")
