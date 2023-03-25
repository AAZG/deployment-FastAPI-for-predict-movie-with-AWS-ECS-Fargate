import os

def main():
    region = os.environ.get('AWS_REGION')
    return region

if __name__ == '__main__':
    main()