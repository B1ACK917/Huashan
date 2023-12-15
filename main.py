from utils.uploader import Akira
import argparse

parser = argparse.ArgumentParser(description="Akira parser")
parser.add_argument("-f", "--file", type=str, help='Path to file')

if __name__ == '__main__':
    token = "<token>"
    cookie = "<cookie>"
    akira = Akira(token, cookie)

    args = parser.parse_args()
    akira.upload("sample.txt")
    akira.upload(args.file)
