from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from utils.hashing import calculate_image_hash, verify_image_integrity
from utils.image_handler import ImageHandler
from utils.blockchain import BlockchainInterface
from config import Config

verify_bp = Blueprint('verify', __name__)


@verify_bp.route('/api/verify', methods=['POST'])
def verify_image():
    """Verify image authenticity against blockchain"""
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not ImageHandler.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file temporarily
        temp_path = os.path.join(Config.UPLOAD_FOLDER, f"temp_verify_{file.filename}")
        file.save(temp_path)
        
        # Validate image
        is_valid, error = ImageHandler.validate_image(temp_path)
        if not is_valid:
            ImageHandler.cleanup_file(temp_path)
            return jsonify({'error': error}), 400
        
        # Calculate image hash
        image_hash = calculate_image_hash(temp_path)
        
        # Get image info
        image_info = ImageHandler.get_image_info(temp_path)
        
        # Clean up temp file
        ImageHandler.cleanup_file(temp_path)
        
        # Initialize blockchain interface
        if not Config.CONTRACT_ADDRESS:
            return jsonify({
                'error': 'Blockchain not configured'
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
                'error': 'Contract ABI not found'
            }), 500
        
        contract_abi = BlockchainInterface.load_contract_abi(abi_path)
        
        blockchain = BlockchainInterface(
            Config.ETHEREUM_NODE_URL,
            Config.CONTRACT_ADDRESS,
            contract_abi,
            Config.PRIVATE_KEY
        )
        
        # Check blockchain for image
        image_details = blockchain.get_image_details(image_hash)
        
        if image_details.get('exists'):
            # Image is registered
            return jsonify({
                'success': True,
                'verified': True,
                'authentic': True,
                'message': 'Image is verified and authentic',
                'image_hash': image_hash,
                'owner': image_details['owner'],
                'timestamp': image_details['timestamp'],
                'registration_date': datetime.fromtimestamp(image_details['timestamp']).isoformat(),
                'original_filename': image_details['file_name'],
                'uploaded_filename': file.filename,
                'file_size': image_info.get('file_size'),
                'dimensions': f"{image_info['width']}x{image_info['height']}",
                'format': image_info.get('format')
            }), 200
        else:
            # Image not found on blockchain
            return jsonify({
                'success': True,
                'verified': False,
                'authentic': False,
                'message': 'Image not found on blockchain. This image is not registered.',
                'image_hash': image_hash,
                'uploaded_filename': file.filename,
                'file_size': image_info.get('file_size'),
                'dimensions': f"{image_info['width']}x{image_info['height']}",
                'format': image_info.get('format')
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500


@verify_bp.route('/api/verify-hash', methods=['POST'])
def verify_hash():
    """Verify image by hash only (no file upload)"""
    try:
        data = request.get_json()
        
        if not data or 'image_hash' not in data:
            return jsonify({'error': 'Image hash is required'}), 400
        
        image_hash = data['image_hash']
        
        # Initialize blockchain interface
        if not Config.CONTRACT_ADDRESS:
            return jsonify({'error': 'Blockchain not configured'}), 500
        
        abi_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'contracts',
            'compiled',
            'ImageVerification.abi'
        )
        
        if not os.path.exists(abi_path):
            return jsonify({'error': 'Contract ABI not found'}), 500
        
        contract_abi = BlockchainInterface.load_contract_abi(abi_path)
        
        blockchain = BlockchainInterface(
            Config.ETHEREUM_NODE_URL,
            Config.CONTRACT_ADDRESS,
            contract_abi,
            Config.PRIVATE_KEY
        )
        
        # Check blockchain
        image_details = blockchain.get_image_details(image_hash)
        
        if image_details.get('exists'):
            return jsonify({
                'success': True,
                'verified': True,
                'authentic': True,
                'message': 'Hash verified on blockchain',
                'image_hash': image_hash,
                'owner': image_details['owner'],
                'timestamp': image_details['timestamp'],
                'registration_date': datetime.fromtimestamp(image_details['timestamp']).isoformat(),
                'original_filename': image_details['file_name']
            }), 200
        else:
            return jsonify({
                'success': True,
                'verified': False,
                'authentic': False,
                'message': 'Hash not found on blockchain',
                'image_hash': image_hash
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'Hash verification failed: {str(e)}'}), 500


@verify_bp.route('/api/check-tampering', methods=['POST'])
def check_tampering():
    """Check if image has been tampered with"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        if 'original_hash' not in request.form:
            return jsonify({'error': 'Original hash is required'}), 400
        
        file = request.files['image']
        original_hash = request.form['original_hash']
        
        # Save temp file
        temp_path = os.path.join(Config.UPLOAD_FOLDER, f"temp_tamper_{file.filename}")
        file.save(temp_path)
        
        # Calculate current hash
        current_hash = calculate_image_hash(temp_path)
        
        # Compare hashes
        is_tampered = current_hash != original_hash
        
        # Clean up
        ImageHandler.cleanup_file(temp_path)
        
        return jsonify({
            'success': True,
            'tampered': is_tampered,
            'original_hash': original_hash,
            'current_hash': current_hash,
            'message': 'Image has been tampered with' if is_tampered else 'Image is intact'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Tampering check failed: {str(e)}'}), 500
