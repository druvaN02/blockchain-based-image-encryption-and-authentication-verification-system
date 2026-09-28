from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from utils.blockchain import BlockchainInterface
from config import Config

history_bp = Blueprint('history', __name__)


@history_bp.route('/api/history/<address>', methods=['GET'])
def get_user_history(address):
    """Get transaction history for a user address"""
    try:
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
        
        # Get user's images
        image_hashes = blockchain.get_user_images(address)
        
        # Get details for each image
        images = []
        for image_hash in image_hashes:
            details = blockchain.get_image_details(image_hash)
            if details.get('exists'):
                images.append({
                    'image_hash': image_hash,
                    'owner': details['owner'],
                    'timestamp': details['timestamp'],
                    'registration_date': datetime.fromtimestamp(details['timestamp']).isoformat(),
                    'filename': details['file_name']
                })
        
        return jsonify({
            'success': True,
            'address': address,
            'total_images': len(images),
            'images': images
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch history: {str(e)}'}), 500


@history_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Get blockchain statistics"""
    try:
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
        
        # Get statistics
        total_images = blockchain.get_total_images()
        is_connected = blockchain.is_connected()
        
        stats = {
            'success': True,
            'connected': is_connected,
            'total_images_registered': total_images,
            'contract_address': Config.CONTRACT_ADDRESS,
            'network_id': Config.NETWORK_ID,
            'timestamp': datetime.now().isoformat()
        }
        
        # Get balance if account available
        if Config.PRIVATE_KEY:
            balance = blockchain.get_balance()
            stats['account_balance'] = f"{balance} ETH"
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500


@history_bp.route('/api/all-images', methods=['GET'])
def get_all_images():
    """Get all registered images (with pagination)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
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
        
        # Get total images
        total = blockchain.get_total_images()
        
        # Calculate pagination
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total)
        
        # Calculate retention cutoff time
        retention_days = Config.RETENTION_DAYS
        cutoff_timestamp = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)
        
        # Fetch images
        images = []
        for idx in range(start_idx, end_idx):
            try:
                image_hash = blockchain.contract.functions.getImageByIndex(idx).call()
                details = blockchain.get_image_details(image_hash)
                
                if details.get('exists'):
                    # Check if image is within retention period
                    if details['timestamp'] >= cutoff_timestamp:
                        images.append({
                            'image_hash': image_hash,
                            'owner': details['owner'],
                            'timestamp': details['timestamp'],
                            'registration_date': datetime.fromtimestamp(details['timestamp']).isoformat(),
                            'filename': details['file_name']
                        })
            except:
                continue
        
        return jsonify({
            'success': True,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'images': images
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch images: {str(e)}'}), 500
