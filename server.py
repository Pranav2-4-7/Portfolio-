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

    def log_message(self, format, *args):
        print(f"[SERVER] {self.address_string()} - {format % args}")

PORT = 8080
with socketserver.TCPServer(('', PORT), NoCacheHandler) as httpd:
    print(f"[SERVER] Serving on http://localhost:{PORT}")
    httpd.serve_forever()
