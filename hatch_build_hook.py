import os
import platform
import sys
from typing import Dict, Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:

        base_dir = os.path.basename(os.getcwd()).split('-')[1]
        parent_dir = os.path.dirname(os.getcwd())

        build_data['pure_python'] = False
        build_data['infer_tag'] = True
        build_data['force_include'].update({
            os.path.join(parent_dir, 'init.py'): os.path.join(base_dir, '__init__.py'),
        })

        if sys.platform.startswith('linux'):
            build_data['force_include'].update({
                os.path.join(base_dir, 'linux_x64'): base_dir,
            })

        elif sys.platform.startswith('darwin'):
            if platform.machine() == 'x86_64':
                build_data['force_include'].update({
                    os.path.join(base_dir, 'mac_x64'): base_dir,
                })
            elif platform.machine() == 'amd64':
                pass

        elif sys.platform.startswith('win'):
            major, minor = sys.version_info[:2]
            assert major == 3
            assert minor in (7, 8, 9, 10, 11)
            win_dir = os.path.join(base_dir, 'win_x64')
            md = 'thostmduserapi_se.dll'
            td = 'thosttraderapi_se.dll'
            build_data['force_include'].update({
                os.path.join(win_dir, md): os.path.join(base_dir, md),
                os.path.join(win_dir, td): os.path.join(base_dir, td),
                os.path.join(win_dir, f'py3{minor}'): base_dir,
            })
