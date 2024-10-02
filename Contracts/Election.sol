// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Election {
    // Candidate model
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Mappings
    mapping(uint => Candidate) public candidates;
    mapping(address => bool) public voters;

    // Candidate count
    uint public candidatesCount;

    // Event to notify when a vote is cast
    event VotedEvent(uint indexed candidateId);

    constructor() {
        addCandidate("Donald Trump");
        addCandidate("Kamala Harris");
    }

    // Private function to add a candidate
    function addCandidate(string memory _name) private {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    // Vote function
    function vote(uint candidateId) public {
        // Ensure the voter hasn't voted before
        require(!voters[msg.sender], "You have already voted");

        // Ensure the candidate is valid
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate");

        // Record that this account has voted
        voters[msg.sender] = true;

        // Update the candidate's vote count
        candidates[candidateId].voteCount++;

        // Trigger the event
        emit VotedEvent(candidateId);
    }

    // Return candidate details
    function getCandidate(uint candidateId) public view returns (string memory, uint) {
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate ID");
        Candidate memory candidate = candidates[candidateId];
        return (candidate.name, candidate.voteCount);
    }

    // Return the total number of candidates
    function getCandidateCount() public view returns (uint) {
        return candidatesCount;
    }
}
