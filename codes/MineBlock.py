import bitcoin.wallet
from bitcoin.core import b2lx
from utils import *
import time
import struct
from hashlib import sha256

bitcoin.SelectParams("mainnet")

private_key = "KxeN3BxxGstQhXSsdBzfv3WpfC58KnDSmAjpL6g4SJekBdo1eTwN"
my_private_key = bitcoin.wallet.CBitcoinSecret(private_key)
my_public_key = my_private_key.pub


def P2PKH_scriptPubKey(key):
    return [OP_DUP, OP_HASH160, Hash160(key), OP_EQUALVERIFY, OP_CHECKSIG]

def create_transaction():

    coinbase_data = '810199554SinaTabassi'.encode('utf-8').hex()
    block_reward = 6.25

    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txid_to_spend, index = (64*'0'), int('0xFFFFFFFF', 16)
    txin = create_txin(txid_to_spend, index)
    txout = create_txout(block_reward, txout_scriptPubKey)
    txin.scriptSig = CScript([int(coinbase_data, 16).to_bytes(len(coinbase_data)//2, 'big')])

    return CMutableTransaction([txin], [txout])

def target_calc(bits):

    target = int(bits[4:], 16) * (int('2', 16) ** (8 * (int(bits[2:4], 16) - 3)))
    target_hex = format(target, 'x')
    target_hex = str(target_hex).zfill(64)
    print("Target in hex: ", target_hex)
    return bytes.fromhex(target_hex)

def create_block(header, block_body):

    block_size = len(header) + len(b'\x01') + len(block_body)
    magic_number = 0xD9B4BEF9.to_bytes(4, "little")
    block = magic_number + struct.pack("<L", block_size) + header + b'\x01' + block_body
    return block

def print_block_inforamtion(nonce, hash, header, hash_rate, time_stamp, block, version, block_body, merkle_root):

    print("######################## Mining Successfully Done! #############################")
    print("Merkle root: ", merkle_root)
    print("Block body: ", block_body.hex())
    print("Block header:", header.hex())
    print("Block hash:", b2lx(hash))
    print("Hash rate:", hash_rate, "H/s")
    print("Block in hex:", b2x(block))
    print("Version:", version)
    print("Time stamp:", time_stamp)
    print("Nonce:", nonce)

def reverse(x):
    return x[::-1]
def header_maker(version, merkle_root, time_stamp, bits, prev_block_hash):
    return struct.pack("<L", version) + reverse(bytes.fromhex(prev_block_hash)) + reverse(
        bytes.fromhex(merkle_root)) + struct.pack('<LL', time_stamp, int(bits, 16))
def bitcoin_mining(prev_block_hash):

    version = 2
    bits = '0x1f010000'

    tx = create_transaction()
    block_body = tx.serialize()
    merkle_root = b2lx(sha256(sha256(block_body).digest()).digest())
    target = target_calc(bits)
    time_stamp = int(time.time())
    partial_header = header_maker(version, merkle_root, time_stamp, bits, prev_block_hash)
    nounce = 0

    start_time = time.time()
    while nounce <= 2**32:

        header = partial_header + struct.pack('<L', nounce)
        hash = sha256(sha256(header).digest()).digest()

        if reverse(hash) < target:

            block = create_block(header, block_body)
            hash_rate = nounce / (time.time() - start_time)
            print_block_inforamtion(nounce, hash, header, hash_rate, time_stamp,block,version,block_body,merkle_root)

            return
        nounce = nounce + 1


if __name__ == '__main__':
    
    # prev_block_hash = '0000000069106242b2224082ba60c7f4af8bb2d1d412f47d9e4c50e8aaf99fbe'
    # n = 9554
    number = input("enter the block number: ")
    prev_block_hash = input("enter pre block hash: ")
    bitcoin_mining(prev_block_hash)