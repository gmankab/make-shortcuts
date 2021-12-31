import install_requirements
import blacklist
from run_command import run
import shutil
import ctypes
import stat
import sys
import os
from win32com.client import Dispatch
from dataclasses import dataclass
import pathlib


@dataclass
class Lnk:
    path = ""

def ls(path):  # my listdir(), called like in linux
    if not os.path.isdir(path):
        if isends(path, '.exe'):
            mklnk(Lnk.path, path)
        return []

    answer = list(os.listdir(path))

    for i in blacklist.rirs:
        if i in answer:
            answer.remove(i)
    return answer


def isends(file, ext):
    return file[-len(ext):] == ext

def mklnk(save_to, target):
    if not isends (save_to, '.lnk'):
        save_to = conc(save_to, target.rsplit('\\', 1)[-1].replace('.exe', '.lnk'))

    shortcut = Dispatch('WScript.Shell').CreateShortCut(save_to)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = rf'{target}\..'
    shortcut.save()

def conc(a, b):
    if a[-1] == "\\":
        a = a[:-1]
    return '\\'.join([a, b])


def rmdir(path):
    run(f'RMDIR "{path}" /S /Q')

def main():
    path = 'D:\\'
    Lnk.path = conc(path, 'links')
    rmdir(Lnk.path)
    os.mkdir(Lnk.path)
    for dir1 in ls(path):
        dir2 = conc(path, dir1)
        for dir3 in ls(dir2):
            dir3 = conc(dir2, dir3)
            for dir4 in ls(dir3):
                dir4 = conc(dir3, dir4)
                ls(dir4)


main()
