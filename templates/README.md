# openctp-ctp-CTP_VERSION

[![PyPI - Version](https://badgen.net/badge/pypi/vCTP2/blue)](https://pypi.org/project/openctp-ctp-CTP_VERSION)
[![PyPI - Python Version](https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/blue)](https://pypi.org/project/openctp-ctp-CTP_VERSION)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install openctp-ctp-CTP_VERSION
```

## Example

[Demo](https://github.com/Jedore/openctp-ctp-python/tree/main/demo)

```python
from openctp_ctp_CTP_VERSION import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

## License

`openctp-ctp-CTP_VERSION` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
