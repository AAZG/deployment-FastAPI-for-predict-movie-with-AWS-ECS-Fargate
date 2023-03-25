import os

def main():
    region = os.environ.get('AWS_REGION')
    print(region)

if __name__ == '__main__':
    main()