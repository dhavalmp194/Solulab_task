from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from web3 import Web3
import os
import time
import random
import threading
from dotenv import load_dotenv
from web3 import Web3
from langchain_openai import OpenAI  # Updated import

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEB3_URL = os.getenv("WEB3_URL")
CRYPTO_CONTRACT_ADDRESS = os.getenv("CRYPTO_CONTRACT_ADDRESS")
CHAIN_ID = os.getenv("CHAIN_ID")
GAS = os.getenv("GAS")
AGENT1_WALLET_ADDRESS = os.getenv("AGENT1_WALLET_ADDRESS")
AGENT1_PRIVATE_KEY = os.getenv("AGENT1_PRIVATE_KEY")
AGENT2_WALLET_ADDRESS = os.getenv("AGENT2_WALLET_ADDRESS")
AGENT2_PRIVATE_KEY = os.getenv("AGENT2_PRIVATE_KEY")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(WEB3_URL))
if not w3.is_connected():
    print("Web3 is not connected. Check your INFURA_URL or node.")
    exit(1)  # Exit the script if not connected

# USDT Contract ABI
usdt_abi = [
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
]

# Load contract
usdt_contract = w3.eth.contract(address=CRYPTO_CONTRACT_ADDRESS, abi=usdt_abi)


# Define the AI Agent
class AIAgent:

    def __init__(self, name, wallet_address, private_key):
        self.name = name
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.inbox = []
        self.outbox = []
        self.llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)  # Initialize the AI model

    def get_balance(self):
        balance = usdt_contract.functions.balanceOf(self.wallet_address).call()
        return w3.from_wei(balance, 'ether')

    def send_crypto(self, recipient_address, amount):
        # Check balance before sending
        balance = self.get_balance()
        amount_in_wei = w3.to_wei(amount, 'ether')
        gas_price = w3.eth.gas_price
        estimated_gas = 2000000  # You can adjust this based on your needs

        total_cost = gas_price * estimated_gas + amount_in_wei
        if balance < total_cost:
            print(f"[{self.name}] Insufficient funds to send {amount} Ether. Current balance: {balance} Ether.")
            return None  # Exit if insufficient funds

        # Prepare and send a transaction
        nonce = w3.eth.get_transaction_count(self.wallet_address)
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': amount_in_wei,
            'gas': estimated_gas,
            'gasPrice': gas_price
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return w3.to_hex(tx_hash)

    def send_message(self, message, recipient):
        recipient.inbox.append(message)
        print(f"[{self.name}] Sent Message: {message}")

    def handle_message(self, message, recipient_agent):
        if "crypto" in message.lower():
            amount_to_send = 1  # in Ether
            tx_hash = self.send_crypto(recipient_agent.wallet_address, amount_to_send)
            print(f"[{self.name}] Sent {amount_to_send} Ether to {recipient_agent.name}. Transaction Hash: {tx_hash}")
        elif "hello" in message.lower():
            print(f"[{self.name}] Received hello message: {message}")
        else:
            print(f"[{self.name}] No action taken for message: {message}")

    def generate_ai_message(self):
        prompt = """Generate a two-word random message with the help of this ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", 
        "human"] words. you have to generate message from only given words don't use any other words ."""
        response = self.llm(prompt)
        return response.strip()  # Clean up the response

    def generate_random_message(self, recipient):
        """Generate messages every 2 seconds, with occasional crypto messages."""
        while True:
            if random.random() < 0.1:  # 10% chance to send a crypto message
                recipient_address = recipient.wallet_address  # Use the recipient's wallet address
                amount_to_send = 0.01  # Example amount
                self.send_message(f"crypto {recipient_address} {amount_to_send}", self)  # Send crypto message
            else:
                message = self.generate_ai_message()  # Generate message using AI
                self.send_message(message, recipient)
            time.sleep(2)  # Wait for 2 seconds before sending the next message

    def receive_messages(self):
        """Receive messages from the inbox and handle them."""
        while True:
            if self.inbox:
                message = self.inbox.pop(0)  # Get the first message from the inbox
                self.handle_message(message, self)  # Handle the received message
            time.sleep(1)  # Sleep for a short duration to avoid busy waiting

    def start(self, recipient):
        """Start the agent's threads for message handling and generation."""
        threading.Thread(target=self.receive_messages, daemon=True).start()
        threading.Thread(target=self.generate_random_message, args=(recipient,), daemon=True).start()


# Main execution
def main():
    # Initialize the agents
    agent1 = AIAgent("Agent1", AGENT1_WALLET_ADDRESS, AGENT1_PRIVATE_KEY)
    agent2 = AIAgent("Agent2", AGENT2_WALLET_ADDRESS, AGENT2_PRIVATE_KEY)

    # Start the agents
    agent1.start(agent2)  # Agent1 will send messages to Agent2
    agent2.start(agent1)  # Agent2 will send messages to Agent1

    # Keep the main thread alive to allow the agents to run
    try:
        while True:
            time.sleep(1)  # Sleep to keep the main thread alive
    except KeyboardInterrupt:
        print("Program interrupted. Shutting down gracefully...")


if __name__ == "__main__":
    main()
