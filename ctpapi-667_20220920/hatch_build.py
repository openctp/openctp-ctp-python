import sys
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        build_data['artifacts'] = ['ctpapi_667/linux64']
        build_data['pure_python'] = False
        print(build_data)
        # if sys.platform.startswith('linux'):
        #     build_data['tag'] = 'py3-none-'
        # elif sys.platform.startswith('darwin'):
        #     build_data['tag'] = 'py3-none-'
        # elif sys.platform.startswith('win'):
        #     build_data['tag'] = 'py3-none-'
