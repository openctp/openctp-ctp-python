from openctp_ctp import tdapi

import config


class CTdSpiBase(tdapi.CThostFtdcTraderSpi):
    """ 交易回调实现类 """

    def __init__(self, front_name: str):
        print("----------------------------------------------------------- 测试开始 ")
        super().__init__()
        self._front_name = front_name
        self._front = config.fronts[front_name]["td"]
        self._user = config.user
        self._password = config.password
        self._authcode = config.authcode
        self._appid = config.appid
        self._broker_id = config.broker_id

        self._is_authenticate = False

        self._api: tdapi.CThostFtdcTraderApi = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(self._user)

        print("CTP交易API版本号:", self._api.GetApiVersion())
        print("交易前置", self._front_name, "环境", self._front)

        # 注册交易前置
        self._api.RegisterFront(self._front)
        # 注册交易回调实例
        self._api.RegisterSpi(self)
        # 订阅私有流
        self._api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
        # 订阅公有流
        self._api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
        # 初始化交易实例
        self._api.Init()

    def release(self):
        # 释放实例
        self._api.Release()

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("交易前置连接成功")

        print("发送认证请求")
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = self._broker_id
        req.UserID = self._user
        req.AppID = self._appid
        req.AuthCode = self._authcode
        self._api.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("交易前置连接断开: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                          pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("认证失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("认证成功")
        self._is_authenticate = True

    def wait(self):
        # 阻塞 等待
        print("----------------------------------------------------------- 按任意键退出程序 ")
        input()

        self.release()


if __name__ == '__main__':
    spi = CTdSpiBase('7x24')
    spi.wait()
