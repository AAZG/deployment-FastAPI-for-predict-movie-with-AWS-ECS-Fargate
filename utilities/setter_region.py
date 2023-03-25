import os

def main():
    role = os.environ.get('AWS_IAM_ROLE')
    return role

if __name__ == '__main__':
    main()