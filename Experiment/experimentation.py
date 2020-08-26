# Creating a CryptoCurrency

#importng the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
#from uuid import uuid4
from urllib.parse import urlparse
import subprocess


#also required additional python module named as requests

#blockchain

class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.transactions = [] #list containing all the transactions before they are mined into a block, basically works as a mempool
        #self.Create_Block(proof = 1, previous_hash = '0', merkle_root='0')
        self.Create_Block(previous_hash = '0', merkle_root='0')
        self.nodes = set()
        
    #def Create_Block(self, proof, previous_hash, merkle_root):
    def Create_Block(self, previous_hash, merkle_root):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 #'proof' : proof, 
                 'previous_hash' : previous_hash,
                 'transactions' : self.transactions,
                 'merkle_root': merkle_root}
        self.transactions = []
        self.chain.append(block)
        self.consensus1(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # for the last block of the blockchain
    
    #def proof_of_work(self, previous_proof):
        #new_proof = 1
        #check_proof = False
        #while check_proof is False:
            #hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #if hash_operation[:4] == '0000':
                #check_proof = True
            #else:
                #new_proof += 1
        #return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def transaction_hash(self, transaction):
        encoded_transaction = json.dumps(transaction, sort_keys=True).encode()
        return hashlib.sha256(encoded_transaction).hexdigest()
    
    #def is_chain_valid(self, chain):
        #previous_block = chain[0]
        #block_index = 1
        #while block_index < len(chain):
            #block = chain[block_index]
            #if block['previous_hash'] != self.hash(previous_block):
                #return False
            #previous_proof = previous_block['proof']
            #proof = block['proof']
            #hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            #if hash_operation[:4] != '0000':
                #return False
            #previous_block = block
            #block_index = block_index + 1
        #return True
    
    def consensus1(self, block):
        hs = self.hash(block)
        print(hs)
        chaini = blockchain.chain
        chaini_len = len(chaini)
        out = subprocess.getoutput('python3 G:\MyProjects\Blockchain_for_user_auth\Experiment\client.py http://127.0.0.1:5000 {0} {1}'.format(chaini_len, hs))
        print(out)
        if 'success' in out:
            return True
        else :
            return False
        
    def consensus2(self, chaini_len):
        #hs = self.hash(block)
        #print(hs)
        out = subprocess.getoutput('python3 G:\MyProjects\Blockchain_for_user_auth\Experiment\client.py http://127.0.0.1:5000 {}'.format(chaini_len))
        print(out)
        if 'success' in out:
            return True
        else :
            return False
    
    
    def merkle_root(self):
        i=self.transactions
        for trans in i:
            new_mr = self.transaction_hash(trans)
        return new_mr
        
    
    def add_transaction(self, identity): #sender, receiver, message):
        #self.transactions.append({'sender' : sender,
         #                         'receiver' : receiver,
          #                        'message' : message})#format of our transactions
        identity = self.transaction_hash(identity) # getting hash of each transaction
        self.transactions.append({'identity' : identity})
        previous_block = self.get_previous_block() #get the index of the last block
        return previous_block['index'] + 1 #index of the block to which transactions will be added
    
    def add_node(self, address):
        parsed_url = urlparse(address) #function to parse the url of  the address node
        self.nodes.add(parsed_url.netloc) #basically gives the url of the node which can be used as its unique identity eg - '127.0.0.1:5000'
    
    def replace_chain(self):
        network = self.nodes #network of the nodes that are in our blockchain all the nodes
        longest_chain = None #it will contain our longest chain throughout the network which we will find out after iterating our network 
        max_length = len(self.chain) # it will contain the max length of the chain and will be initialized by the length of the current chain we are dealing with
        for node in network:
            response = requests.get(f'http://{node}/get_chain') #f here is the fstring functionformat which givver us whole http address of the node
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
                
            
        
    
# Mining a blockchain

#creating a flask based web app
app = Flask(__name__)

#creating an address for the node on Post 5000
#node_address = str(uuid4()).replace('-', '')
 #it is needed for getting mining fee from the block being mined as there will be a transaction from that block address to you

#creating a blockchain
blockchain = BlockChain()

#mining a blockchain
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    #previous_proof = previous_block['proof']
    #proof = blockchain.proof_of_work(previous_proof)
    cons = blockchain.consensus1(previous_block)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(sender = node_address, receiver = 'HARLEQUIN', message = "Hello!!" )
    blockchain.add_transaction(identity= "ID")
    merkle_root=blockchain.merkle_root()
    #block = blockchain.Create_Block(proof, previous_hash, merkle_root)
    block = blockchain.Create_Block(previous_hash, merkle_root)
    response = {'Message' : 'Congratulations, you just mined a block!', 
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                #'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions'],
                'merkle_root': block['merkle_root']}
    return jsonify(response), 200


# getting the full blockchain 
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain, 
                'length' : len(blockchain.chain)}
    return jsonify(response), 200


#checking the blockchain is valid

#@app.route('/is_valid', methods = ['GET'])

#def is_valid():
    #is_valid = blockchain.is_chain_valid(blockchain.chain)
    #if is_valid:
        #response = {'message' : 'All good. The blockchain is valid.'}
    #else:
        #response = {'message' : 'My man we got a problem, blockchain is not valid here.'}
    #return jsonify(response), 200
    
#checking the blockchain is valid

@app.route('/is_consensus', methods = ['GET'])

def is_consensus():
    chaini = blockchain.chain
    chaini_len = len(chaini)
    is_valid = blockchain.consensus2(chaini_len)
    if is_valid:
        response = {'message' : 'All good. The blockchain is valid.'}
    else:
        response = {'message' : 'My man we got a problem, blockchain is not valid here.'}
    return jsonify(response), 200
    

# Adding a new transaction to the Blockchain

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    #transaction_keys = ['sender', 'receiver', 'message']# update keys for using for authentication
    transaction_keys = ['identity']
    if not all(key in json for key in transaction_keys):
        return 'Houstein, we have a problem . It looks like Some elements are missing!!!', 400
    #index = blockchain.add_transaction(json['sender'], json['receiver'], json['message'])
    index = blockchain.add_transaction(json['identity'])
    response = {'message' : f'This transaction will be added to Block {index}'}
    return jsonify(response), 201



# Decentralizing our Blockchain

#Connecting a New node

@app.route('/connect_node', methods = ['POST'])

def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No Nodes found', 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'All the nodes are connected. HARLECOIN Blockchain now contains the following nodes: ',
                'total_nodes' : list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain with the longest chain if needed

@app.route('/replace_chain', methods = ['GET'])

def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message' : 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain' : blockchain.chain}
    else:
        response = {'message' : 'All good. The blockchain is largest one.',
                    'actual_chain' : blockchain.chain}
    return jsonify(response), 200


# Running the app

app.run(host = '0.0.0.0', port = 5005)