from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3
from pydantic import BaseModel
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

contract_address = '0x6a7a2ba8E7123990b237c8d9033D0c8d46f1E938'
contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "candidateId",
          "type": "uint256"
        }
      ],
      "name": "VotedEvent",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "candidates",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "voteCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "candidatesCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "voters",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "candidateId",
          "type": "uint256"
        }
      ],
      "name": "vote",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "candidateId",
          "type": "uint256"
        }
      ],
      "name": "getCandidate",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "getCandidateCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

class VoteRequest(BaseModel):
    candidate_id: int
    signed_transaction: str 

@app.get("/candidates")
def get_candidates():
    candidates_count = contract.functions.getCandidateCount().call()
    candidates = []
    for i in range(1, candidates_count + 1):
        candidate = contract.functions.getCandidate(i).call()
        candidates.append({"id": i, "name": candidate[0], "voteCount": candidate[1]})
    return {"candidates": candidates}

@app.post("/vote/")
def vote(vote_request: VoteRequest):
    candidate_id = vote_request.candidate_id
    signed_transaction = vote_request.signed_transaction

    try:
        tx_hash = w3.eth.sendRawTransaction(signed_transaction)
        w3.eth.waitForTransactionReceipt(tx_hash)
        return {"status": "Vote cast successfully", "tx_hash": tx_hash.hex()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Transaction error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing vote: " + str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
