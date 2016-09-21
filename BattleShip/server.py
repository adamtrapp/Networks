import requests
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import parse_headers

ownBoard = [['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '']]

oppBoard = [['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '']]
carrier = 5
battleship = 4
cruiser = 3
submarine = 3
destroyer = 2

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
            message = "<h1>Your Board</h1>\n<table>\n"
            self.wfile.write(message.encode('utf-8'))
            for row in ownBoard:
                row_string = ""
                for character in row:
                    row_string = row_string + "<td>" + character + "</td>\n "
                row_string = "<tr>\n" + row_string + "</tr>\n"
                self.wfile.write(row_string.encode('utf-8'))
            table_close = "</table>"
            self.wfile.write(table_close.encode('utf-8'))
            stats = "<p>Hits Left:</p>\n <p>Carrier: " + str(carrier) + "</p>\n<p>Battleship: " + str(battleship) + "</p>\n<p>Cruiser: " + str(cruiser) + "" \
            "</p>\n<p>Submarine: " + str(submarine) + "</p>\n<p>Destroyer: " + str(destroyer) + "</p>"
            self.wfile.write(stats.encode('utf-8'))
            url = self.path
            print(url)
        elif url=="/opponent_board.html":
            message = "<h1>Opponent's Board</h1>\n<table>\n"
            self.wfile.write(message.encode('utf-8'))
            loadOppBoard()
            for row in oppBoard:
                row_string = ""
                for character in row:
                    row_string = row_string + "<td>" + character + "</td>\n "
                row_string = "<tr>\n" + row_string + "</tr>\n"
                self.wfile.write(row_string.encode('utf-8'))
            table_close = "</table>"
            self.wfile.write(table_close.encode('utf-8'))
            url = self.path
            print(url)
        else:
            message = "<h1>Oops!</h1>"
            self.wfile.write(message.encode('utf-8'))
            url = self.path
            print(url)
        return

    def do_POST(self):
        global ownBoard
        sunk = 0
        content_len = int(self.headers.get('Content-Length'))
        post_body = str(self.rfile.read(content_len))
        payload = post_body.replace("'", "-").split('-', 2)
        coordinate_string = payload[1]
        values = coordinate_string.replace("&", "=").split('=')
        x = int(values[1])
        y = int(values[3])
        if x >= 10 or x < 0 or y >= 10 or y < 0:
            self.send_response(404)
            self.send_header('Connection', 'close')
            self.end_headers()
        elif values[0] != "x" or values[2] != "y":
            self.send_response(400)
            self.send_header('Connection', 'close')
            self.end_headers()
        else:
            target = ownBoard[x][y]
            if target == "C":
                ownBoard[x][y] = "X"
                global carrier
                carrier -= 1
                if carrier == 0:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1&sunk=C"
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1"
                    self.wfile.write(msg.encode('utf-8'))
            elif target == "B":
                ownBoard[x][y] = "X"
                global battleship
                battleship -= 1
                if battleship == 0:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1&sunk=B"
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1"
                    self.wfile.write(msg.encode('utf-8'))
            elif target == "R":
                ownBoard[x][y] = "X"
                global cruiser
                cruiser -= 1
                if cruiser == 0:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1&sunk=R"
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1"
                    self.wfile.write(msg.encode('utf-8'))
            elif target == "S":
                ownBoard[x][y] = "X"
                global submarine
                submarine -= 1
                if submarine == 0:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1&sunk=S"
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1"
                    self.wfile.write(msg.encode('utf-8'))
            elif target == "S":
                ownBoard[x][y] = "X"
                global destroyer
                destroyer -= 1
                if destroyer == 0:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1&sunk=D"
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    msg = "hit=1"
                    self.wfile.write(msg.encode('utf-8'))
            elif target == "X":
                    self.send_response(410)
                    self.send_header('Connection', 'close')
                    self.end_headers()
            else:
                ownBoard[x][y] = "X"
                self.send_response(200)
                self.send_header('Connection', 'close')
                self.end_headers()
                msg = "hit=0"
                self.wfile.write(msg.encode('utf-8'))
        print(post_body)
        print(values)
        return

PORT_NUMBER = int(sys.argv[1])


def setupGame():
    loadOwnBoard()
    clearOppBoard()


def clearOppBoard():
    with open("opponent_board.txt", 'r+') as textFile:
        textFile.truncate()
        textFile.close()
    with open("opponent_board.txt", 'w') as textFile:
        for row in oppBoard:
            for yc in oppBoard[0]:
                textFile.write("_")
            textFile.write("\n")
        textFile.close()


def loadOwnBoard():
    global ownBoard
    x = 0
    y = 0
    with open(sys.argv[2], 'r+') as textFile:
        n = 1
        textFile.seek(0)
        line = textFile.readline()
        while line is not None and x < len(ownBoard):
            for character in line:
                if y < len(ownBoard[x]):
                    ownBoard[x][y] = character
                    y += 1
            y = 0
            line = textFile.readline()
            x += 1
    textFile.close()

def loadOppBoard():
    global oppBoard
    x = 0
    y = 0
    with open("opponent_board.txt", 'r+') as textFile:
        n = 1
        textFile.seek(0)
        line = textFile.readline()
        while line is not None and x < len(oppBoard):
            for character in line:
                if y < len(oppBoard[x]):
                    oppBoard[x][y] = character
                    y += 1
            y = 0
            line = textFile.readline()
            x += 1
        while line is not "":
            line = textFile.readline()
    textFile.close()


try:
    setupGame()
    server = HTTPServer(('', PORT_NUMBER), boardHandler)
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()