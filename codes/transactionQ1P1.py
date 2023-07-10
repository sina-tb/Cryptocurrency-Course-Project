import bitcoin.wallet
from utils import *

# 0.01450576
# txid = efb8aefbe2f195bbcea6c8a049d1cb127e1d73962d4f938e970b2ff541bfc5b4
# msuv6EVFEZyA8N49EGYuxRbiATFpBvWqxQ
# 91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb

bitcoin.SelectParams("testnet") ## Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("91wCkGpbGK42f3RXVUJ4utnewk3SoPnMDUq7JJPjXgZr6QA3MHb") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, first_txout, second_txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature_two_outputs(txin, first_txout, second_txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def make_transaction(first_amount_to_spend, second_amount_to_spend, txid_to_spend, utxo_index,first_txout_scriptPubKey, second_txout_scriptPubKey):

    first_txout = create_txout(first_amount_to_spend, first_txout_scriptPubKey)
    second_txout = create_txout(second_amount_to_spend, second_txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey()

    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = P2PKH_scriptSig(txin, first_txout, second_txout, txin_scriptPubKey)

    new_tx = create_signed_transaction_two_outputs(txin, first_txout, second_txout, txin_scriptPubKey,txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    # 0.01450576
    first_amount_to_spend = 0.000001
    second_amount_to_spend = 0.013
    txid_to_spend = ('efb8aefbe2f195bbcea6c8a049d1cb127e1d73962d4f938e970b2ff541bfc5b4') # TxHash of UTXO
    utxo_index = 0

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex

    first_txout_scriptPubKey = [OP_RETURN]
    second_txout_scriptPubKey = [OP_1]
    response = make_transaction(first_amount_to_spend, second_amount_to_spend, txid_to_spend, utxo_index, first_txout_scriptPubKey, second_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

    # result = 9bcfda8a676eaffd3859d1990d983b552e22b49c454560648ddf8d91ceee239e