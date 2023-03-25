import os
from base64 import b64decode

def main():
    id = os.environ.get('AWS_ACCESS_KEY_ID')
    print(b64decode(id).decode())
    key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    print(b64decode(key).decode())
    print(None)
    print(None)

if __name__ == '__main__':
    main()