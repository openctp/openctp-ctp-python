# SPDX-FileCopyrightText: 2023-present Jedore <jedore@protonmail.com>
#
# SPDX-License-Identifier: MIT
import os
import sys

__all__ = ['mdapi', 'tdapi']

path = os.getcwd()

# switch working directory
is_linux = sys.platform.startswith('linux')
if is_linux:
    os.chdir(os.path.dirname(__file__))

from . import thostmduserapi as mdapi

if not sys.platform.startswith('darwin'):
    from . import thosttraderapi as tdapi

# switch working directory
if is_linux:
    os.chdir(path)
