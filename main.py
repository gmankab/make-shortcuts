import os
from sys import stdout
print(stdout.encoding)

path = r'D:\dev\test'

def ls(path):  # my listdir(), called like in linux
    if not os.path.isdir(path):
        print(f'{path} is not a dir')
        return

    dir = path.split('/')[-1]

    if dir in [
        'System Volume Information',
        '$RECYCLE.BIN',
        '.git',  
    ]:
        print(f'{path} in blacklist')
        return

    return list(os.listdir( path))

print('aboba')
def mklink(path):
    print(path) 

def main():
    for dir in ls(path):
        for file in ls('\\'.join([path, dir])):
            if file[:-4] == '.exe':
                mklink(file)
            elif file[:-5] == '.link':
                mklink(file)
