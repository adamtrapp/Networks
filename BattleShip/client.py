import sys
import requests


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


def hit(input):
    payload = int(input)
    #if payload == 1:


main()
