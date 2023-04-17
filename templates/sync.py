"""
    Sync pyproject.toml/__about__.py/init.py
    Execute this module in project root directory.
"""

import os
import shutil
import sys

if __name__ == '__main__':
    try:
        ctp_version = sys.argv[1]
    except IndexError:
        print('Execute in project root directory: \n'
              '     python sync.py <ctp version>')
        exit(-1)

    target_dir = os.path.join(os.getcwd(), f'openctp-ctp-{ctp_version}')
    print('Target dir', target_dir)


    def src_file(*filenames):
        return os.path.join('templates', *filenames)


    def test_file(*filenames):
        return os.path.join('tests', *filenames)


    def target_file(*filenames):
        return os.path.join(target_dir, *filenames)


    print('Sync __about__.py')
    with open(src_file('__about__.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('PKG_VERSION', '1.0.1')
    with open(target_file('libs', '__about__.py'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync __init__.py')
    shutil.copyfile(src_file('init.py'), target_file('libs', '__init__.py'))

    print('Sync pyproject.toml')
    with open(src_file('pyproject.toml'), 'r') as file_obj:
        text = file_obj.read()
    version = f'{ctp_version[0]}.{ctp_version[1]}.{ctp_version[2:]}'
    new_text = text.replace('CTP_VERSION2', version)
    new_text = new_text.replace('CTP_VERSION', ctp_version)
    if sys.platform.startswith('darwin'):
        new_text = new_text.replace('TEST', 'pytest tests/test_mdapi.py')
    else:
        new_text = new_text.replace('TEST', 'pytest tests')
    with open(target_file('pyproject.toml'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync README.md')
    with open(src_file('README.md'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION', ctp_version)
    with open(target_file('README.md'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync hook')
    with open(src_file('hatch_build_hook.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION', ctp_version)
    with open(target_file('hatch_build_hook.py'), 'w') as file_obj:
        file_obj.write(new_text)

    print('Sync tests')
    os.mkdir(target_file('tests'))
    with open(src_file('tests', 'test_mdapi.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION2', version)
    new_text = new_text.replace('CTP_VERSION', ctp_version)
    with open(target_file('tests', 'test_mdapi.py'), 'w') as file_obj:
        file_obj.write(new_text)

    with open(src_file('tests', 'test_tdapi.py'), 'r') as file_obj:
        text = file_obj.read()
    new_text = text.replace('CTP_VERSION2', version)
    new_text = new_text.replace('CTP_VERSION', ctp_version)
    with open(target_file('tests', 'test_tdapi.py'), 'w') as file_obj:
        file_obj.write(new_text)
