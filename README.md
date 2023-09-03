<h1 align="center">OPENCTP-CTP</h1>

<p align="center">          
    <em>:rocket:以 Python 的方式，简化对接 CTPAPI 的过程，节省精力，快速上手</em>  
</p>

<p align="center">     
    <a href="https://gitee.com/jedore/ctp-resources" target="_blank">
        <img src="https://badgen.net/badge/ctpapi/6.3.15|6.3.19_P1|6.5.1|6.6.1_P1|6.6.7|6.6.9|6.7.0/green" />
    </a>       
    <a href="#">     
        <img src="https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/green" />          
    </a> 
    <a href="#">         
        <img src="https://badgen.net/badge/plat/Windows|Linux|Mac/green" />  
    </a>        
</p>

<p align="center">     
    <a href="https://pypi.org/project/openctp-ctp" target="_blank">                                             
        <img src="https://badgen.net/badge/pypi/openctp-ctp/green" />                    
    </a> 
    <a href="https://pepy.tech/project/openctp-ctp" target="_blank">                                             
        <img src="https://static.pepy.tech/badge/openctp-ctp" />                    
    </a> 
</p>

## 安装

```shell
pip install openctp-ctp==6.3.15.*
pip install openctp-ctp==6.3.19.*
pip install openctp-ctp==6.5.1.*
pip install openctp-ctp==6.6.1.*
pip install openctp-ctp==6.6.7.*
pip install openctp-ctp==6.6.9.*
pip install openctp-ctp==6.7.0.*
```

同时只能安装一个版本的CTPAPI

## 代码示例

```python
from openctp_ctp import mdapi, tdapi

md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
td_api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi('user_id')
```

- 行情 [demo](demo/mdapi.py)
- 交易 [demo](demo/tdapi.py)

## 功能

- 支持多版本 CTPAPI
    - 6.3.15
    - 6.3.19_P1
    - 6.5.1
    - 6.6.1_P1
    - 6.6.7
    - 6.6.9
    - 6.7.0
- 支持多版本 Python 3.7 ~ 3.11
- 支持多平台
    - Windows x64
    - Linux x64
    - Mac x64 arm64

## 常见问题

1. Linux下安装后，导入时报错
    ```text
    >>> import openctp_ctp
    terminate called after throwing an instance of 'std::runtime_error'
      what():  locale::facet::_S_create_c_locale name not valid
    Aborted
    ```
   这是字符集问题，方案：
    ```bash
    # Ubuntu (20.04)
    sudo apt-get install -y locales
    sudo locale-gen zh_CN.GB18030
   
    # Debian (11)
    sudo apt install locales-all
    sudo localedef -c -f GB18030 -i zh_CN zh_CN.GB18030
   
    # CentOS (7)
    sudo yum install -y kde-l10n-Chinese
    sudo yum reinstall -y glibc-common
    ```

## 其他说明

- 限于时间/精力有限，只是在 SimNow 模拟平台进行了简单的测试，若要通过 openctp-ctp
  使用CTPAPI所有的接口或用于生产环境，请自行进行充分测试。
- 后续会完善更多的测试, 以及用于生产的验证
- [更新日志](CHANGELOG.md)

*使用本项目进行实盘交易的后果完全由使用者自己承担。*
