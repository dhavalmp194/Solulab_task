import time
import random
import threading
from web3 import Web3
import config  # Import the configuration file

# Connect to Ethereum network (e.g., Infura, Alchemy)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/04bbf1252bbc4283a825a9694511153d'))

# Define the USDT contract address and ABI
USDT_CONTRACT_ADDRESS = Web3.to_checksum_address(config.USDT_CONTRACT_ADDRESS)  # USDT contract address
USDT_ABI = [
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

# Create contract instance
usdt_contract = w3.eth.contract(address=USDT_CONTRACT_ADDRESS, abi=USDT_ABI)

# Define the words for random message generation
WORDS = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

class RealAgent:

    def __init__(self, name, wallet_address, private_key):
        self.name = name
        self.inbox = []
        self.outbox = []
        self.wallet_address = wallet_address  # Wallet address for transactions
        self.private_key = private_key  # Private key for signing transactions
        self.message_handlers = {}  # Dictionary to hold message handlers

    def register_message_handler(self, message_type, handler):
        """Register a message handler for a specific message type."""
        self.message_handlers[message_type] = handler

    def send_message(self, message, recipient):
        """Send a message to the OutBox."""
        recipient.inbox.append(message)
        print(f"[{self.name}] Sent Message: {message}")

    def send_crypto_message(self, recipient_address, amount=1.1E-10):  # Default amount set to 1.1E-10
        """Send a crypto message to the specified recipient address with the specified amount."""
        message = f"crypto {recipient_address} {amount}"  # Format the message
        self.send_message(message, self)  # Send the message to self for processing

    def handle_message(self, message):
        """Handle incoming messages based on their content."""
        for message_type, handler in self.message_handlers.items():
            if message_type in message:
                handler(message)

    def handle_crypto(self, message, sender_private_key):
        """Handle crypto messages and perform token transfer."""
        parts = message.split()
        if len(parts) != 3:
            print(f"[{self.name}] Invalid crypto message format: {message}")
            return

        recipient_address = parts[1]  # Extract recipient address
        amount_to_send = float(parts[2])  # Extract amount to send

        try:
            # Fetch balance from the blockchain
            balance = usdt_contract.functions.balanceOf(self.wallet_address).call()
        except Exception as e:
            print(f"[{self.name}] Error fetching balance: {e}")
            return  # Exit early if there's an error fetching the balance

        amount_to_send_wei = w3.to_wei(amount_to_send, 'ether')  # Convert USDT to Wei

        if balance < amount_to_send_wei:
            print(f"[{self.name}] Not enough USDT to transfer for: {message}")
            return  # Exit early if balance is insufficient

        # Log the current balance and recipient address
        print(f"[{self.name}] Current Balance: {w3.from_wei(balance, 'ether')} USDT, Recipient: {recipient_address}")

        # Prepare transaction
        nonce = w3.eth.get_transaction_count(self.wallet_address)
        gas_price = w3.eth.gas_price  # Get current gas price

        transaction = usdt_contract.functions.transfer(recipient_address, amount_to_send_wei).build_transaction({
            'chainId': 11155111,  # Sepolia Testnet
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign the transaction with the sender's private key
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=sender_private_key)

        # Send the transaction
        try:
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"[{self.name}] Transaction successful - Tx Hash: {tx_hash.hex()}")
            time.sleep(5)  # Wait for 5 seconds after the transaction
        except Exception as e:
            print(f"[{self.name}] Transaction failed for: {message} - Error: {e}")

    def generate_random_message(self, recipient):
        """Generate random 2-word messages every 2 seconds, with occasional crypto messages."""
        while True:
            if random.random() < 0.1:  # 10% chance to send a crypto message
                recipient_address = recipient.wallet_address  # Use the recipient's wallet address
                amount_to_send = 1.1E-10  # Example amount
                self.send_crypto_message(recipient_address, amount_to_send)
            else:
                message = f"{random.choice(WORDS)} {random.choice(WORDS)}"
                self.send_message(message, recipient)
            time.sleep(2)

    def start(self, recipient):
        """Start the agent's threads for message handling and generation."""
        threading.Thread(target=self.receive_messages, daemon=True).start()
        threading.Thread(target=self.generate_random_message, args=(recipient,), daemon=True).start()

    def receive_messages(self):
        """Receive messages from the inbox and handle them."""
        while True:
            if self.inbox:
                message = self.inbox.pop(0)  # Get the first message from the inbox
                self.handle_message(message)  # Handle the received message
            time.sleep(1)  # Sleep for a short duration to avoid busy waiting

    def print_available_tokens(self):
        """Fetch and print available tokens for transaction."""
        balance = usdt_contract.functions.balanceOf(self.wallet_address).call()
        print(f"[{self.name}] Available Tokens:")
        print(f"USDT Balance: {w3.from_wei(balance, 'ether')} USDT")

# Create two real agents with wallet addresses and private keys from config
agent1 = RealAgent("Agent1", config.AGENT1_WALLET_ADDRESS, config.AGENT1_PRIVATE_KEY)
agent2 = RealAgent("Agent2", config.AGENT2_WALLET_ADDRESS, config.AGENT2_PRIVATE_KEY)

# Print available tokens before starting the agents
agent1.print_available_tokens()
agent2.print_available_tokens()

# Ask user if they want to continue with the AI agents
user_input = input("Do you want to continue with the AI agents? (yes/no): ").strip().lower()
if user_input != 'yes':
    print("Exiting the program.")
    exit()

# Register message handlers
agent1.register_message_handler("hello", lambda msg: print(f"[{agent1.name}] Hello Message Received: {msg}"))
agent1.register_message_handler("crypto", lambda msg: agent1.handle_crypto(msg, agent1.private_key))

agent2.register_message_handler("hello", lambda msg: print(f"[{agent2.name}] Hello Message Received: {msg}"))
agent2.register_message_handler("crypto", lambda msg: agent2.handle_crypto(msg, agent2.private_key))

# Start the agents
agent1.start(agent2)  # Agent1 will send messages to Agent2
agent2.start(agent1)  # Agent2 will send messages to Agent1

# Keep the main thread alive to allow the agents to run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted. Shutting down gracefully...")
