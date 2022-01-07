'''

   oooooooooo.   oooooooooo.       telegram | gmanka
   `888'   `Y8b  `888'   `Y8b       discord | gmanka#3806
    888     888   888      888       github | gmankab/betterdata
    888oooo888'   888      888       donate | 5536 9139 9403 2981
    888    `88b   888      888       python | 3.10.1
    888    .88P   888     d88'       vscode | 1.61.2
   o888bood8P'   o888bood8P'     betterdata | 22.0

'''

python_vers = '3.10.1'

from dataclasses import dataclass
from inspect import cleandoc as cd
from pprint import pp
import pickle
import sys
import os

# noqa: E731
# noqa: F821
# pyright: reportUndefinedVariable=false
# pyright: reportMissingImports=false
# pylint: disable=import-outside-toplevel
# pylint: disable=import-error


def check_python_vers(required_vers):
    if '.'.join(str(i) for i in sys.version_info) < required_vers:
        raise VersionError(
            f'Python version must be at least {required_vers}'
        )


check_python_vers(python_vers)


def to_list(*args, convert=None):
    '''
    make list of str from anything
    '''

    @dataclass
    class Answer:
        list = []

    def recursive_add_str(whatever):
        if isinstance(whatever, (list, tuple)):
            for i in whatever:
                recursive_add_str(i)
        else:
            if convert:
                whatever = convert(whatever)
            Answer.list.append(whatever)

    for arg in args:
        recursive_add_str(arg)

    return Answer.list


def install_if_missing(module):
    def pip_install(module_):
        print(f'installing {module_}:')
        os.system(f'{sys.executable} -m pip install {module_ }')

    module = to_list(module, convert=str)
    try:
        __import__(module[0])
    except ImportError:
        if len(module) == 1:
            pip_install(module[0])
        else:
            for i in module[1:]:
                pip_install(i)


for module in [
    'forbiddenfruit',
    ['yaml', 'pyyaml'],
]:
    install_if_missing(module)


from forbiddenfruit import curse
import yaml


def modify_builtin_functions():
    def str_conc(self, *peaces):  # universal analog of ".join()"
        return self.join(to_list(peaces, convert=str))

    def str_rmborders(self, *borders):
        for border in to_list(borders):
            while self[:len(border)] == border:
                self = self[len(border):]
            while self[-len(border):] == '\\':
                self = self[:-len(border)]

    def list_rm(self, *to_remove):
        for i in to_list(to_remove):
            if i in self:
                self.remove(i)
        return self

    for funcname, func in locals().copy().items():
        builtin_funcname, addmethod = funcname.split('_', 1)
        curse(eval(builtin_funcname), addmethod, func)


modify_builtin_functions()


class VersionError(Exception):
    pass


class NameExpectedError(Exception):
    @staticmethod
    def text(data):
        if isinstance(data, dict):
            name = 'dict'
        else:
            name = 'else'
        return open(f'error_messages/{name}.txt').read()


class UnsupportedExtensionError(Exception):
    pass


class Bd:
    """
    @DynamicAttrs
    disabling pycharm "unresolved attribute" warnings
    """
    def __init__(self, data: dict, name: str = None):
        if name:
            data['name'] = name
        for key, val in data.items():
            vars(self)[key] = val

    def to_dict(self, name=True):
        if isinstance(name, str):
            vars(self)['name'] = name
        elif not name:
            vars(self).pop('name', None)
        return vars(self)


class Path:
    def __init__(self, *args):
        args = list(args)
        for arg in args:
            if isinstance(arg, str):
                arg.rmborders('/', '\\')
        self.str = '/'.conc(args)

    def __repr__(self):
        return self.str

    def conc(*peaces):
        for peace in peaces:
            peace.rmborders('\\', '/')
        return '/'.conc()


def run(command, printing: bool = True):
    command_type = type(command).__name__
    match command_type:
        case 'str':
            pass
        case 'list':
            command = ' '.join(command)
        case _:
            raise TypeError(
                cd(
                    f'''
                    expected types of 'command' argument:
                        str, list
                    get:
                        {command_type}
                    '''
                )
            )

    if printing:
        os.system(command)
    else:
        return os.popen(command).read()


def dump(data, name: str = None):
    if not name:
        if isinstance(data, dict):
            if 'name' not in data.keys():
                raise NameExpectedError(NameExpectedError.text(data))
            name = data['name']
        else:
            if 'name' not in vars(data).keys():
                raise NameExpectedError(NameExpectedError.text(data))
            name = data.name
    extension = name.split('.')[-1]
    match extension:
        case 'pickle':
            pickle.dump(data, open(f'data/{name}', 'wb'))
        case 'yml':
            if not isinstance(data, dict):
                data = data.to_dict
            yaml.dump(data, open(f'data/{name}', 'w'))
        case _:
            raise UnsupportedExtensionError(
                "only 'pickle' and 'yml' extensions supported"
            )


def load(name: str, ins: str = 'bd'):  # ins = instance or type
    extension = name.split('.')[-1]
    match extension:
        case 'pickle':
            data = pickle.load(open(f'data/{name}', 'rb'))
            data.name = name
            return data
        case 'yml ':
            data = yaml.load(
                open(f'data/{name}', 'r').read(),
                Loader=yaml.Loader
            )
            data['name'] = name
            match ins.lower():
                case 'dict' | 'dc' | 'dct':
                    return data
                case 'bd' | 'betterdata':
                    return Bd(data)
                case _:
                    raise TypeError("Only 'bd' and 'dct' instances supported")
        case _:
            raise UnsupportedExtensionError(
                "only 'pickle' and 'yml' extensions supported"
            )


def update_pip():
    output = run(
        f'{sys.executable} -m pip install --upgrade pip',
        printing=False
    )
    if output[:30] != 'Requirement already satisfied:':
        print(output)


def isends(file, ext):
    return file[-len(ext):] == ext


def filename(path: str):
    return path.rsplit('\\', 1)[-1]


def rmdir(path: str):
    run(f'RMDIR "{path}" /S /Q')


def rm(string: str, to_remove):
    if isinstance(to_remove, str):
        to_remove = [to_remove]
    for i in to_remove:
        string = string.replace(i, '')
    return string


def typenm(object_):  # type name
    return type(object_).__name__


def type_error_message(expected, get):
    return cd(
        f'''
        expected types:
            {', '.join(expected)}
        get:
            {get}
        '''
    )


path = Path('D')
