import bitcoin.wallet
from utils import *


# 0.0128
# txid = c9420f311b98fec5e98adee5c7e38954500629ea263a031e5142ca1170440f40
# msuv6EVFEZyA8N49EGYuxRbiATFpBvWqxQ
# 91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb

bitcoin.SelectParams("testnet")

my_private_key = bitcoin.wallet.CBitcoinSecret("91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb")
first_private_key = bitcoin.wallet.CBitcoinSecret("92UN41zMS2NiGy6gMaGER5iq5fwthC2uVY64eNAtmARCpDiyoMA")
second_private_key = bitcoin.wallet.CBitcoinSecret("929D9AU2Vh8msPzdwtYEwo1c9LD8tgz7o8uo6Uq1HAstWsvwDec")
third_private_key = bitcoin.wallet.CBitcoinSecret("91fuVHjXcY8kmXoao97BPVvCrLZMpcvy8MaXfGgKJgX4KjiuVtH")

my_public_key = my_private_key.pub
first_person_public_key = first_private_key.pub
second_person_public_key = second_private_key.pub
third_person_public_key = third_private_key.pub

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index,txout_scriptPubKey):

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_txin_scriptPubKey()

    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    # 0.0128
    amount_to_send = 0.0124
    txid_to_spend = ('c9420f311b98fec5e98adee5c7e38954500629ea263a031e5142ca1170440f40')
    utxo_index = 0

    txout_scriptPubKey = [OP_2, first_person_public_key, second_person_public_key, third_person_public_key, OP_3, OP_CHECKMULTISIG]
    response = make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

    # result = '6863e1ba33f20e3dcb8286dc09999ca019e64595645768826c6f3424d212877e'