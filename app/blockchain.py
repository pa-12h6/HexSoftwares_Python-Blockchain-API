import hashlib
import json
from datetime import datetime


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the first block
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        """
        Create a new block and add it to the blockchain.
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "transactions": self.pending_transactions.copy(),
            "proof": proof,
            "previous_hash": previous_hash
        }

        # Clear pending transactions after adding them to a block
        self.pending_transactions = []

        self.chain.append(block)

        return block

    def get_previous_block(self):
        """
        Return the last block in the blockchain.
        """
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        """
        Add a transaction to the list of pending transactions.
        """

        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }

        self.pending_transactions.append(transaction)

        # Return the index of the block that will contain
        # this transaction.
        return self.get_previous_block()["index"] + 1

    def hash_block(self, block):
        """
        Create a SHA-256 hash of a block.
        """

        encoded_block = json.dumps(
            block,
            sort_keys=True
        ).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        """
        Simple Proof-of-Work algorithm.

        We search for a proof where the SHA-256 hash
        starts with four zeros.
        """

        new_proof = 1

        while True:
            calculation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if calculation[:4] == "0000":
                return new_proof

            new_proof += 1

    def is_chain_valid(self):
        """
        Check whether the blockchain is valid.
        """

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check previous hash
            if current_block["previous_hash"] != self.hash_block(previous_block):
                return False

            # Check proof of work
            previous_proof = previous_block["proof"]
            current_proof = current_block["proof"]

            calculation = hashlib.sha256(
                str(current_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if calculation[:4] != "0000":
                return False

        return True

    def get_chain(self):
        """
        Return the complete blockchain.
        """
        return self.chain