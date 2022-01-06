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

from inspect import cleandoc
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


check_python_vers('3.10.1')


def install(module):
    def install_(module_):
        print(f'installing {module_}:')
        os.system(f'{sys.executable} -m pip install {module_ }')

    try:
        match type(module).__name__:
            case 'str':
                __import__(module)
            case 'list':
                __import__(module[0])
            case _:
                raise TypeError(
                    type_error_message(
                        expected=(str, list),
                        get=type(module).__name__
                    )
                )

    except ImportError:
        match type(module[1]).__name__:
            case 'str':
                install_(module[1])
            case 'list':
                for i in module[1]:
                    install(i)
            case _:
                raise TypeError(
                    type_error_message(
                        expected=(str, list),
                        get=type(module).__name__
                    )
                )


for module in [
    'forbiddenfruit',
    ['yaml', 'pyyaml'],
]:
    install(module)


from forbiddenfruit import curse
import yaml


def conc(self, *args):  # universal analog of ".join()"
    to_join = []
    for arg in args:
        if isinstance(arg, list):
            to_join += list(str(i) for i in arg)
        else:
            to_join.append(str(arg))
    return self.join(to_join)


curse(str, 'bdj', conc)


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
        for arg in args:
            while arg[0] == '\\':
                arg = arg[1:]
            while arg[-1] == '\\':
                arg = arg[:-1]
        self.str = '\\'.conc(args)

    def __repr__(self):
        return self.str


a = Path('aboba')

print(a)


def run(command, printing: bool = True):
    command_type = type(command).__name__
    match command_type:
        case 'str':
            pass
        case 'list':
            command = ' '.join(command)
        case _:
            raise TypeError(
                cleandoc(
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


def list_subtract(list_, blacklist):
    for i in blacklist:
        if i in list_:
            list_.remove(i)
    return list_


def isends(file, ext):
    return file[-len(ext):] == ext


# def conc(a, b):
#     if a[-1] == "\\":
#         a = a[:-1]
#     return '\\'.join([a, b])


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
    return cleandoc(
        f'''
        expected types:
            {', '.join(expected)}
        get:
            {get}
        '''
    )
