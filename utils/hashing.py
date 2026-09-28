import hashlib
from PIL import Image
import io

def calculate_image_hash(image_data):
    """
    Calculate SHA-256 hash of image data
    
    Args:
        image_data: Binary image data or file path
        
    Returns:
        str: Hexadecimal SHA-256 hash
    """
    if isinstance(image_data, str):
        # If file path is provided
        with open(image_data, 'rb') as f:
            image_bytes = f.read()
    else:
        # If binary data is provided
        image_bytes = image_data
    
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(image_bytes).hexdigest()
    return sha256_hash


def calculate_file_hash(file_path):
    """
    Calculate SHA-256 hash of any file
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Hexadecimal SHA-256 hash
    """
    sha256_hash = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def verify_image_integrity(original_hash, image_data):
    """
    Verify if an image matches its original hash
    
    Args:
        original_hash: Original SHA-256 hash
        image_data: Binary image data or file path
        
    Returns:
        bool: True if hashes match, False otherwise
    """
    current_hash = calculate_image_hash(image_data)
    return current_hash == original_hash


def get_image_metadata(image_path):
    """
    Extract metadata from an image
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: Image metadata including format, size, mode
    """
    try:
        with Image.open(image_path) as img:
            metadata = {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'info': img.info
            }
        return metadata
    except Exception as e:
        return {'error': str(e)}
