from transactionQ2P1 import *

# 0.0124
# txid = 6863e1ba33f20e3dcb8286dc09999ca019e64595645768826c6f3424d212877e
# msuv6EVFEZyA8N49EGYuxRbiATFpBvWqxQ
# 91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub

def P2PKH_output_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):

    first_person_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, first_private_key)
    second_person_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, second_private_key)

    return [OP_0, first_person_signature, second_person_signature]

def make_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = [OP_2, first_person_public_key, second_person_public_key, third_person_public_key, OP_3, OP_CHECKMULTISIG]

    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    # 0.0124
    amount_to_send = 0.0120
    txid_to_spend = ('6863e1ba33f20e3dcb8286dc09999ca019e64595645768826c6f3424d212877e')
    utxo_index = 0
    txout_scriptPubKey = P2PKH_output_scriptPubKey()
    response = make_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

#transaction_hash: fb444f9092ea24dcb9ee48519dcaadfcfe8d7ac2b89a25032149d065919e9467