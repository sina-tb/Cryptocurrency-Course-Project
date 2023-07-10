import secrets
import hashlib
import base58
import ecdsa


def checksum(key):
    return hashlib.sha256(hashlib.sha256(key).digest()).digest()[0:4]

def wif_maker(private_key):
    extended = b"\xef" + bytes.fromhex(private_key)
    return base58.b58encode(extended + checksum(extended)).decode('utf-8')

def public_key_generator(private_key):
    private_key_bytes = bytes.fromhex(private_key)
    public_key_bytes = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    return public_key_bytes.to_string().hex()

def ripemd_hash(sha256_1):
    ripemd = hashlib.new('ripemd160')
    ripemd.update(sha256_1)
    ripemd_key = ripemd.hexdigest()
    return b"\x6f".hex() + ripemd_key

def public_key_compressed(random_private_key):
    public_key_compressed = '04' + public_key_generator(random_private_key)
    public_key_compressed_bytes = bytes.fromhex(public_key_compressed)
    return public_key_compressed_bytes
def address_generator(random_private_key):

    public_key_compressed_bytes = public_key_compressed((random_private_key))

    sha256_1 = hashlib.sha256(public_key_compressed_bytes).digest()

    rip_key_extended = ripemd_hash(sha256_1)

    address = bytes.fromhex(rip_key_extended) + checksum(bytes.fromhex(rip_key_extended))

    final_base58 = base58.b58encode(address).decode('utf-8')

    return final_base58

def generate_vanity_address(chars):
    while True:
        private_key = secrets.token_hex(32)
        address = address_generator(private_key)
        if address[1:4] == chars:
            print('vanity private key:' + private_key)
            return address

if __name__ == '__main__':
    chars = input()
    private = secrets.token_hex(32)
    print("Vanity Address: ", generate_vanity_address(chars))
