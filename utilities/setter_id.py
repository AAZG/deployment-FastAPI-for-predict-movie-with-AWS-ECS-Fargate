import os
from base64 import b64decode

def main():
    key = os.environ.get('AWS_ACCESS_KEY_ID')
    print(b64decode(key).decode())

if __name__ == '__main__':
    main()