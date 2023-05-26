import secrets
import hashlib
import base58
import ecdsa

VERSION_BYTE_PRIVATE_KEY = b"\xef"
VERSION_BYTE_PUBLIC_KEY = b"\x6f"

def convert_private_to_WIF(private_key):
    extended = VERSION_BYTE_PRIVATE_KEY + bytes.fromhex(private_key)
    return base58.b58encode(extended + checksum(extended)).decode('utf-8')


def random_private_key_generator():
    return secrets.token_hex(32);

def generate_public_key_uncompressed(private_key):
    private_key_bytes = bytes.fromhex(private_key)
    public_key_bytes = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    return public_key_bytes.to_string().hex()

def checksum(key):
    return hashlib.sha256(hashlib.sha256(key).digest()).digest()[0:4]

def address_generator(random_private_key):
    public_key_uncompressed = '04' + generate_public_key_uncompressed(random_private_key)
    # print("uncompressed: " + public_key_uncompressed)
    public_key_compressed = compress_public_key(public_key_uncompressed)
    # print("compressed: " + public_key_compressed)

    public_key_compressed_bytes = bytes.fromhex(public_key_compressed)
    sha256_1 = hashlib.sha256(public_key_compressed_bytes).digest()
    # print("sha1: " + sha256_1.hex())
    rip = hashlib.new('ripemd160')
    rip.update(sha256_1)
    rip_key = rip.hexdigest()
    # print("rip: " + rip_key)
    rip_key_extended = VERSION_BYTE_PUBLIC_KEY.hex() + rip_key

    address = bytes.fromhex(rip_key_extended) + checksum(bytes.fromhex(rip_key_extended))

    return base58.b58encode(address).decode('utf-8')

def generate_vanity_address(chars):
    while True:
        private_key = random_private_key_generator()
        address = address_generator(private_key)
        if address[1:4] == chars:
            print('vanity private key:' + private_key)
            return address

def compress_public_key(public_key):
    if int.from_bytes(bytearray.fromhex(public_key[-2:]), 'big') % 2 == 0:
        prefix = '02'
    else:
        prefix = '03'

    return prefix + public_key[2:66]

if __name__ == '__main__':
    private = "2a172fe722c4f25c8b6acc95728428490bc0261c64c66fa25a78b9a9f104d698"
    ad = "mqNX1Esv3N3DDqnSBmg8yY95dWGXkjadE1"
    pr = "91uTJxaiPUvZ763ia9ikQNj6i6oHxDvfv93ksxe1egzdcUtRt3M"
    txid = "0905cf196d3f05c86140e890d7c9614d46347078ce82e8b4eb0f66435b673dd6"
    print("address: ",address_generator(private))
    print("WIF private: ",convert_private_to_WIF(private))
    # print()
    # print('vanity addr for sin: ' + generate_vanity_address('sin'))