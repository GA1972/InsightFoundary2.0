#!/usr/bin/env python3
"""
Insight Foundry Download Server
Simple HTTP server for downloading project files
"""

import os
import http.server
import socketserver
import webbrowser
import threading
import time
from datetime import datetime

# Configuration
PORT = 9000
WORKSPACE_DIR = '/project/workspace'

class DownloadHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_DIR, **kwargs)
    
    def end_headers(self):
        # Add download headers for archive files
        if self.path.endswith(('.zip', '.tar.gz', '.tar', '.gz')):
            filename = os.path.basename(self.path)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/download':
            self.serve_download_page()
        else:
            super().do_GET()
    
    def serve_download_page(self):
        """Serve the download center HTML page"""
        try:
            with open(os.path.join(WORKSPACE_DIR, 'download-center.html'), 'r') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            # Generate a simple download page if the HTML file doesn't exist
            self.generate_download_page()
    
    def generate_download_page(self):
        """Generate a simple download page listing available files"""
        
        # Get available download files
        download_files = []
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            for file in files:
                if file.endswith(('.zip', '.tar.gz', '.pdf', '.md')) and not '/node_modules/' in root:
                    rel_path = os.path.relpath(os.path.join(root, file), WORKSPACE_DIR)
                    file_size = os.path.getsize(os.path.join(root, file))
                    download_files.append({
                        'name': file,
                        'path': rel_path.replace(os.sep, '/'),
                        'size': self.format_file_size(file_size),
                        'type': self.get_file_type(file)
                    })
        
        # Sort files by type and name
        download_files.sort(key=lambda x: (x['type'], x['name']))
        
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insight Foundry - Download Center</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1rem;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #6c757d;
            font-size: 0.9rem;
        }}
        
        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .file-card {{
            background: white;
            border: 2px solid #f0f0f0;
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .file-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }}
        
        .file-type {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            text-transform: uppercase;
        }}
        
        .file-icon {{
            font-size: 3rem;
            margin-bottom: 15px;
            display: block;
        }}
        
        .file-name {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            word-break: break-word;
        }}
        
        .file-size {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }}
        
        .download-btn {{
            width: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }}
        
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
            color: #666;
        }}
        
        .server-info {{
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .server-info strong {{
            color: #1565c0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📥 Insight Foundry Download Center</h1>
            <p>Access your project files and documentation</p>
        </div>
        
        <div class="server-info">
            <strong>🚀 Server Running:</strong> http://localhost:{PORT} | <strong>📅 Started:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len([f for f in download_files if f['type'] == 'Archive'])}</div>
                <div class="stat-label">Archive Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([f for f in download_files if f['type'] == 'Document'])}</div>
                <div class="stat-label">Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(download_files)}</div>
                <div class="stat-label">Total Files</div>
            </div>
        </div>
        
        <div class="files-grid">
        '''
        
        # Add file cards
        for file_info in download_files:
            icon = self.get_file_icon(file_info['type'])
            html_content += f'''
            <div class="file-card">
                <span class="file-type">{file_info['type']}</span>
                <div class="file-icon">{icon}</div>
                <div class="file-name">{file_info['name']}</div>
                <div class="file-size">{file_info['size']}</div>
                <a href="/{file_info['path']}" class="download-btn" download>
                    📥 Download
                </a>
            </div>
            '''
        
        if not download_files:
            html_content += '''
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 20px;">📂</div>
                <h3>No download files available</h3>
                <p>Check back later for project archives and documentation.</p>
            </div>
            '''
        
        html_content += '''
        </div>
        
        <div class="footer">
            <p>🤖 <strong>Insight Foundry</strong> - AI-Powered Research Analysis Platform</p>
            <p>Generated at {}</p>
        </div>
    </div>
</body>
</html>
        '''.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def get_file_type(filename):
        """Get file type for categorization"""
        if filename.endswith(('.zip', '.tar.gz', '.tar')):
            return 'Archive'
        elif filename.endswith(('.pdf', '.md', '.txt')):
            return 'Document'
        else:
            return 'Other'
    
    @staticmethod
    def get_file_icon(file_type):
        """Get emoji icon for file type"""
        icons = {
            'Archive': '📦',
            'Document': '📄',
            'Other': '📎'
        }
        return icons.get(file_type, '📎')

def start_server():
    """Start the download server"""
    try:
        os.chdir(WORKSPACE_DIR)
        
        with socketserver.TCPServer(("", PORT), DownloadHandler) as httpd:
            print(f"🚀 Download server starting...")
            print(f"📁 Serving files from: {WORKSPACE_DIR}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📥 Download center: http://localhost:{PORT}/download")
            print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"")
            print(f"🔗 Available endpoints:")
            print(f"   • http://localhost:{PORT} - Download center")
            print(f"   • http://localhost:{PORT}/download - Download center")
            print(f"   • http://localhost:{PORT}/<filename> - Direct file download")
            print(f"")
            print(f"📦 Available files:")
            
            # List available download files
            download_count = 0
            for root, dirs, files in os.walk(WORKSPACE_DIR):
                for file in files:
                    if file.endswith(('.zip', '.tar.gz', '.pdf', '.md')) and not '/node_modules/' in root:
                        rel_path = os.path.relpath(os.path.join(root, file), WORKSPACE_DIR)
                        file_size = os.path.getsize(os.path.join(root, file))
                        print(f"   • {file} ({DownloadHandler.format_file_size(file_size)})")
                        download_count += 1
            
            if download_count == 0:
                print(f"   • No download files available")
            
            print(f"")
            print(f"🛑 Press Ctrl+C to stop the server")
            print(f"{'='*60}")
            
            # Auto-open browser after a short delay
            def open_browser():
                time.sleep(2)
                try:
                    webbrowser.open(f'http://localhost:{PORT}/download')
                    print(f"🌐 Opened download center in your default browser")
                except:
                    pass
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print(f"💡 Try using a different port or stop the existing server")
            print(f"🔍 To find what's using the port: sudo lsof -i :{PORT}")
        else:
            print(f"❌ Error starting server: {e}")
    except KeyboardInterrupt:
        print(f"\\n🛑 Download server stopped by user")
        print(f"👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_server()