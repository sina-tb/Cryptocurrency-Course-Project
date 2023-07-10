import bitcoin.wallet

from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("0905cf196d3f05c86140e890d7c9614d46347078ce82e8b4eb0f66435b673dd6") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('mqNX1Esv3N3DDqnSBmg8yY95dWGXkjadE1') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)

    txin = create_txin(txid_to_spend, utxo_index)

    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.1
    txid_to_spend = ('0905cf196d3f05c86140e890d7c9614d46347078ce82e8b4eb0f66435b673dd6') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
