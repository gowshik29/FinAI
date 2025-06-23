// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FinanceLedger {
    struct Transaction {
        uint id;
        string purpose;
        uint amount;
        uint timestamp;
    }

    Transaction[] public transactions;

    function logTransaction(uint id, string memory purpose, uint amount) public {
        transactions.push(Transaction(id, purpose, amount, block.timestamp));
    }

    function getTransactionCount() public view returns (uint) {
        return transactions.length;
    }

    function getTransaction(uint index) public view returns (uint, string memory, uint, uint) {
        require(index < transactions.length, "Index out of bounds");
        Transaction memory txn = transactions[index];
        return (txn.id, txn.purpose, txn.amount, txn.timestamp);
    }

    function getAllTransactions() public view returns (Transaction[] memory) {
        return transactions;
    }
}
