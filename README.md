# Blockchain AI Agent

## Overview

The `Blockchain_Ai_Agent.py` script implements a simple AI agent that interacts with the Ethereum blockchain to send and receive USDT (Tether) tokens. The agent can generate random messages and handle incoming messages, including cryptocurrency transactions.

## Features

- Connects to the Ethereum network (Sepolia Testnet).
- Interacts with the USDT smart contract to check balances and perform transfers.
- Generates random messages and sends them to other agents.
- Handles incoming messages and processes cryptocurrency transactions.
- Prints available USDT balance before starting the agents.

## Requirements

- Python 3.6 or higher
- `web3.py` library (version 7.5.0 or higher)
- An Ethereum wallet address and private key for testing

## Installation

1. Clone the repository or download the script.
2. Install the required packages using pip:

   ```bash
   pip install web3
   ```

3. Ensure you have an Ethereum wallet address and private key for testing.

## Usage

1. Open the script in your preferred Python environment.
2. Update the wallet addresses and private keys for `agent1` and `agent2` in the script.
3. Run the script:

   ```bash
   python Blockchain_Ai_Agent.py
   ```

4. When prompted, enter `yes` to continue with the AI agents.

## Code Structure

- **Imports**: The script imports necessary libraries such as `time`, `random`, `threading`, and `web3`.
- **Ethereum Connection**: Connects to the Ethereum network using Infura or Alchemy.
- **USDT Contract**: Defines the USDT contract address and ABI for interaction.
- **RealAgent Class**: Implements the AI agent with methods for sending messages, handling messages, and performing cryptocurrency transactions.
- **Main Execution**: Creates two agents, prints their available tokens, and starts the message handling and generation processes.

## Example Output

When running the script, you can expect output similar to the following:
