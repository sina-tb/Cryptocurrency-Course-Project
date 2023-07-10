import bitcoin.wallet
from utils import *

PRIME_NUM1 = 2909
PRIME_NUM2 = 249

# 0.0116
# txid = 8b9c71c4d0794e308fe24c3fa0610d1769051108946101b8c7acd8443adc389b
# msuv6EVFEZyA8N49EGYuxRbiATFpBvWqxQ
# 91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb

bitcoin.SelectParams("testnet")

my_private_key = bitcoin.wallet.CBitcoinSecret("91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb")
my_public_key = my_private_key.pub

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index):

    sub = PRIME_NUM1 - PRIME_NUM2
    add = PRIME_NUM1 + PRIME_NUM2

    txout_scriptPubKey = P2PKH_txin_scriptPubKey()

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = [OP_2DUP,
                        OP_SUB, OP_HASH160, Hash160(sub.to_bytes(2, byteorder="little")), OP_EQUALVERIFY,
                        OP_ADD, OP_HASH160, Hash160(add.to_bytes(2, byteorder="little")), OP_EQUAL]

    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = [PRIME_NUM1, PRIME_NUM2]

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    # 0.0116
    amount_to_send = 0.0112
    txid_to_spend = ('8b9c71c4d0794e308fe24c3fa0610d1769051108946101b8c7acd8443adc389b')
    utxo_index = 0

    response = make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index)
    print(response.status_code, response.reason)
    print(response.text)

    # result 54750f60bec7f093e9c6be9b4d398c62042b4830da498897d8d436319bcde627