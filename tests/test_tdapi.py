"""
written by krenx on 2023-1-10.
published in openctp@github: https://github.com/krenx1983/openctp/tree/master/ctpapi-python
"""

import sys

import importlib
from queue import Queue

import pytest

Q_CONNECT = Queue(maxsize=1)
Q_AUTH = Queue(maxsize=1)

TIMEOUT = 5  # seconds


@pytest.fixture(scope='session')
def ctp(pytestconfig):
    return pytestconfig.getoption("ctp")


def test_mdapi(ctp):
    ctp_pkg = f'openctp_ctp_{ctp}'
    tdapi = getattr(importlib.import_module(ctp_pkg), 'tdapi')
    ctp_version = f'{ctp[0]}.{ctp[1]}.{ctp[2:]}'

    class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
        def __init__(self, tdapi):
            super().__init__()
            self.tdapi = tdapi

        def OnFrontConnected(self):
            Q_CONNECT.put(True, timeout=TIMEOUT)
            req = tdapi.CThostFtdcReqAuthenticateField()
            req.BrokerID = brokerid
            req.UserID = user
            req.AppID = appid
            req.AuthCode = authcode
            self.tdapi.ReqAuthenticate(req, 0)

        def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                              pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
            if pRspInfo is None or pRspInfo.ErrorID == 0:
                # success
                Q_AUTH.put(True, timeout=TIMEOUT)
            else:
                # failed
                Q_AUTH.put(False, timeout=TIMEOUT)

    # Success if at least 1 md front success.
    td_fronts = (
        'tcp://180.168.146.187:10130',
        'tcp://180.168.146.187:10201',
        'tcp://180.168.146.187:10202',
        'tcp://180.168.146.187:10203',
    )
    error = None
    for td_front in td_fronts:
        try:
            user = '209025'

            brokerid = '9999'
            authcode = '0000000000000000'
            appid = 'simnow_client_test'

            tdapi = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(user)

            assert ctp_version in tdapi.GetApiVersion(), 'GetApiVersion Failed!'

            tdspi = CTdSpiImpl(tdapi)
            tdapi.RegisterSpi(tdspi)
            tdapi.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
            tdapi.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
            tdapi.RegisterFront(td_front)
            tdapi.Init()

            try:
                Q_CONNECT.get(timeout=TIMEOUT)
            except:
                assert False, 'Connect Failed!'

            try:
                if not Q_AUTH.get(timeout=TIMEOUT):
                    assert False, 'Auth Failed!'

            except:
                assert False, 'Auth Failed!'

            # success
            break
        except AssertionError as e:
            error = str(e)
    else:
        assert False, error
