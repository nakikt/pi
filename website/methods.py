#This class helps with creating names for new blockchains
class New_blockchains:
  def __init__(self, name):
    self.name = name

def mine_block(blockchain, id, name_surname, birth_date, diseases, vaccinations):
    blockchain.add_health_card(
        id =  id,
        name_surname = name_surname,
        birth_date = birth_date,
        diseases = diseases,
        vaccinations = vaccinations,
    )
# obtain the hash of last block in the blockchain
    last_block_hash = blockchain.hash_block(blockchain.last_block)
# using PoW, get the nonce for the new block to be added to the blockchain
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_health_card)
# add the new block to the blockchain using the last block hash and the current nonce
    blockchain.append_block(nonce, last_block_hash)





