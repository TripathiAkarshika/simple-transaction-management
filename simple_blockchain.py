import hashlib
import time
import json
import random

# Block class represents each block in the blockchain
class Block:
    def __init__(self, block_index, previous_block_hash, timestamp, block_transactions, block_hash, mining_nonce=0):
        self.block_index = block_index
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.block_transactions = block_transactions
        self.block_hash = block_hash
        self.mining_nonce = mining_nonce

    # This method generates the hash by combining the block’s details
    def generate_hash(self):
        block_data = f'{self.block_index}{self.previous_block_hash}{self.timestamp}{json.dumps(self.block_transactions)}{self.mining_nonce}'
        return hashlib.sha256(block_data.encode('utf-8')).hexdigest()

# Blockchain class manages the entire chain of blocks
class Blockchain:
    def __init__(self, miner_reward=50):
        self.blocks = []
        self.pending_transactions = []
        self.miner_reward = miner_reward  # Reward for the miner
        self.create_genesis_block()

    # Create the very first block (the genesis block)
    def create_genesis_block(self):
        genesis_block = Block(0, "0", int(time.time()), [], self.generate_hash())
        self.blocks.append(genesis_block)

    # Calculate the hash of the most recent block
    def generate_hash(self):
        last_block = self.blocks[-1] if self.blocks else None
        return last_block.generate_hash() if last_block else ""

    # Add a new transaction to the list of transactions
    def add_new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)

    # A simple check to validate transactions (assuming sender has enough balance)
    def validate_transaction(self, sender, amount):
        # For simplicity, we assume the sender has an infinite balance
        return True

    # Add a new block to the blockchain with the current transactions
    def mine_new_block(self):
        last_block = self.blocks[-1]
        new_block = Block(
            block_index=last_block.block_index + 1,
            previous_block_hash=last_block.block_hash,
            timestamp=int(time.time()),
            block_transactions=self.pending_transactions,
            block_hash="",
        )

        # Mine the block by finding a valid nonce
        new_block.mining_nonce = self.mine_block(new_block)
        new_block.block_hash = new_block.generate_hash()

        self.blocks.append(new_block)
        self.pending_transactions = []  # Clear the transactions after adding the block

        # Reward the miner
        self.add_new_transaction("System", "Miner", self.miner_reward)

    # Proof of work: Find a nonce that generates a hash starting with four zeros
    def mine_block(self, block):
        block.mining_nonce = random.randint(0, 1000000)
        while not block.generate_hash().startswith("0000"):  # Looking for a hash that starts with 4 zeros
            block.mining_nonce += 1
        return block.mining_nonce

    # Display the entire blockchain
    def display_chain(self):
        for block in self.blocks:
            print(f"Block Index: {block.block_index}")
            print(f"Previous Block Hash: {block.previous_block_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.block_transactions}")
            print(f"Block Hash: {block.block_hash}")
            print("-" * 40)

    # Check the integrity of the blockchain
    def verify_blockchain(self):
        for i in range(1, len(self.blocks)):
            block = self.blocks[i]
            prev_block = self.blocks[i - 1]
            if block.block_hash != block.generate_hash():
                print(f"Block {block.block_index} has been tampered with!")
                return False
            if block.previous_block_hash != prev_block.block_hash:
                print(f"Block {block.block_index} is not linked correctly to the previous block!")
                return False
        print("Blockchain is valid.")
        return True

# Example usage of the blockchain
if __name__ == "__main__":
    blockchain = Blockchain()

    # Creating transactions
    blockchain.add_new_transaction("Bala", "Akarshika", 50)
    blockchain.add_new_transaction("Sri Charan", "Nayeem", 30)

    # Adding a block with the transactions
    blockchain.mine_new_block()

    # More transactions
    blockchain.add_new_transaction("Nayeem", "Akarshika", 50)

    # Add another block
    blockchain.mine_new_block()

    # Display the entire blockchain
    print("Displaying Valid Blockchain:")
    blockchain.display_chain()

    # Verify the blockchain’s integrity (valid output)
    print("\nVerifying Valid Blockchain:")
    blockchain.verify_blockchain()

    # Tampering: Manually change a transaction amount in Block 2
    blockchain.blocks[1].block_transactions[0]['amount'] = 100  # Change the amount in the first transaction

    # Display the tampered blockchain
    print("\nDisplaying Tampered Blockchain:")
    blockchain.display_chain()

    # Verify the blockchain’s integrity (tampered output)
    print("\nVerifying Tampered Blockchain:")
    blockchain.verify_blockchain()
