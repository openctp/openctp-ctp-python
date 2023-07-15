<p align="center">     
    <a href="http://www.sfit.com.cn/5_2_DocumentDown_6.htm" target="_blank">
        <img src="https://badgen.net/badge/ctpapi/6.3.15|6.3.19_P1|6.5.1|6.6.1_P1|6.6.7|6.6.9/cyan" />
    </a>       
    <a href="#">         
        <img src="https://badgen.net/badge/platform/windows_x64|linux_x64|mac_x64/cyan" />  
    </a>        
</p>

<p align="center">  
    <a href="#">     
        <img src="https://badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11/cyan" />          
    </a> 
    <a href="https://pypi.org/project/openctp-ctp-669" target="_blank">                                             
        <img src="https://badgen.net/badge/pypi/openctp-ctp/blue" />                    
    </a> 
</p>


<p align="center">          
    <em>:rocket:以 Python 的方式，简化对接 CTP 的过程，节省精力，快速上手</em>  
</p>

-----

## 安装

```shell
pip install openctp-ctp==6.3.15.*
pip install openctp-ctp==6.3.19.*
pip install openctp-ctp==6.5.1.*
pip install openctp-ctp==6.6.1.*
pip install openctp-ctp==6.6.7.*
pip install openctp-ctp==6.6.9.*
```

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
- 支持多版本 Python 3.7 ~ 3.11
- 支持多平台
    - Windows x64
    - Linux x64
    - Mac x64

## 其他说明

- 限于时间/精力有限，只是在 SimNow 平台进行了简单的测试，若要通过 openctp-ctp
  使用CTPAPI所有的接口或用于生产环境，请自行进行充分测试。
- 后续会完善更多的测试, 以及用于生产的验证

*使用本项目进行实盘交易的后果完全由使用者自己承担。*
