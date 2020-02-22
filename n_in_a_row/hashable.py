import hashlib
from struct import pack

from config import load_config


class Hashable:

    def build_hash(self, hash_obj) -> None:
        raise NotImplementedError()  # don't use ABCMeta metaclass

    def __hash__(self) -> int:
        config = load_config()
        hash_obj = hashlib.new(config['hash_algorithm'])
        self.build_hash(hash_obj)
        return int.from_bytes(hash_obj.digest(), byteorder='big')


def pack_ints(*integers):
    return pack('!' + 'I' * len(integers), *integers)
