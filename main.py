import install_requirements
from run_command import run
import betterdata
import blacklist
import os
from win32com.client import Dispatch
from dataclasses import dataclass



def rmext(path:str):
    return path.rsplit('.', 1)[0]


def ls(path, lnk_path):  # my listdir(), called like in linux
    if not os.path.isdir(path):
        if isends(path, '.exe'):
            mklnk(lnk_path, path)
        return []

    last_2_dirs = path.rsplit('\\', 2)[1:]
    if 'python' in last_2_dirs[0].lower() and last_2_dirs[1] == 'App':
        mklnk(lnk_path, conc(path, r'Python\python.exe'))

    return betterdata.list_subtract(
        list(os.listdir(path)),
        blacklist.dirs,
    )



def mklnk(save_to, target):
    if not isends (save_to, '.lnk'):
        save_to = conc(save_to, name(target).replace('.exe', '.lnk'))

    shortcut = Dispatch('WScript.Shell').CreateShortCut(save_to)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = rf'{target}\..'
    shortcut.save()


def main():
    path = 'D:\\'
    lnk_path = conc(path, 'links')
    rmdir(lnk_path)
    os.mkdir(lnk_path)
    for dir1 in ls(path, lnk_path):
        dir2 = conc(path, dir1)
        for dir3 in ls(dir2, lnk_path):
            dir3 = conc(dir2, dir3)
            for dir4 in ls(dir3, lnk_path):
                dir4 = conc(dir3, dir4)
                ls(dir4, lnk_path)


main()
