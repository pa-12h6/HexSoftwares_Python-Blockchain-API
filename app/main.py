from fastapi import FastAPI
from .blockchain import Blockchain
from .models import Transaction


app = FastAPI(
    title="Python Blockchain API",
    description="A simple blockchain backend built using Python and FastAPI",
    version="1.0.0"
)


# Create blockchain object
blockchain = Blockchain()


@app.get("/")
def home():
    return {
        "message": "Python Blockchain API is running!",
        "status": "success"
    }


@app.get("/blockchain")
def get_blockchain():
    return {
        "length": len(blockchain.chain),
        "chain": blockchain.get_chain()
    }


@app.post("/transactions")
def add_transaction(transaction: Transaction):

    block_index = blockchain.add_transaction(
        transaction.sender,
        transaction.receiver,
        transaction.amount
    )

    return {
        "message": f"Transaction will be added to block {block_index}",
        "transaction": transaction
    }


@app.post("/mine")
def mine_block():

    previous_block = blockchain.get_previous_block()

    previous_proof = previous_block["proof"]

    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash_block(previous_block)

    block = blockchain.create_block(
        proof,
        previous_hash
    )

    return {
        "message": "New block mined successfully!",
        "block": block
    }


@app.get("/validate")
def validate_blockchain():

    is_valid = blockchain.is_chain_valid()

    return {
        "blockchain_valid": is_valid
    }