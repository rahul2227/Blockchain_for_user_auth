# User Authentication model based on blockchain
This is a type of blockchain implementation in which we are trying to use the blockchain for user authentication. As blockchain technology is already pretty secure by design this implementation makes full use of this feature of blockchain and use it for user authentication.
For consensus [raft protocol](http://raft.github.io/) was used in this project. 
This model is deployed in a multi-single-multi structure of server applications.
The consensus is used in the form of key vault to make the whole process lot easier, the original key vault [vesper](https://github.com/Oaklight/Vesper.git) is the integral part of the verification algorithm.

## Block_structure
'''python
block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()), 
                 'previous_hash' : previous_hash,
                 'transactions' : self.transactions,
                 'merkle_root': merkle_root}
'''
This block structure was used in the main blockchain, In here the transactions are basically username or ID and password, These two will be hashed and will be mined in the blocks, in the time of mining we will be inserting the final hash value to our raft consensus.
When using the consensus algorithm we are pushing our values in the servers using PUT protocol and the using the GET protocol to verify our key value pair.

## Deployment
## This the deployment of the VESPER
## How to run the SERVER

Each server is initialized with an index and an `ip_list.txt`
```
usage: python3 server.py <id> <ip-list-file>
```

there is a file called `ip_list.txt` that has a list of IPs of the servers, the consensus majority will be calculated based on the "number of servers" (#lines) in this file. Make sure there are **no empty** lines!

example of 5-server `ip_list.txt`

```
http://127.0.0.1:5000
http://127.0.0.1:5001
http://127.0.0.1:5002
http://127.0.0.1:5003
http://127.0.0.1:5004
```

 example of running 5 servers
```
➜  python3 server.py 0 ip_list.txt
➜  python3 server.py 1 ip_list.txt
➜  python3 server.py 2 ip_list.txt
➜  python3 server.py 3 ip_list.txt
➜  python3 server.py 4 ip_list.txt
```

## How to run the CLIENT
the client can perform `GET` and `PUT` request from the command line.

- the first argument is always the `http://ip:port` of a functioning server
- the second is the `key`
- the third is optional and is a `value`
  - if the `value` **is** present the client performs a `PUT` request with key and value to the specified server
  - if the `value` **is not** present the client performs a `GET` request of the key to the specified server

```
PUT usage: python3 client.py 'address' 'key' 'value'
GET usage: python3 client.py 'address' 'key'
Format: address: http://ip:port
```

example of `PUT` key="name" , value="Leslie Lamport"
```
➜  python3 client.py http://127.0.0.1:5000 name "Leslie Lamport"
{'code': 'success'}
```
example of `GET` key="name" 
```
➜  python3 client.py http://127.0.0.1:5000 name 
{'code': 'success', 'payload': {'key': 'name', 'value': 'Leslie Lamport'}}
```

## Deployment of the main blockchain
`app.run(host = '0.0.0.0', port = 5005)`
In here the port number is the number of port in which we will be deplying our blockchain.

## USAGE
These blockchain nodes were deployed using [postman](https://www.postman.com/)

### GET CHAIN request
Our application will be initialized by a genesis block with structure shown above, this function will be displaying the whole chain.
`@app.route('/get_chain', methods = ['GET'])`

on postman select GET request and use URL below to view the whole chain.
`http://127.0.0.1:5005/get_chain`

### ADDING TRANSACTIONS
In this scenario our transactions would be ID and password.This method will be helping in adding the transactions in our block.
`@app.route('/add_transaction', methods = ['POST'])`


on postman select POST request and use URL below to add transactions in our chain.
`http://127.0.0.1:5005/add_transaction`

The transactions should be passed in json format.
```
{
"identity" : "",
"password" : ""
}
```
### MINING THE BLOCK  
This function will be mining our blocks into the blockchain.
`@app.route('/mine_block', methods = ['GET'])`

on postman select GET request and use URL below to mine blocks in our chain.
`http://127.0.0.1:5005/mine_block`

### CONSENSUS 
This is a GET request that will be handling the consensus part of our application
`@app.route('/is_consensus', methods = ['GET'])`

on postman select GET request and use URL below to check consensus and verify our chain data.
`http://127.0.0.1:5005/is_consensus`

### ADDING NODES
This blockchain is a decentralized blockchain which give it and additional layer of security in this scenario.
`@app.route('/connect_node', methods = ['POST'])`

on postman select POST request and use URL below to add nodes in our network.
`http://127.0.0.1:5005/connect_nodes`

The nodes address should be passed in json format.
example
```
{
    "nodes": ["http://127.0.0.1:5005", 
              "http://127.0.0.1:5006",
              "http://127.0.0.1:5007"]
}
```

### REPLACING CHAIN
Replacing the chain with the longest chain if needed, This function will help in maintaining the same chain over all the nodes.
`@app.route('/replace_chain', methods = ['GET'])`

on postman select GET request and use URL below to replace current chain from the longest chain .
`http://127.0.0.1:5005/replace_chain`

# Developed by
**Rahul sharma(rahul2227.l115@gmail.com)**



