#!/usr/bin/env python3
"""HTTP server with no-cache headers for development"""
import http.server
import socketserver

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(post_data.decode('utf-8') + '\n')
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        print(f"[SERVER] {self.address_string()} - {format % args}")

PORT = 3000
with socketserver.TCPServer(('', PORT), NoCacheHandler) as httpd:
    print(f"[SERVER] Serving on http://localhost:{PORT}")
    httpd.serve_forever()
