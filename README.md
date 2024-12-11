# Blockchain AI Agent

## Overview

The `Blockchain_Ai_Agent.py` script implements a simple AI agent that interacts with the Ethereum blockchain to send and receive USDT (Tether) tokens. The agent can generate messages using AI and handle incoming messages, including cryptocurrency transactions.

## Features

- Connects to the Ethereum network (Sepolia Testnet).
- Interacts with the USDT smart contract to check balances and perform transfers.
- Generates messages using AI and sends them to other agents.
- Handles incoming messages and processes cryptocurrency transactions.
- Prints available USDT balance before starting the agents.

## Requirements

- Python 3.6 or higher
- `web3.py` library (version 7.5.0 or higher)
- `langchain-openai` library for AI message generation
- An Ethereum wallet address and private key for testing

## Installation

1. Clone the repository or download the script.
2. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have an Ethereum wallet address and private key for testing.

## Troubleshooting Dependency Issues

If you encounter any dependency errors while running the project, you can try upgrading the relevant packages using the following command:

```bash
pip install --upgrade web3 eth-account eth-abi parsimonious langchain-openai
```

This command will ensure that you have the latest versions of the `web3`, `eth-account`, `eth-abi`, `parsimonious`, and `langchain-openai` libraries, which may resolve compatibility issues with Python 3.12 or other dependencies.

## Usage

1. Open the script in your preferred Python environment.
2. Update the wallet addresses and private keys for `agent1` and `agent2` in the script.
3. Run the script:

   ```bash
   python Blockchain_Ai_Agent.py
   ```

## Code Structure

- **Imports**: The script imports necessary libraries such as `time`, `random`, `threading`, `web3`, and `langchain_openai`.
- **Ethereum Connection**: Connects to the Ethereum network using Infura or Alchemy.
- **USDT Contract**: Defines the USDT contract address and ABI for interaction.
- **AIAgent Class**: Implements the AI agent with methods for sending messages, handling messages, and performing cryptocurrency transactions.
- **Main Execution**: Creates two agents, prints their available tokens, and starts the message handling and generation processes.

## Example Output

When running the script, you can expect output similar to the following:
