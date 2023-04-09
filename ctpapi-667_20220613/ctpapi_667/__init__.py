# SPDX-FileCopyrightText: 2023-present Jedore <jedore@protonmail.com>
#
# SPDX-License-Identifier: MIT
import os
import sys

if sys.platform.startswith('linux'):
    path = os.getcwd()
    os.chdir(os.path.dirname(__file__))

    from . import thostmduserapi
    from . import thosttraderapi

    os.chdir(path)
