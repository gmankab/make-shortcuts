import sys
from requirements import requirements
from inspect import cleandoc


def update_pip():
    output = run(f'{sys.executable} -m pip install --upgrade pip', printing=False)
    if output[:30] != 'Requirement already satisfied:':
        print(output)

def install_requirements():
    for import_name in requirements:
        match type(import_name).__name__:
            case 'str':
                install_name = import_name
            case 'list':
                import_name, install_name = import_name
            case _:
                raise TypeError(
                    cleandoc(
                        f'''
                        expected types of 'command' argument:
                            str, list
                        get:
                            {type(import_name).__name__}
                        '''
                    )
                )

        try:
            __import__(import_name)
        except ImportError:
            print(f'installing {install_name}...')
            run(f'{sys.executable} -m pip install {install_name}')

main()
