#!/usr/bin/env python3
"""
Android Project Rebuilder - Standalone macOS Application
Main entry point for PyWebView-based standalone app
"""

import webview
import os
import sys
import base64
import tempfile
from pathlib import Path
from backend.processor import AndroidProjectProcessor


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class API:
    """Python API exposed to JavaScript"""

    def __init__(self):
        self.window = None
        self.processor = None
        self.temp_files = {}  # Store temporary file paths

    def set_window(self, window):
        """Set the window reference for callbacks"""
        self.window = window

    def select_zip_file(self):
        """Open file dialog to select ZIP file"""
        try:
            file_types = ('ZIP Files (*.zip)',)
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                allow_multiple=False,
                file_types=file_types
            )
            if result and len(result) > 0:
                return {'success': True, 'path': result[0]}
            return {'success': False, 'error': 'No file selected'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def select_json_file(self):
        """Open file dialog to select google-services.json file"""
        try:
            file_types = ('JSON Files (*.json)',)
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                allow_multiple=False,
                file_types=file_types
            )
            if result and len(result) > 0:
                return {'success': True, 'path': result[0]}
            return {'success': False, 'error': 'No file selected'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def select_image_file(self, dialog_title='Select Image'):
        """Open file dialog to select image file"""
        try:
            file_types = ('Image Files (*.png;*.jpg;*.jpeg)',)
            result = self.window.create_file_dialog(
                webview.OPEN_DIALOG,
                allow_multiple=False,
                file_types=file_types
            )
            if result and len(result) > 0:
                return {'success': True, 'path': result[0]}
            return {'success': False, 'error': 'No file selected'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def save_file_dialog(self, default_filename='rebuilt_project.zip'):
        """Open save file dialog"""
        try:
            result = self.window.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=default_filename
            )
            if result:
                return {'success': True, 'path': result}
            return {'success': False, 'error': 'No location selected'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def process_project(
        self,
        zip_path,
        new_package,
        new_app_name,
        google_services_path=None,
        icon_path=None,
        splash_path=None,
        new_base_url=None,
        include_log=True
    ):
        """
        Process Android project with given parameters

        Returns:
            {
                'success': bool,
                'output_zip': str,  # Path to output ZIP
                'logs': List[str],
                'error': str (optional)
            }
        """
        try:
            # Initialize processor
            self.processor = AndroidProjectProcessor()

            # Run processing
            result = self.processor.process(
                zip_path=zip_path,
                new_package=new_package,
                new_app_name=new_app_name,
                google_services_path=google_services_path,
                icon_path=icon_path,
                splash_path=splash_path,
                new_base_url=new_base_url,
                include_log=include_log
            )

            return result

        except Exception as e:
            return {
                'success': False,
                'output_zip': None,
                'logs': [f'[ERROR] Processing failed: {str(e)}'],
                'error': str(e)
            }

    def cleanup_processor(self):
        """Clean up processor temporary files"""
        try:
            if self.processor:
                self.processor.cleanup()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_file_as_base64(self, file_path):
        """Read file and return as base64 for download"""
        try:
            with open(file_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
            return {'success': True, 'content': content}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def copy_file(self, source_path, destination_path):
        """Copy file from source to destination"""
        try:
            import shutil
            shutil.copy2(source_path, destination_path)
            return {'success': True, 'message': f'File saved to {destination_path}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_message(self):
        """Test API method"""
        return "Android Project Rebuilder - Ready!"


def main():
    """Main application entry point"""
    # Initialize API
    api = API()

    # Get HTML file path
    html_path = get_resource_path('frontend/index_standalone.html')

    # Check if HTML file exists
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        sys.exit(1)

    # Create window
    window = webview.create_window(
        'Android Project Rebuilder',
        html_path,
        js_api=api,
        width=1200,
        height=900,
        resizable=True,
        frameless=False,
        min_size=(800, 600)
    )

    # Set window reference in API
    api.set_window(window)

    # Start the application
    webview.start(debug=True)


if __name__ == '__main__':
    main()
