from openctp_ctp import tdapi

from base import CTdSpiBase
from time import sleep


class CTdSpiLogin(CTdSpiBase):
    """ 交易回调实现类 """

    def __init__(self, front_name: str):
        super().__init__(front_name)

        self._is_login = False

    def login(self):
        """ 登录请求 """
        # 等待认证成功
        while not self._is_authenticate:
            sleep(1)

        print("发送登录请求")
        req = tdapi.CThostFtdcReqUserLoginField()
        req.BrokerID = self._broker_id
        req.UserID = self._user
        req.Password = self._password
        self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("登录失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("登录成功:", pRspUserLogin.UserID, "TradingDay=", pRspUserLogin.TradingDay)
        self._is_login = True


if __name__ == '__main__':
    spi = CTdSpiLogin('7x24')
    spi.login()
    spi.wait()
