# openctp-ctp-667

[![PyPI - Version](https://badgen.net/badge/pypi/v1.0.0/blue)](https://pypi.org/project/openctp-ctp-667)
[![PyPI - Python Version](https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue)](https://pypi.org/project/openctp-ctp-667)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install openctp-ctp-667
```

## Example

[Demo](https://github.com/Jedore/openctp-ctp-python/tree/main/demo)

```python
from openctp_ctp_667 import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

## License

`openctp-ctp-667` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
