import glob
import os
import platform
import shutil
import sys

cur_dir = os.path.dirname(__file__)
old_dir = os.path.join(os.path.dirname(cur_dir), 'ctpapi_667')

srcs = []
srcs.extend(glob.glob(os.path.join(old_dir, 'thost*.py')))
if sys.platform.startswith('linux'):
    srcs.extend(glob.glob(os.path.join(old_dir, 'linux_x64', '*')))
elif sys.platform.startswith('darwin'):
    if platform.machine() == 'x86_64':
        srcs.extend(glob.glob(os.path.join(old_dir, 'mac_x64', '*')))
        src = os.path.join(old_dir, 'mac_x64')
    elif platform.machine() == 'amd64':
        pass
elif sys.platform.startswith('win'):
    major, minor = sys.version_info[:2]
    assert major == 3
    assert minor in (7, 8, 9, 10, 11)
    path = os.path.join(old_dir, 'win_x64', f'py{major}{minor}', '*')
    srcs.extend(glob.glob(path))

for src in srcs:
    shutil.copy2(src, cur_dir)
