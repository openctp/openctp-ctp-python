from queue import Queue

from openctp_ctp_651 import mdapi

Q_CONNECT = Queue(maxsize=1)
Q_LOGIN = Queue(maxsize=1)

TIMEOUT = 5  # seconds


class CMdSpiImpl(mdapi.CThostFtdcMdSpi):
    def __init__(self, md_api):
        super().__init__()
        self.md_api = md_api

    def OnFrontConnected(self):
        print("OnFrontConnected")
        Q_CONNECT.put(True, timeout=TIMEOUT)
        req = mdapi.CThostFtdcReqUserLoginField()
        self.md_api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int,
                       bIsLast: bool):
        print(f"OnRspUserLogin")
        if pRspInfo is None or pRspInfo.ErrorID == 0:
            print('Login success')
            Q_LOGIN.put(True, timeout=TIMEOUT)
        else:
            print('Login failed: ', pRspInfo.ErrorMsg)
            Q_LOGIN.put(False, timeout=TIMEOUT)


def test_mdapi():
    md_front = 'tcp://180.168.146.187:10211'

    md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi()
    print("ApiVersion: ", md_api.GetApiVersion())
    md_spi = CMdSpiImpl(md_api)
    md_api.RegisterFront(md_front)
    md_api.RegisterSpi(md_spi)
    md_api.Init()

    try:
        Q_CONNECT.get(timeout=TIMEOUT)
    except:
        assert False
    try:
        if not Q_LOGIN.get(timeout=TIMEOUT):
            assert False
    except:
        assert False


if __name__ == '__main__':
    test_mdapi()
