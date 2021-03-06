import hashlib
import time

class Block:

    def __init__(self, index, proof_num, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_num = proof_num
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_num,
                                              self.prev_hash, self.data,
                                              self.timestamp)

        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_num,
                                               self.prev_hash, self.data,
                                               self.timestamp)


class Blockchain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_gen()

    def construct_gen(self):
        self.construct_block(proof_num=0, prev_hash=0)

    def construct_block(self, proof_num, prev_hash):
        block = Block(
            index=len(self.chain),
            proof_num=proof_num,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block

    @staticmethod

    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index | prev_block.calculate_hash != block.prev_hash:
            return False

        elif not Blockchain.verifying_proof(block.proof_num,
                                            prev_block.proof_num):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        proof_no = 0
        while Blockchain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, details_miner):

        self.new_data(
            sender="0",
            recipient=details_miner,
            quantity=1,
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_num
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        return Block(
            block_data['index'],
            block_data['proof_num'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])


blockchain = Blockchain()

print("** Let's go mining **")
print(blockchain.chain)

last_block = blockchain.latest_block
last_proof_num = last_block.proof_num
proof_num = blockchain.proof_of_work(last_proof_num)

blockchain.new_data(
    sender="0",
    recipient="Bob Ross",
    quantity=1,
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_num, last_hash)

print("** AEY Successfully Mined **")
print(blockchain.chain)