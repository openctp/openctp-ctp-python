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

## 简介

**openctp-ctp** 是由 [**openctp**](https://github.com/openctp) 团队提供的 ctp 官方 ctpapi(c++) 的python版本，
使用 **swig** 转换 ctpapi(c++) 生成。

openctp-ctp 有 6.3.15.x / 6.3.19.x / 6.5.1.x / 6.6.1.x / 6.6.7.x / 6.6.9.x / 6.7.0.x 多个版本系列，
分别对应 ctpapi(c++) 的**生产版本**: 6.3.15 / 6.3.19_P1 / 6.5.1 / 6.6.1_P1 / 6.6.7 / 6.6.9 / 6.7.0

*通过 openctp-ctp 库只能连接支持 ctpapi(c++) **官方实现**的柜台，如：simnow; 不支持连接所谓的兼容 ctpapi(c++)
接口但**非官方实现**的柜台，如: openctp(由tts支持).*

## 安装使用

*需要自行提前准备好 Python 环境*

安装方式:

```shell
# 安装最新版
pip install openctp-ctp
# 指定版本号
pip install openctp-ctp==6.6.7.*
```

*需要注意同时只能安装一个版本系列的 openctp-ctp*

引用方式:

```python 
from openctp_ctp import tdapi, mdapi
```

更多使用方式参见代码示例。

## 代码示例

本项目提供了一些 openctp-ctp 的基本使用方式及部分接口示例，具体如下:

- 行情 [demo](demo/mdapi.py)
    - 登录
    - 订阅行情
- 交易 [demo](demo/tdapi.py)
    - 登录
    - 投资者结算结果确认
    - 请求查询合约
    - 请求查询合约手续费率
    - 请求查询合约保证金率
    - 请求查询行情
    - 报单录入请求
    - 报单撤销请求

**代码示例仅仅作为参考，只是完成 openctp-ctp 库及ctpapi接口本身的功能，未考虑项目及工程性场景逻辑，
若要将 openctp-ctp 引入项目，勿照搬示例代码。**

*代码示例不在pypi库中，只能手动下载使用。*

## 常见问题

1. Linux下安装后，导入时报错
    ```text
    >>> import openctp_ctp
    terminate called after throwing an instance of 'std::runtime_error'
      what():  locale::facet::_S_create_c_locale name not valid
    Aborted
    ```
   这是字符集问题，需要安装 `GB18030` 字符集，这里提供 ubuntu/debian/centos 的方案：
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

2. 如何使用评测版本 ctpapi

   openctp-ctp 只支持 ctpapi 生产版本，不支持评测版本。

3. 支持哪些系统平台
    - Window x64
    - Linux x64
    - Mac x64
    - Mac arm64

   支持 Mac 系统的版本有: 6.6.7/6.6.9/6.7.0

## 其他说明

- 限于时间/精力有限，只是在 SimNow 模拟平台进行了简单的测试，若要通过 openctp-ctp
  使用CTPAPI所有的接口或用于生产环境，请自行进行充分测试。
- 后续会完善更多的测试, 以及用于生产的验证
- [更新日志](CHANGELOG.md)

**使用 openctp-ctp 进行实盘交易的后果完全由使用者自己承担。**
