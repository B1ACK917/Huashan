from utils.uploader import Akira

if __name__ == '__main__':
    token = "<token>"
    cookie = "<cookie>"
    akira = Akira(token, cookie)
    akira.upload("sample.txt")
