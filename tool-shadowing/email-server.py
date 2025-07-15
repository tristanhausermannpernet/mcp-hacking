#!/usr/bin/env python3
"""
Tool Shadowing Attack - Server 2 (Email Server)

This server provides a send_email tool that should be influenced by the
malicious instructions from the add_numbers tool in the other server.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import signal
import os

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle MCP JSON-RPC requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(post_data.decode('utf-8'))
            response = self.handle_mcp_request(request)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_mcp_request(self, request):
        """Process MCP JSON-RPC request"""
        method = request.get('method')
        request_id = request.get('id')
        
        if method == 'initialize':
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "tool-shadowing-email",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == 'tools/list':
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "send_email",
                            "description": "Sends an email to the specified recipient with the given subject and message content.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "to": {
                                        "type": "string",
                                        "description": "Email address of the recipient"
                                    },
                                    "subject": {
                                        "type": "string",
                                        "description": "Subject line of the email"
                                    },
                                    "message": {
                                        "type": "string",
                                        "description": "Body content of the email"
                                    }
                                },
                                "required": ["to", "subject", "message"]
                            }
                        }
                    ]
                }
            }
        
        elif method == 'tools/call':
            params = request.get('params', {})
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name == 'send_email':
                return self.execute_send_email(request_id, arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Unknown method: {method}"
            }
        }
    
    def execute_send_email(self, request_id, arguments):
        """Execute the send_email tool (simulated)"""
        try:
            to = arguments.get('to')
            subject = arguments.get('subject')
            message = arguments.get('message')
            
            if not all([to, subject, message]):
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: to, subject, message"
                    }
                }
            
            # Simulate email sending
            print(f"[EMAIL SIMULATION] Email would be sent:")
            print(f"  To: {to}")
            print(f"  Subject: {subject}")
            print(f"  Message: {message}")
            print(f"  ---")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Email sent successfully to {to} with subject '{subject}'"
                        }
                    ]
                }
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nShutting down server...")
    sys.exit(0)

def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    port = 8081
    server_address = ('localhost', port)
    
    httpd = HTTPServer(server_address, MCPHandler)
    
    print(f"Tool Shadowing Attack - Email Server starting on port {port}")
    print(f"Server URL: http://localhost:{port}")
    print("This server provides send_email functionality")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()
