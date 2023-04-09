# SPDX-FileCopyrightText: 2023-present Jedore <jedore@protonmail.com>
#
# SPDX-License-Identifier: MIT
import os
import sys

path = os.getcwd()

is_linux = sys.platform.startswith('linux')
if is_linux:
    os.chdir(os.path.dirname(__file__))

from . import thostmduserapi as mdapi
from . import thosttraderapi as tdapi

if is_linux:
    os.chdir(path)

__all__ = ['mdapi', 'tdapi']
