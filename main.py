from utils.uploader import Tuploader
from utils.login import get_cloud_session
from Shinomiya.Src.logger import *
import argparse

parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("-f", "--file", type=str, help='Path to file')
parser.add_argument("-t", "--token", type=str, help='Token')
parser.add_argument("-p", "--passwd", type=str, help='Password')
parser.add_argument("-c", "--cookies", type=str, help='Cookies')

if __name__ == '__main__':
    args = parser.parse_args()
    
    iprint(f"Token: {args.token}, Password: {args.passwd}, File: {args.file}")
    akira = Tuploader()
    
    # use token & cookie
    # akira.set(args.token, args.cookies)
    
    # or token & passwd
    akira.login(args.token, args.passwd)
    
    akira.upload(args.file)
