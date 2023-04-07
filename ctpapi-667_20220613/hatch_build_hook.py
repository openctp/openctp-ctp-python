import sys
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        build_data['pure_python'] = False
        build_data['infer_tag'] = True
        if sys.platform.startswith('linux'):
            build_data['artifacts'] = ['ctpapi_667/linux64/*.so']
        elif sys.platform.startswith('darwin'):
            build_data['artifacts'] = ['ctpapi_667/mac64/*.so']
        elif sys.platform.startswith('win'):
            major, minor = sys.version_info[:2]
            assert major == 3
            assert minor in (7, 8, 9, 10, 11)
            build_data['force_include'].update({
                'ctpapi_667/win64/thostmduserapi_se.dll': 'ctpapi_667/thostmduserapi_se.dll',
                'ctpapi_667/win64/thosttraderapi_se.dll': 'ctpapi_667/thosttraderapi_se.dll',
                f'ctpapi_667/win64/py3{minor}/_thostmduserapi.pyd': 'ctpapi_667/thostmduserapi.pyd',
                f'ctpapi_667/win64/py3{minor}/_thosttraderapi.pyd': 'ctpapi_667/thosttraderapi.pyd',
            })
