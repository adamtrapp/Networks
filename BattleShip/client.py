import sys
import requests
import re

board = None
x = None
y = None


def main():
    ipadress = sys.argv[1]
    port = sys.argv[2]
    x = sys.argv[3]
    y = sys.argv[4]
    url = ipadress + ':' + port
    payload = {'x': x, 'y': y}
    print("\nSending ", payload, " to IP Address ", url, ".\n")

    r = requests.post(url, data=payload)
    if r.reason == "OK":
        hit(r.text)
    if r.reason == 'Not Found':
        print("Out of bounds! Server returned POST Reason \"Not Found\"")
    if r.reason == "Gone":
        print("Already fired upon! Server returned POST Reason \"Gone\"")
    if r.reason == "Bad Request":
        print("Message Not Formatted Correctly! Server returned POST Reason \"Bad Request\"")


def hit(binaryinput):
    payload = int(binaryinput)
    hit = int(re.search(r'\d+', binaryinput).group())
    loadfile()
    if hit == 1:
        board[x][y] = 'X'
    if hit == 2:
        board[x][y] = '~'
    closefile


def loadfile():
    with open("opponent_board.txt") as textFile:
        read = textFile.read()
        empty_check = textFile.read(1)
        if not empty_check:
            for x in range(0, 9):
                for y in range(0, 9):
                    board[x][y] = '_'
        else:
            n = 1
            textFile.seek(0)
            for x in range(0, 9):
                for y in range(0, 9):
                    board[x][y] = textFile.read(n)
                    n += 1


def closefile():
    with open("opponent_board.txt", 'w') as textFile:
        for x in range(0, 9):
            for y in range(0, 9):
                textFile.write(board[x][y])
            textFile.write("\n")


main()
