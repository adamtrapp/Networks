import sys


def main():
    ipadress = sys.argv[1]
    port = sys.argv[2]
    x = sys.argv[3]
    y = sys.argv[4]
    print("\nSending (", x, ",", y, ") to IP Address ", ipadress, " using port ", port, ".\n")


main()
