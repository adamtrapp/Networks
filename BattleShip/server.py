import requests
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer

board = [['C', 'C', 'C', 'C', 'C', '_', '_', '_', '_', '_'],
         ['B', 'B', 'B', 'B', '_', '_', '_', '_', '_', '_'],
         ['R', 'R', 'R', '_', '_', '_', '_', '_', '_', '_'],
         ['S', 'S', 'S', '_', '_', '_', '_', '_', '_', '_'],
         ['D', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
         ['D', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']]






# This class will handles any incoming request from
# the browser
class boardHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        url = self.path
        if url=="/own_board.html":
            message = "<h1>Your Board</h1>"
            self.wfile.write(message.encode('utf-8'))
            for row in board:
                row_string = ""
                for character in row:
                    row_string = row_string + character + " "
                row_string = "<h3>" + row_string + "</h3>"
                self.wfile.write(row_string.encode('utf-8'))

            url = self.path
            print(url)
        elif url=="/opponent_board.html":
            message = "<h1>Opponent Board</h1>"
            self.wfile.write(message.encode('utf-8'))
            for row in board:
                row_string = ""
                for character in row:
                    row_string = row_string + character + " "
                row_string = "<h3>" + row_string + "</h3>"
                self.wfile.write(row_string.encode('utf-8'))

            url = self.path
            print(url)
        else:
            message = "<h1>Oops!</h1>"
            self.wfile.write(message.encode('utf-8'))
            url = self.path
            print(url)
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print(post_body)
        return

PORT_NUMBER = int(sys.argv[1])

try:
    server = HTTPServer(('', PORT_NUMBER), boardHandler)
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()


