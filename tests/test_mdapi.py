import importlib
from queue import Queue

import pytest

Q_CONNECT = Queue(maxsize=1)
Q_LOGIN = Queue(maxsize=1)

TIMEOUT = 5  # seconds


@pytest.fixture(scope='session')
def ctp(pytestconfig):
    return pytestconfig.getoption("ctp")


def test_mdapi(ctp):
    ctp_pkg = f'openctp_ctp_{ctp}'
    mdapi = getattr(importlib.import_module(ctp_pkg), 'mdapi')
    ctp_version = f'{ctp[0]}.{ctp[1]}.{ctp[2:]}'

    class CMdSpiImpl(mdapi.CThostFtdcMdSpi):
        def __init__(self, md_api):
            super().__init__()
            self.md_api = md_api

        def OnFrontConnected(self):
            Q_CONNECT.put(True, timeout=TIMEOUT)
            req = mdapi.CThostFtdcReqUserLoginField()
            self.md_api.ReqUserLogin(req, 0)

        def OnRspUserLogin(self, pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
                           pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int,
                           bIsLast: bool):
            if pRspInfo is None or pRspInfo.ErrorID == 0:
                # success
                Q_LOGIN.put(True, timeout=TIMEOUT)
            else:
                # failed
                Q_LOGIN.put(False, timeout=TIMEOUT)

    # Success if at least 1 md front success.
    md_fronts = (
        'tcp://180.168.146.187:10131',
        'tcp://180.168.146.187:10211',
        'tcp://180.168.146.187:10212',
        'tcp://180.168.146.187:10213',
    )
    error = None
    for md_front in md_fronts:
        try:
            md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi()

            assert ctp_version in md_api.GetApiVersion(), 'GetApiVersion Failed!'

            md_spi = CMdSpiImpl(md_api)
            md_api.RegisterFront(md_front)
            md_api.RegisterSpi(md_spi)
            md_api.Init()

            try:
                Q_CONNECT.get(timeout=TIMEOUT)
            except:
                assert False, 'Connect Failed!'

            try:
                if not Q_LOGIN.get(timeout=TIMEOUT):
                    assert False, 'Login Failed!'

            except:
                assert False, 'Login Failed!'

            # success
            break
        except AssertionError as e:
            error = str(e)
    else:
        # Failed
        assert False, error
