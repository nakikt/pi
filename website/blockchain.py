import hashlib
import json
from time import time
import requests
from urllib.parse import urlparse
from datetime import datetime
import sys
PORT = sys.argv[1]

class Blockchain(object):
    difficulty_target = "0000"
    def hash_block(self, block):
# encode the block into bytes and then hashes it;
        block_encoded = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()
    def __init__(self):
        self.nodes = set()
# stores all the blocks in the entire blockchain
        self.chain = []
# temporarily stores the health card for the current block
        self.current_health_card = []
# create the genesis block with a specific fixed hash of previous block genesis block starts with index 0
        genesis_hash = self.hash_block("genesis_block")
        self.append_block(
            hash_of_previous_block=genesis_hash,
            nonce=self.proof_of_work(0, genesis_hash, [])
           )
# use PoW to find the nonce for the current block
    def proof_of_work(self, index, hash_of_previous_block, health_cards):
# try with nonce = 0
        nonce = 0
# try hashing the nonce together with the hash of the previous block until it is valid
        while self.valid_proof(index, hash_of_previous_block, health_cards, nonce) is False:
            nonce += 1

        return nonce
# check if the block's hash meets the difficulty target
    def valid_proof(self, index, hash_of_previous_block, health_cards, nonce):
# create a string containing the hash of the previous block and the block content, including the nonce
        content = f'{index}{hash_of_previous_block}{health_cards}{nonce}'.encode()
# hash using sha256
        content_hash = hashlib.sha256(content).hexdigest()
# check if the hash meets the difficulty target
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target
# creates a new block and adds it to the blockchain
    def append_block(self, nonce, hash_of_previous_block):
        block = {
            'index': len(self.chain),
            'timestamp': str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')),
            'health_card': self.current_health_card,
            'nonce': nonce,
            'hash_of_previous_block': hash_of_previous_block
            }
# reset the current list of the health_card attributes
        self.current_health_card = []
        # add the new block to the blockchain
        self.chain.append(block)
        return block
    def add_health_card (self, id, name_surname, birth_date, diseases, vaccinations):
# adds a new health_card to the current list of health_cards
        self.current_health_card.append({
            'id': id,
            'name_surname': name_surname,
            'birth_date': birth_date,
            'diseases': diseases,
            'vaccinations': vaccinations,
            })
# get the index of the last block in the blockchain and add one to it this will be the block that the current health_card will be added to
        return self.last_block['index'] + 1
    @property
    def last_block(self):
    # returns the last block in the blockchain
        return self.chain[-1]
# --------------------
# add a new node to the list of nodes e.g.

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        # print(parsed_url.netloc)
# determine if a given blockchain is valid
    def valid_chain(self, chain):
        last_block = chain[0] # the genesis block
        current_index = 1 # starts with the second block
        while current_index < len(chain):
# get the current block
            block = chain[current_index]
# check that the hash of the previous block is
# correct by hashing the previous block and then
# comparing it with the one recorded in thelast_b
# current block
            if block['hash_of_previous_block'] != self.hash_block(last_block):

                return False
# check that the nonce is correct by hashing the
# hash of the previous block together with the
# nonce and see if it matches the target
            if not self.valid_proof(current_index, block['hash_of_previous_block'],block['health_card'],block['nonce']):
                return False
# move on to the next block on the chain
            last_block = block
            current_index += 1
# the chain is valid
        return True


    def update_blockchain(self, id):
        # get the nodes around us that has been registered
        try:
            neighbours = self.nodes
            new_chain = None
            # for simplicity, look for chains longer than ours
            max_length = len(self.chain)
            # grab and verify the chains from all the nodes in
            # our network

            for node in neighbours:
                # get the blockchain from the other nodes
                response = requests.get(f'http://{node}//blockchain/{id}')
                # check if the length is longer and the chain
                # is valid

                if response.status_code == 200:

                    length = response.json()['length']
                    chain = response.json()['chain']

                if length > max_length:
                    max_length = length
                    new_chain = chain

            # replace
            if new_chain is not None:
                self.chain = new_chain
                return True
            return True
        except:
            return False

    def initial_sync(self, id):


        node = f'http://127.0.0.1:5000'
                # get the blockchain from the other nodes
        response = requests.get(f'{node}/blockchain/{id}')
                # check if the length is longer and the chain
                # is valid

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']
            self.chain = chain
            return True

        return False
    def valid_new(self,id):
        # get the nodes around us that has been registered
        neighbours = self.nodes
        # for simplicity, look for chains longer than ours

        # grab and verify the chains from all the nodes in
        # our network
        chain_to_check = self.chain
        number_of_nodes = len(neighbours)
        x = 0
        for node in neighbours:
            # get the blockchain from the other nodes
            response = requests.get(f'http://{node}//blockchain/{id}')
            # check if the length is longer and the chain
            # is valid

            if response.status_code == 200:
                chain = response.json()['chain']
                if chain_to_check == chain:
                    x+=1
                if x > (number_of_nodes/2):
                    return True
        return False

