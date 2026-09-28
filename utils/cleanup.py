import os
import time
from datetime import datetime, timedelta
from config import Config


class FileCleanup:
    """Handle automatic cleanup of old files"""
    
    @staticmethod
    def cleanup_old_files():
        """Delete files older than retention period"""
        try:
            retention_days = Config.RETENTION_DAYS
            cutoff_time = time.time() - (retention_days * 24 * 60 * 60)
            
            deleted_count = 0
            folders_to_check = [
                Config.UPLOAD_FOLDER,
                Config.ENCRYPTED_FOLDER,
                Config.KEYS_FOLDER
            ]
            
            for folder in folders_to_check:
                if not os.path.exists(folder):
                    continue
                
                for filename in os.listdir(folder):
                    # Skip .gitkeep files
                    if filename == '.gitkeep':
                        continue
                    
                    file_path = os.path.join(folder, filename)
                    
                    # Check if it's a file (not directory)
                    if not os.path.isfile(file_path):
                        continue
                    
                    # Get file creation/modification time
                    file_time = os.path.getmtime(file_path)
                    
                    # Delete if older than retention period
                    if file_time < cutoff_time:
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                            print(f"Deleted old file: {filename}")
                        except Exception as e:
                            print(f"Error deleting {filename}: {str(e)}")
            
            if deleted_count > 0:
                print(f"Cleanup complete: {deleted_count} files deleted")
            else:
                print("Cleanup complete: No files to delete")
            
            return deleted_count
            
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
            return 0
    
    @staticmethod
    def get_file_age_days(file_path):
        """Get age of file in days"""
        try:
            file_time = os.path.getmtime(file_path)
            age_seconds = time.time() - file_time
            age_days = age_seconds / (24 * 60 * 60)
            return age_days
        except:
            return 0
    
    @staticmethod
    def is_file_expired(file_path):
        """Check if file has exceeded retention period"""
        age_days = FileCleanup.get_file_age_days(file_path)
        return age_days > Config.RETENTION_DAYS
