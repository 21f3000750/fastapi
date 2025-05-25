# api/index.py
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        requested_names = query_params.get('name', [])
        
        marks_data = []
        # Construct the full path to q-vercel-python.json
        # This is important for Vercel's build environment
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, '..', 'q-vercel-python.json') # Go up one level to find q-vercel-python.json
        
        try:
            with open(json_path, 'r') as f:
                marks_data = json.load(f)
        except FileNotFoundError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "q-vercel-python.json not found"}).encode())
            return

        response_marks = []
        name_to_marks = {item['name']: item['marks'] for item in marks_data}

        for name in requested_names:
            response_marks.append(name_to_marks.get(name, None)) # Use .get to handle names not found

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"marks": response_marks}).encode())
