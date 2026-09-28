from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from utils.hashing import calculate_image_hash
from utils.encryption import ImageEncryption
from utils.image_handler import ImageHandler
from utils.blockchain import BlockchainInterface
from config import Config

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/api/upload', methods=['POST'])
def upload_image():
    """Handle image upload and registration"""
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not ImageHandler.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP'}), 400
        
        # Save uploaded file
        file_path, filename = ImageHandler.save_uploaded_file(
            file,
            Config.UPLOAD_FOLDER
        )
        
        # Validate image
        is_valid, error = ImageHandler.validate_image(file_path)
        if not is_valid:
            ImageHandler.cleanup_file(file_path)
            return jsonify({'error': error}), 400
        
        # Calculate image hash
        image_hash = calculate_image_hash(file_path)
        
        # Rename file to include hash for easier retrieval
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{image_hash}{file_extension}"
        new_file_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)
        
        # Rename the file (handle existing files)
        if file_path != new_file_path:
            # If target file already exists, remove it first
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            os.rename(file_path, new_file_path)
            file_path = new_file_path
            filename = new_filename
        
        # Get image info
        image_info = ImageHandler.get_image_info(file_path)
        
        # Encrypt image (optional)
        encrypt_option = request.form.get('encrypt', 'false').lower() == 'true'
        encrypted_path = None
        encryption_key = None
        
        if encrypt_option:
            encryptor = ImageEncryption()
            encryptor.generate_key()
            
            encrypted_filename = f"encrypted_{filename}"
            encrypted_path = os.path.join(Config.ENCRYPTED_FOLDER, encrypted_filename)
            
            encryptor.encrypt_file(file_path, encrypted_path)
            
            # Save encryption key
            key_filename = f"{image_hash}.key"
            key_path = os.path.join(Config.KEYS_FOLDER, key_filename)
            encryptor.save_key(key_path)
            
            encryption_key = key_filename
        
        # Prepare response
        response = {
            'success': True,
            'image_hash': image_hash,
            'filename': filename,
            'file_size': image_info.get('file_size'),
            'dimensions': f"{image_info['width']}x{image_info['height']}",
            'format': image_info.get('format'),
            'timestamp': datetime.now().isoformat(),
            'encrypted': encrypt_option,
            'message': 'Image uploaded successfully. Ready for blockchain registration.'
        }
        
        if encryption_key:
            response['encryption_key'] = encryption_key
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@upload_bp.route('/api/register', methods=['POST'])
def register_on_blockchain():
    """Register image hash on blockchain"""
    try:
        data = request.get_json()
        
        if not data or 'image_hash' not in data:
            return jsonify({'error': 'Image hash is required'}), 400
        
        image_hash = data['image_hash']
        filename = data.get('filename', 'unknown.jpg')
        
        # Initialize blockchain interface
        if not Config.CONTRACT_ADDRESS or not Config.PRIVATE_KEY:
            return jsonify({
                'error': 'Blockchain not configured. Please set CONTRACT_ADDRESS and PRIVATE_KEY in .env'
            }), 500
        
        # Load contract ABI
        abi_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'contracts',
            'compiled',
            'ImageVerification.abi'
        )
        
        if not os.path.exists(abi_path):
            return jsonify({
                'error': 'Contract ABI not found. Please compile the smart contract first.'
            }), 500
        
        contract_abi = BlockchainInterface.load_contract_abi(abi_path)
        
        blockchain = BlockchainInterface(
            Config.ETHEREUM_NODE_URL,
            Config.CONTRACT_ADDRESS,
            contract_abi,
            Config.PRIVATE_KEY
        )
        
        # Check if already registered
        if blockchain.is_image_registered(image_hash):
            return jsonify({
                'error': 'Image already registered on blockchain',
                'image_hash': image_hash
            }), 400
        
        # Register on blockchain
        result = blockchain.register_image(image_hash, filename)
        
        if result['status'] == 'success':
            return jsonify({
                'success': True,
                'message': 'Image successfully registered on blockchain',
                'transaction_hash': result['transaction_hash'],
                'block_number': result['block_number'],
                'gas_used': result['gas_used'],
                'image_hash': image_hash,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'error': 'Blockchain registration failed',
                'details': result
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@upload_bp.route('/api/upload-and-register', methods=['POST'])
def upload_and_register():
    """Combined endpoint: upload and register in one call"""
    try:
        # First, upload the image
        upload_result = upload_image()
        upload_data = upload_result[0].get_json()
        
        if upload_result[1] != 200:
            return upload_result
        
        # Then register on blockchain
        image_hash = upload_data['image_hash']
        filename = upload_data['filename']
        
        register_data = {
            'image_hash': image_hash,
            'filename': filename
        }
        
        # Create a mock request for register_on_blockchain
        original_json = request.get_json
        request.get_json = lambda: register_data
        
        register_result = register_on_blockchain()
        request.get_json = original_json
        
        if register_result[1] == 200:
            register_data = register_result[0].get_json()
            
            # Combine results
            combined_result = {**upload_data, **register_data}
            return jsonify(combined_result), 200
        else:
            return register_result
            
    except Exception as e:
        return jsonify({'error': f'Combined operation failed: {str(e)}'}), 500
