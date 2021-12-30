import install_requirements
import os, ctypes, sys, shutil, stat


def ls(path):  # my listdir(), called like in linux
    if not os.path.isdir(path):
        return []

    dir_ = path.rsplit('\\', 1)[-1]

    if dir_ in [
        'System Volume Information',
        '$RECYCLE.BIN',
        'downloads'
        '.git',
    ]:
        return []

    return list(os.listdir( path))

def mklink(path):
    print(path)

def conc(a, b):
    if a[-1] == "\\":
        a = a[:-1]
    return '\\'.join([a, b])


def rmdir(path):
    dirlist=os.listdir(path)
    for f in dirlist:
        fullname=os.path.join(path,f)
        if fullname == os.path.join(path,"thrash.txt"):
            os.chmod(fullname , stat.S_IWRITE)
            os.remove(fullname)
        if os.path.isdir(fullname):
            rmdir(fullname)


def main():
    path = 'D:\\'
    rmdir(conc(path, 'links'))
    for dir1 in ls(path):
        dir2 = conc(path, dir1)
        for file in ls(dir2):
            file = conc(dir2, file)
            if file.rsplit('.', 1)[-1] == 'exe':
                print(file)

main()
