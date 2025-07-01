import os
import datetime
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

from utils import ConfigManager

class OutputHandler(QObject):
    """
    Handler class for managing output operations including:
    - Copying text to clipboard
    - Saving text to files (with append or overwrite modes)
    
    This class integrates with ConfigManager for settings.
    """
    
    # Signals for notifying status updates
    clipboardStatusSignal = pyqtSignal(bool, str)  # Success flag, message
    fileStatusSignal = pyqtSignal(bool, str)       # Success flag, message
    
    def __init__(self):
        """Initialize the OutputHandler."""
        super().__init__()
        self._initialize_settings()
        
    def _initialize_settings(self):
        """Initialize settings from ConfigManager."""
        # Create default output settings if they don't exist
        if 'output_options' not in ConfigManager.get_config():
            ConfigManager.set_config_section('output_options', {
                'enable_clipboard': True,
                'enable_file_output': True,
                'output_file_path': os.path.join('output', 'transcriptions.txt'),
                'file_output_mode': 'append',  # 'append' or 'overwrite'
                'add_timestamp': True,
                'create_directory': True
            })
            ConfigManager.save_config()
        
    def process_output(self, text):
        """
        Process the text output by sending it to enabled output methods.
        
        Args:
            text (str): The text to output
            
        Returns:
            bool: True if all enabled outputs were successful, False otherwise
        """
        if not text:
            return False
            
        output_options = ConfigManager.get_config_section('output_options')
        success = True
        
        # Process clipboard output if enabled
        if output_options.get('enable_clipboard', True):
            clipboard_success = self.copy_to_clipboard(text)
            success = success and clipboard_success
            
        # Process file output if enabled
        if output_options.get('enable_file_output', True):
            file_success = self.save_to_file(text)
            success = success and file_success
            
        return success
            
    def copy_to_clipboard(self, text):
        """
        Copy text to clipboard.
        
        Args:
            text (str): Text to copy to clipboard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            ConfigManager.console_print(f"Text copied to clipboard ({len(text)} characters)")
            self.clipboardStatusSignal.emit(True, "Text copied to clipboard")
            return True
        except Exception as e:
            error_msg = f"Failed to copy to clipboard: {str(e)}"
            ConfigManager.console_print(error_msg)
            traceback.print_exc()
            self.clipboardStatusSignal.emit(False, error_msg)
            return False
    
    def save_to_file(self, text):
        """
        Save text to file based on configuration settings.
        
        Args:
            text (str): Text to save to file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            output_options = ConfigManager.get_config_section('output_options')
            file_path = output_options.get('output_file_path', os.path.join('output', 'transcriptions.txt'))
            mode = output_options.get('file_output_mode', 'append')
            add_timestamp = output_options.get('add_timestamp', True)
            create_directory = output_options.get('create_directory', True)
            
            # Create directory if it doesn't exist and option is enabled
            directory = os.path.dirname(file_path)
            if directory and create_directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # Prepare content with timestamp if enabled
            content = text
            if add_timestamp:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = f"[{timestamp}] {text}"
                
            # Determine write mode
            write_mode = 'a' if mode == 'append' else 'w'
            
            # Write to file
            with open(file_path, write_mode, encoding='utf-8') as f:
                # Add newline if appending and file is not empty
                if mode == 'append' and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    f.write('\n')
                f.write(content)
                
            success_msg = f"Text saved to {file_path} (mode: {mode})"
            ConfigManager.console_print(success_msg)
            self.fileStatusSignal.emit(True, success_msg)
            return True
            
        except Exception as e:
            error_msg = f"Failed to save to file: {str(e)}"
            ConfigManager.console_print(error_msg)
            traceback.print_exc()
            self.fileStatusSignal.emit(False, error_msg)
            return False

