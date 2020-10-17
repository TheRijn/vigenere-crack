import sys
from argparse import ArgumentParser


def encrypt(plaintext, keyword, outputfile):
    if not keyword.isalpha():
        print("invalid keyword")
        exit(1)

    index = 0

    for c in plaintext:

        if c.isalpha():
            key = ord(keyword[index].upper()) - ord('A')
            if c.isupper():
                print(chr((ord(c) - ord('A') + key) % 26 + ord('A')), end="")
            else:
                print(chr((ord(c) - ord('a') + key) % 26 + ord('a')), end="")

            index = (index + 1) % len(keyword)
        else:
            print(c, end="")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("plaintext")
    parser.add_argument("keyword")
    parser.add_argument("-o","--output", help="Output file", default=None)
    args = parser.parse_args()

    with open(args.plaintext, "r") as f:
        plaintext = f.read()

    encrypt(plaintext, args.keyword, args.output)