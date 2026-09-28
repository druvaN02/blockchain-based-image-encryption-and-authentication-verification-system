from web3 import Web3
from eth_account import Account
import json
import os


class BlockchainInterface:
    """Interface for interacting with Ethereum blockchain"""
    
    def __init__(self, node_url, contract_address, contract_abi, private_key=None):
        """
        Initialize blockchain interface
        
        Args:
            node_url: Ethereum node URL
            contract_address: Deployed contract address
            contract_abi: Contract ABI
            private_key: Private key for transactions
        """
        self.web3 = Web3(Web3.HTTPProvider(node_url))
        self.contract_address = Web3.to_checksum_address(contract_address) if contract_address else None
        self.private_key = private_key
        
        # Load contract
        if self.contract_address and contract_abi:
            self.contract = self.web3.eth.contract(
                address=self.contract_address,
                abi=contract_abi
            )
        else:
            self.contract = None
        
        # Set default account if private key provided
        if private_key:
            self.account = Account.from_key(private_key)
            self.web3.eth.default_account = self.account.address
        else:
            self.account = None
    
    def is_connected(self):
        """Check if connected to blockchain"""
        return self.web3.is_connected()
    
    def get_balance(self, address=None):
        """Get ETH balance of an address"""
        if address is None and self.account:
            address = self.account.address
        
        if address:
            balance = self.web3.eth.get_balance(Web3.to_checksum_address(address))
            return self.web3.from_wei(balance, 'ether')
        return 0
    
    def register_image(self, image_hash, file_name):
        """
        Register an image on the blockchain
        
        Args:
            image_hash: SHA-256 hash of the image
            file_name: Original file name
            
        Returns:
            dict: Transaction receipt
        """
        if not self.contract or not self.account:
            raise Exception("Contract or account not initialized")
        
        # Build transaction
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        
        transaction = self.contract.functions.registerImage(
            image_hash,
            file_name
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': 20000000000
        })
        
        # Sign transaction
        signed_txn = self.web3.eth.account.sign_transaction(
            transaction,
            private_key=self.private_key
        )
        
        # Send transaction
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for transaction receipt
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'status': 'success' if tx_receipt['status'] == 1 else 'failed',
            'transaction_hash': tx_hash.hex(),
            'block_number': tx_receipt['blockNumber'],
            'gas_used': tx_receipt['gasUsed']
        }
    
    def verify_image(self, image_hash):
        """
        Verify an image on the blockchain
        
        Args:
            image_hash: SHA-256 hash of the image
            
        Returns:
            dict: Verification result
        """
        if not self.contract:
            raise Exception("Contract not initialized")
        
        try:
            # Call verifyImage function
            result = self.contract.functions.verifyImage(image_hash).call()
            
            exists, owner, timestamp, file_name = result
            
            return {
                'exists': exists,
                'owner': owner,
                'timestamp': timestamp,
                'file_name': file_name,
                'registered': exists
            }
        except Exception as e:
            return {
                'exists': False,
                'error': str(e)
            }
    
    def get_image_details(self, image_hash):
        """
        Get image details from blockchain (view function)
        
        Args:
            image_hash: SHA-256 hash of the image
            
        Returns:
            dict: Image details
        """
        if not self.contract:
            raise Exception("Contract not initialized")
        
        try:
            result = self.contract.functions.getImageDetails(image_hash).call()
            exists, owner, timestamp, file_name = result
            
            return {
                'exists': exists,
                'owner': owner,
                'timestamp': timestamp,
                'file_name': file_name
            }
        except Exception as e:
            return {'error': str(e)}
    
    def is_image_registered(self, image_hash):
        """Check if image is registered"""
        if not self.contract:
            return False
        
        try:
            return self.contract.functions.isImageRegistered(image_hash).call()
        except:
            return False
    
    def get_user_images(self, user_address):
        """Get all images registered by a user"""
        if not self.contract:
            raise Exception("Contract not initialized")
        
        try:
            image_hashes = self.contract.functions.getUserImages(
                Web3.to_checksum_address(user_address)
            ).call()
            
            return image_hashes
        except Exception as e:
            return []
    
    def get_total_images(self):
        """Get total number of registered images"""
        if not self.contract:
            return 0
        
        try:
            return self.contract.functions.getTotalImages().call()
        except:
            return 0
    
    def get_transaction_history(self, address=None):
        """
        Get transaction history for an address
        
        Args:
            address: Ethereum address (uses default account if None)
            
        Returns:
            list: Transaction history
        """
        if address is None and self.account:
            address = self.account.address
        
        if not address:
            return []
        
        # Get latest block number
        latest_block = self.web3.eth.block_number
        
        transactions = []
        
        # Search recent blocks (limit to last 1000 blocks for performance)
        start_block = max(0, latest_block - 1000)
        
        for block_num in range(start_block, latest_block + 1):
            try:
                block = self.web3.eth.get_block(block_num, full_transactions=True)
                
                for tx in block.transactions:
                    if tx['from'] == address or tx['to'] == address:
                        transactions.append({
                            'hash': tx['hash'].hex(),
                            'from': tx['from'],
                            'to': tx['to'],
                            'value': self.web3.from_wei(tx['value'], 'ether'),
                            'block_number': block_num,
                            'timestamp': block['timestamp']
                        })
            except:
                continue
        
        return transactions
    
    @staticmethod
    def load_contract_abi(abi_file):
        """Load contract ABI from file"""
        with open(abi_file, 'r') as f:
            return json.load(f)
