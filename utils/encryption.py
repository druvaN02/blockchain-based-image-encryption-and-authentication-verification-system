import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import json


class ImageEncryption:
    """Handle AES-256 encryption and decryption of images"""
    
    def __init__(self, key_file=None):
        """
        Initialize encryption handler
        
        Args:
            key_file: Path to save/load encryption key
        """
        self.key_file = key_file
        self.key = None
        
        if key_file and os.path.exists(key_file):
            self.load_key(key_file)
    
    def generate_key(self):
        """Generate a new AES-256 encryption key"""
        self.key = os.urandom(32)  # 256 bits
        return self.key
    
    def save_key(self, file_path):
        """Save encryption key to file"""
        with open(file_path, 'wb') as f:
            f.write(self.key)
    
    def load_key(self, file_path):
        """Load encryption key from file"""
        with open(file_path, 'rb') as f:
            self.key = f.read()
        return self.key
    
    def derive_key_from_password(self, password, salt=None):
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt for key derivation (generated if None)
            
        Returns:
            tuple: (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        self.key = kdf.derive(password.encode())
        return self.key, salt
    
    def encrypt_image(self, image_data):
        """
        Encrypt image data using AES-256-CBC
        
        Args:
            image_data: Binary image data
            
        Returns:
            dict: Encrypted data with IV
        """
        if self.key is None:
            self.generate_key()
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad the data
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(image_data) + padder.finalize()
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return {
            'encrypted_data': encrypted_data,
            'iv': iv,
            'key': self.key
        }
    
    def decrypt_image(self, encrypted_data, iv, key=None):
        """
        Decrypt image data using AES-256-CBC
        
        Args:
            encrypted_data: Encrypted binary data
            iv: Initialization vector
            key: Encryption key (uses self.key if None)
            
        Returns:
            bytes: Decrypted image data
        """
        if key is not None:
            self.key = key
        
        if self.key is None:
            raise ValueError("Encryption key not set")
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Unpad the data
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        return decrypted_data
    
    def encrypt_file(self, input_file, output_file):
        """
        Encrypt a file and save to output file
        
        Args:
            input_file: Path to input file
            output_file: Path to save encrypted file
            
        Returns:
            dict: Encryption metadata
        """
        with open(input_file, 'rb') as f:
            file_data = f.read()
        
        encrypted = self.encrypt_image(file_data)
        
        # Save encrypted data
        with open(output_file, 'wb') as f:
            f.write(encrypted['encrypted_data'])
        
        # Save metadata
        metadata = {
            'iv': base64.b64encode(encrypted['iv']).decode(),
            'original_name': os.path.basename(input_file)
        }
        
        metadata_file = output_file + '.meta'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
        
        return metadata
    
    def decrypt_file(self, encrypted_file, output_file, metadata_file=None):
        """
        Decrypt a file and save to output file
        
        Args:
            encrypted_file: Path to encrypted file
            output_file: Path to save decrypted file
            metadata_file: Path to metadata file (auto-detected if None)
            
        Returns:
            bool: Success status
        """
        if metadata_file is None:
            metadata_file = encrypted_file + '.meta'
        
        # Load metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        iv = base64.b64decode(metadata['iv'])
        
        # Read encrypted data
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt
        decrypted_data = self.decrypt_image(encrypted_data, iv)
        
        # Save decrypted file
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        return True
