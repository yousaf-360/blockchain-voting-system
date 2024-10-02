import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Web3 from 'web3';
import './App.css'; 

function App() {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [account, setAccount] = useState('');
  const [web3, setWeb3] = useState(null);

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/candidates');
        setCandidates(response.data.candidates);
      } catch (error) {
        console.error('Error fetching candidates:', error);
        alert('Failed to load candidates. Please check the console for more details.');
      }
    };
    fetchCandidates();

    const connectAccount = async () => {
      if (window.ethereum) {
        try {
          const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
          setAccount(accounts[0]);

          const web3Instance = new Web3(window.ethereum);
          const networkId = await web3Instance.eth.net.getId();

          console.log('Connected Network ID:', networkId);
          setWeb3(web3Instance);
        } catch (error) {
          console.error('Error connecting to MetaMask:', error);
        }
      } else {
        alert('Ethereum wallet not detected. Please install MetaMask.');
      }
    };
    connectAccount();
  }, []);

  const handleChange = (candidateId) => {
    setSelectedCandidate(candidateId);
  };

  const vote = async () => {
    if (!selectedCandidate) {
      alert('Please select a candidate to vote for.');
      return;
    }

    if (web3) {
      try {
        const transactionParameters = {
          to: '0x6a7a2ba8E7123990b237c8d9033D0c8d46f1E938', 
          from: account,
          gas: '100000',
          data: web3.eth.abi.encodeFunctionCall(
            {
              name: 'vote',
              type: 'function',
              inputs: [{ type: 'uint256', name: 'candidateId' }],
            },
            [selectedCandidate]
          ),
        };

        const txHash = await window.ethereum.request({
          method: 'eth_sendTransaction',
          params: [transactionParameters],
        });

        alert('Vote cast successfully! Transaction Hash: ' + txHash);

        const updatedCandidates = await fetchUpdatedCandidates();
        setCandidates(updatedCandidates);
      } catch (error) {
        alert('Error voting: ' + (error.message || 'An error occurred'));
      }
    } else {
      alert('Web3 is not initialized properly.');
    }
  };

  const fetchUpdatedCandidates = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/candidates'); 
      return response.data.candidates;
    } catch (error) {
      console.error('Error fetching updated candidates:', error);
      return candidates; 
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Voting System</h1>
      <p className="app-description">CAST YOUR VOTE!</p>

      {candidates.length === 0 ? (
        <p>Loading candidates...</p>
      ) : (
        <div className="candidates-container">
          {candidates.map((candidate) => (
            <div key={candidate.id} className="candidate-card">
              <label className="candidate-label">
                <input
                  type="radio"
                  name="candidate"
                  value={candidate.id}
                  checked={selectedCandidate === candidate.id}
                  onChange={() => handleChange(candidate.id)}
                  className="candidate-radio"
                />
                <span className="candidate-name">{candidate.name}</span>
                <span className="candidate-votes">({candidate.voteCount} votes)</span>
              </label>
            </div>
          ))}
          <button className="vote-button" onClick={vote}>Vote</button>
        </div>
      )}
    </div>
  );
}

export default App;
