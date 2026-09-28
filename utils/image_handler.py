import os
from PIL import Image
import io
from werkzeug.utils import secure_filename


class ImageHandler:
    """Handle image processing and validation"""
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    MAX_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImageHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_image(file_data):
        """
        Validate if file is a valid image
        
        Args:
            file_data: Binary file data or file path
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            if isinstance(file_data, str):
                img = Image.open(file_data)
            else:
                img = Image.open(io.BytesIO(file_data))
            
            # Verify it's a valid image
            img.verify()
            
            return True, None
        except Exception as e:
            return False, f"Invalid image: {str(e)}"
    
    @staticmethod
    def save_uploaded_file(file, upload_folder, custom_name=None):
        """
        Save uploaded file securely
        
        Args:
            file: FileStorage object from Flask
            upload_folder: Folder to save the file
            custom_name: Custom filename (uses original if None)
            
        Returns:
            tuple: (file_path, filename)
        """
        if custom_name:
            filename = secure_filename(custom_name)
        else:
            filename = secure_filename(file.filename)
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Create unique filename if file exists
        base_name, ext = os.path.splitext(filename)
        counter = 1
        final_filename = filename
        
        while os.path.exists(os.path.join(upload_folder, final_filename)):
            final_filename = f"{base_name}_{counter}{ext}"
            counter += 1
        
        file_path = os.path.join(upload_folder, final_filename)
        file.save(file_path)
        
        return file_path, final_filename
    
    @staticmethod
    def compress_image(input_path, output_path=None, quality=85, max_size=None):
        """
        Compress image while maintaining quality
        
        Args:
            input_path: Input image path
            output_path: Output path (overwrites input if None)
            quality: JPEG quality (1-100)
            max_size: Maximum dimension (width or height)
            
        Returns:
            str: Output file path
        """
        if output_path is None:
            output_path = input_path
        
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if saving as JPEG
            if img.mode == 'RGBA' and output_path.lower().endswith('.jpg'):
                img = img.convert('RGB')
            
            # Resize if max_size specified
            if max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save with compression
            img.save(output_path, quality=quality, optimize=True)
        
        return output_path
    
    @staticmethod
    def create_thumbnail(input_path, output_path, size=(200, 200)):
        """
        Create thumbnail of image
        
        Args:
            input_path: Input image path
            output_path: Output thumbnail path
            size: Thumbnail size tuple (width, height)
            
        Returns:
            str: Output file path
        """
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(output_path, quality=85, optimize=True)
        
        return output_path
    
    @staticmethod
    def get_image_info(file_path):
        """
        Get detailed image information
        
        Args:
            file_path: Path to image file
            
        Returns:
            dict: Image information
        """
        try:
            with Image.open(file_path) as img:
                info = {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': os.path.getsize(file_path),
                    'file_name': os.path.basename(file_path)
                }
                
                # Add EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    info['exif'] = img._getexif()
                
                return info
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def convert_to_format(input_path, output_path, output_format='PNG'):
        """
        Convert image to different format
        
        Args:
            input_path: Input image path
            output_path: Output image path
            output_format: Target format (PNG, JPEG, etc.)
            
        Returns:
            str: Output file path
        """
        with Image.open(input_path) as img:
            # Convert RGBA to RGB for JPEG
            if output_format.upper() == 'JPEG' and img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.save(output_path, format=output_format)
        
        return output_path
    
    @staticmethod
    def read_image_as_bytes(file_path):
        """Read image file as bytes"""
        with open(file_path, 'rb') as f:
            return f.read()
    
    @staticmethod
    def cleanup_file(file_path):
        """Safely delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
        return False
