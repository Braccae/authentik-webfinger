
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class WebFingerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/.well-known/webfinger'):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            if 'resource' in query_params:
                resource = query_params['resource'][0]
                
                if resource.startswith('acct:'):
                    email = resource[5:]
                    issuer_url = "https://auth.example.com/application/o/tailscale/"
                    response_data = {
                        "subject": resource,
                        "links": [
                            {
                                "rel": "http://openid.net/specs/connect/1.0/issuer",
                                "href": issuer_url
                            },
                            {
                                "rel": "authorization_endpoint",
                                "href": issuer_url + "oauth2/authorize"
                            },
                            {
                                "rel": "token_endpoint",
                                "href": issuer_url + "oauth2/token"
                            },
                            {
                                "rel": "userinfo_endpoint",
                                "href": issuer_url + "userinfo"
                            },
                            {
                                "rel": "jwks_uri",
                                "href": issuer_url + "jwks"
                            }
                        ]
                    }
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode())
                    return
            
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Resource not found")

def run_server(server_class=HTTPServer, handler_class=WebFingerHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting WebFinger server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()


