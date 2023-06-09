import http.server
import socketserver


def start_http_server(port, directory):
    # Create a request handler class by subclassing SimpleHTTPRequestHandler
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        # You can customize the behavior of the server by overriding methods here
        pass

    # Create a TCP server instance with the specified port and request handler
    with socketserver.TCPServer(("", port), RequestHandler) as httpd:
        print(f"Server running on port {port}. Press Ctrl+C to stop.")
        # Start the server
        httpd.serve_forever()
