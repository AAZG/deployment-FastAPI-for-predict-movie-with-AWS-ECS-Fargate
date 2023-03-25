import os
from base64 import b64decode

def main():
    id = os.environ.get('AWS_ACCESS_KEY_ID')
    print(id)
    print(b64decode(id).decode())

if __name__ == '__main__':
    main()