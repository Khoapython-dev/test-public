# Blockchain 
"""
blockchain: Zraight Numium
version: 1.1.2
"""

import hashlib
from enum import Enum  # giữ nguyên
from dataclasses import dataclass, field
import os 
import time, random
import sys

# extension
sys.path.append("/home/blockchain/core/extension")
import ctypes

LIB_PATH = "/home/blockchain/core/extension/so_lib64Proof_h.so"
native = ctypes.CDLL(LIB_PATH)

native.mine.argtypes = [
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_ulonglong)
]

native.mine.restype = None

class Block:

    @dataclass
    class _Block:
        index: int
        data: dict
        nonce: int
        difficulty: int
        timestamp: float
        Bhash: str
        PrevHash: str = "0"

    def __init__(self, idx, data, diff, prev_hash="0"):
        self.struct = Block._Block(
            index=idx,
            data=data,
            nonce=0,
            difficulty=diff,
            timestamp=time.time(),
            Bhash="",
            PrevHash=prev_hash
        )

    def calcHash(self):
        content = (
            f"zn://{self.struct.data}/"
            f"{self.struct.index}/"
            f"{self.struct.nonce}/"
            f"{self.struct.difficulty}|"
            f"{self.struct.timestamp}@"
            f"{self.struct.PrevHash}END"
        )
        return hashlib.sha256(content.encode()).hexdigest()
        
    def mine(self):

      base_data = (
          f"zn://{self.struct.data}/"
          f"{self.struct.index}/"
          f"{self.struct.difficulty}|"
          f"{self.struct.timestamp}@"
          f"{self.struct.PrevHash}END"
      ).encode()

      output_hash = ctypes.create_string_buffer(65)
      final_nonce = ctypes.c_ulonglong()

      native.mine(
          base_data,
          self.struct.difficulty,
          output_hash,
          ctypes.byref(final_nonce)
      )

      self.struct.nonce = final_nonce.value
      self.struct.Bhash = output_hash.value.decode()


class DataSplit(Block):

    @dataclass
    class HandlerRest:
        sender: str 
        claimer: str 
        ip_send: str 
        ip_claim: str 
        msg: str 
        amount: int 

    def __init__(self, idx, data, diff, prev_hash="0"):
        super().__init__(idx, data, diff, prev_hash)

        DATA = self.struct.data

        self.hr = DataSplit.HandlerRest(
            DATA['sender'], 
            DATA['claimer'],
            DATA['ip_send'],
            DATA['ip_claim'],
            DATA['msg'],
            DATA['amount']
        )


class Blockchain:
    def __init__(self):
        self.chain = []

        genesis = Block(0, {"msg": "Genesis Block"}, 4)
        genesis.mine()
        self.chain.append(genesis)

    def add_block(self, data):
        prev_block = self.chain[-1]

        block = Block(
            len(self.chain),
            data,
            4,
            prev_block.struct.Bhash
        )

        block.mine()
        self.chain.append(block)

    def get_latest_block(self):
        return self.chain[-1]
        
bc = Blockchain()
bc.add_block({"sender": "A", "amount": 10})

print(bc.chain[-1].struct.Bhash)
print(bc.chain[-1].struct.nonce)