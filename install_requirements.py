import sys
from run_command import run


def update_pip():
    output = run(f'{sys.executable} -m pip install --upgrade pip', printing=False)
    if output[:30] != 'Requirement already satisfied:':
        print(output)

def main():
    update_pip()

    for package in open('requirements.txt').readlines():
        package = package.replace('\n', '')
        try:
            __import__(package)
        except ImportError:
            run(f'{sys.executable} -m pip install {package}')

# main()