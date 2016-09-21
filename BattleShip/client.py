import sys
import requests
import re

board = [['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '']]
x = int
y = int


def main():
    global x
    global y
    loadfile()
    ipadress = sys.argv[1]
    port = sys.argv[2]
    x = sys.argv[3]
    y = sys.argv[4]
    url = "http://" + ipadress + ':' + port
    payload = "x=" + x + "&y=" + y
    print("\nSending ", payload, " to IP Address ", url, ".\n")

    r = requests.post(url, data=payload)
    if r.reason == "OK":
        print("Location Successful! Server returned POST Reason \"OK\"")
        print(r.text)
        hit(r.text)
    if r.reason == 'Not Found':
        print("Out of bounds! Server returned POST Reason \"Not Found\"")
    if r.reason == "Gone":
        print("Already fired upon! Server returned POST Reason \"Gone\"")
    if r.reason == "Bad Request":
        print("Message Not Formatted Correctly! Server returned POST Reason \"Bad Request\"")


def hit(binaryinput):
    global x
    global y
    global board
    xint = int(x)
    yint = int(y)
    hit = int(re.search(r'\d+', binaryinput).group())

    if hit == 1:
        board[xint][yint] = 'X'
    if hit == 0:
        board[xint][yint] = '~'
    if 'sink' in binaryinput:
        print("You sunk " + binaryinput[-1] + "!")
    closefile()


def loadfile():
    global board
    x = 0
    y = 0
    with open("opponent_board.txt", 'r+') as textFile:
        n = 1
        textFile.seek(0)
        line = textFile.readline()
        while line is not None and x < len(board):
            for character in line:
                if y < len(board[x]):
                    board[x][y] = character
                    y += 1
            y = 0
            line = textFile.readline()
            x += 1
    textFile.close()


def closefile():
    global board
    with open("opponent_board.txt", 'r+') as textFile:
        textFile.truncate()
        textFile.close()
    with open("opponent_board.txt", 'w') as textFile:
        for row in board:
            for yc in row:
                textFile.write(yc)
            textFile.write("\n")
        textFile.close()


main()
