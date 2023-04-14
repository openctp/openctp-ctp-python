# openctp-ctp

[![PyPI - Python Version](https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue)](https://pypi.org/project/openctp-ctp)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install openctp-ctp
```

## Example

[Demo](https://github.com/Jedore/openctp-ctp-python/tree/main/demo)

```python
from openctp_ctp import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

## License

`openctp-ctp` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
