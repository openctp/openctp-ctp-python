"""
    交易API demo
"""
import inspect
import queue
import time

from openctp_ctp import tdapi

import config


class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    """交易回调实现类"""

    def __init__(
        self,
        front: str,
        user: str,
        passwd: str,
        authcode: str,
        appid: str,
        broker_id: str,
    ):
        print("-------------------------------- 启动 trader api demo ")
        super().__init__()
        self._front = front
        self._user = user
        self._password = passwd
        self._authcode = authcode
        self._appid = appid
        self._broker_id = broker_id

        self._is_authenticate = False
        self._is_login = False

        self._is_last = True
        self._print_max = 5
        self._print_count = 0
        self._total = 0

        self._wait_queue = queue.Queue(1)

        self._api: tdapi.CThostFtdcTraderApi = (
            tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(self._user)
        )

        print("CTP交易API版本号:", self._api.GetApiVersion())
        print("交易前置:" + self._front)

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
        print("初始化成功")

    @property
    def is_login(self):
        return self._is_login

    def release(self):
        # 释放实例
        self._api.Release()

    def _check_req(self, req, ret: int):
        """检查请求"""

        # 打印请求
        params = []
        for name, value in inspect.getmembers(req):
            if name[0].isupper():
                params.append(f"{name}={value}")
        self.print("发送请求:", ",".join(params))

        # 检查请求结果
        error = {
            0: "",
            -1: "网络连接失败",
            -2: "未处理请求超过许可数",
            -3: "每秒发送请求数超过许可数",
        }.get(ret, "未知错误")
        if ret != 0:
            self.print(f"请求失败: {ret}={error}")

    def _check_rsp(
        self, pRspInfo: tdapi.CThostFtdcRspInfoField, rsp=None, is_last: bool = True
    ) -> bool:
        """检查响应

        True: 成功 False: 失败
        """

        if self._is_last:
            if pRspInfo and pRspInfo.ErrorID != 0:
                self.print(
                    f"响应失败, ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}"
                )
                return False

            self.print(f"响应成功")
            if rsp:
                params = []
                for name, value in inspect.getmembers(rsp):
                    if name[0].isupper():
                        params.append(f"{name}={value}")
                self.print("响应内容:", ",".join(params))

            if not is_last:
                self._print_count += 1
                self._total = +1
            else:
                if self._is_login:
                    self._wait_queue.put_nowait(None)

        else:
            if self._print_count < self._print_max:
                if rsp:
                    params = []
                    for name, value in inspect.getmembers(rsp):
                        if name[0].isupper():
                            params.append(f"{name}={value}")
                    self.print("     ", ",".join(params))

                self._print_count += 1

            self._total += 1

            if is_last:
                self.print("总计数量:", self._total, "打印数量:", self._print_count)

                self._print_count = 0
                self._total = 0

                if self._is_login:
                    self._wait_queue.put_nowait(None)

        self._is_last = is_last

        return True

    @staticmethod
    def print_rsp_rtn(prefix, rsp_rtn):
        if rsp_rtn:
            params = []
            for name, value in inspect.getmembers(rsp_rtn):
                if name[0].isupper():
                    params.append(f"{name}={value}")
            print(">", prefix, ",".join(params))

    @staticmethod
    def print(*args, **kwargs):
        print("    ", *args, **kwargs)

    def OnFrontConnected(self):
        """交易前置连接成功"""
        print("交易前置连接成功")

        self.authenticate()

    def OnFrontDisconnected(self, nReason: int):
        """交易前置连接断开"""
        print("交易前置连接断开: nReason=", nReason)

        # todo 可以在这里定义交易连接断开时的逻辑

    def authenticate(self):
        """认证 demo"""
        print("> 认证")
        _req = tdapi.CThostFtdcReqAuthenticateField()
        _req.BrokerID = self._broker_id
        _req.UserID = self._user
        _req.AppID = self._appid
        _req.AuthCode = self._authcode
        self._check_req(_req, self._api.ReqAuthenticate(_req, 0))

    def OnRspAuthenticate(
        self,
        pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """客户端认证响应"""
        if not self._check_rsp(pRspInfo, pRspAuthenticateField):
            return

        self._is_authenticate = True

        # 登录
        self.login()

    def login(self):
        """登录 demo"""
        print("> 登录")

        _req = tdapi.CThostFtdcReqUserLoginField()
        _req.BrokerID = self._broker_id
        _req.UserID = self._user
        _req.Password = self._password
        self._check_req(_req, self._api.ReqUserLogin(_req, 0))

    def OnRspUserLogin(
        self,
        pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """登录响应"""
        if not self._check_rsp(pRspInfo, pRspUserLogin):
            return

        self._is_login = True

    def settlement_info_confirm(self):
        """投资者结算结果确认"""
        print("> 投资者结算结果确认")

        _req = tdapi.CThostFtdcSettlementInfoConfirmField()
        _req.BrokerID = self._broker_id
        _req.InvestorID = self._user
        self._check_req(_req, self._api.ReqSettlementInfoConfirm(_req, 0))

    def OnRspSettlementInfoConfirm(
        self,
        pSettlementInfoConfirm: tdapi.CThostFtdcSettlementInfoConfirmField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """投资者结算结果确认响应"""
        if not self._check_rsp(pRspInfo, pSettlementInfoConfirm):
            return

    def qry_instrument(
        self, exchange_id: str = "", product_id: str = "", instrument_id: str = ""
    ):
        """请求查询合约"""
        print("> 请求查询合约")
        _req = tdapi.CThostFtdcQryInstrumentField()
        # 填空可以查询到所有合约
        # 也可分别根据交易所、品种、合约 三个字段查询指定的合约
        _req.ExchangeID = exchange_id
        _req.ProductID = product_id
        _req.InstrumentID = instrument_id
        self._check_req(_req, self._api.ReqQryInstrument(_req, 0))

    def OnRspQryInstrument(
        self,
        pInstrument: tdapi.CThostFtdcInstrumentField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """请求查询合约响应"""
        if not self._check_rsp(pRspInfo, pInstrument, bIsLast):
            return

    def qry_instrument_commission_rate(self, instrument_id: str = ""):
        """请求查询合约手续费率"""
        print("> 请求查询合约手续费率")
        _req = tdapi.CThostFtdcQryInstrumentCommissionRateField()
        _req.BrokerID = self._broker_id
        _req.InvestorID = self._user
        # 若不指定合约ID, 则返回当前持仓对应合约的手续费率
        _req.InstrumentID = instrument_id
        self._check_req(_req, self._api.ReqQryInstrumentCommissionRate(_req, 0))

    def OnRspQryInstrumentCommissionRate(
        self,
        pInstrumentCommissionRate: tdapi.CThostFtdcInstrumentCommissionRateField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """请求查询合约手续费率响应"""
        if not self._check_rsp(pRspInfo, pInstrumentCommissionRate, bIsLast):
            return

    def qry_instrument_margin_rate(self, instrument_id: str = ""):
        """请求查询合约保证金率"""
        print("> 请求查询合约保证金率")
        _req = tdapi.CThostFtdcQryInstrumentMarginRateField()
        _req.BrokerID = self._broker_id
        _req.InvestorID = self._user
        _req.HedgeFlag = tdapi.THOST_FTDC_HF_Speculation
        # 若不指定合约ID, 则返回当前持仓对应合约的保证金率
        _req.InstrumentID = instrument_id
        self._check_req(_req, self._api.ReqQryInstrumentMarginRate(_req, 0))

    def OnRspQryInstrumentMarginRate(
        self,
        pInstrumentMarginRate: tdapi.CThostFtdcInstrumentMarginRateField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """请求查询合约保证金率响应"""
        if not self._check_rsp(pRspInfo, pInstrumentMarginRate, bIsLast):
            return

    def qry_depth_market_data(self, instrument_id: str = ""):
        """请求查询行情，只能查询当前快照，不能查询历史行情"""
        print("> 请求查询行情")
        _req = tdapi.CThostFtdcQryDepthMarketDataField()
        # 若不指定合约ID, 则返回所有合约的行情
        _req.InstrumentID = instrument_id
        self._check_req(_req, self._api.ReqQryDepthMarketData(_req, 0))

    def OnRspQryDepthMarketData(
        self,
        pDepthMarketData: tdapi.CThostFtdcDepthMarketDataField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """请求查询行情响应"""
        if not self._check_rsp(pRspInfo, pDepthMarketData, bIsLast):
            return

    def order_insert(self):
        """报单录入请求

        - 录入错误时对应响应OnRspOrderInsert、OnErrRtnOrderInsert，
        - 正确时对应回报OnRtnOrder、OnRtnTrade。
        """

    def order_cancel(self):
        """报单撤销请求

        - 错误响应: OnRspOrderAction，OnErrRtnOrderAction
        - 正确响应：OnRtnOrder
        """

    def OnRspOrderInsert(
        self,
        pInputOrder: tdapi.CThostFtdcInputOrderField,
        pRspInfo: tdapi.CThostFtdcRspInfoField,
        nRequestID: int,
        bIsLast: bool,
    ):
        """报单录入请求响应"""
        if not self._check_rsp(pRspInfo, pInputOrder, bIsLast):
            return

    def OnRtnOrder(self, pOrder: tdapi.CThostFtdcOrderField):
        """报单通知，当执行ReqOrderInsert后并且报出后，收到返回则调用此接口，私有流回报。"""

    def OnRtnTrade(self, pTrade: tdapi.CThostFtdcTradeField):
        """成交通知，报单发出后有成交则通过此接口返回。私有流"""

    def wait(self):
        # 阻塞 等待
        self._wait_queue.get()
        input("-------------------------------- 按任意键退出 trader api demo ")

        self.release()


if __name__ == "__main__":
    spi = CTdSpiImpl(
        config.fronts["电信1"]["td"],
        config.user,
        config.password,
        config.authcode,
        config.appid,
        config.broker_id,
    )

    # 等待登录成功
    while True:
        time.sleep(1)
        if spi.is_login:
            break

    # 代码中的请求参数编写时测试通过, 不保证以后一定成功。
    # 需要测试哪个请求, 取消下面对应的注释, 并按需修改参请求参数即可。

    # spi.settlement_info_confirm()
    # spi.qry_instrument()
    # spi.qry_instrument(exchange_id="CZCE")
    # spi.qry_instrument(product_id="AP")
    # spi.qry_instrument(instrument_id="AP404")
    # spi.qry_instrument_commission_rate()
    # spi.qry_instrument_commission_rate("ZC309")
    # spi.qry_instrument_margin_rate()
    # spi.qry_instrument_margin_rate(instrument_id="ZC309")
    # spi.qry_depth_market_data()
    # spi.qry_depth_market_data(instrument_id="ZC309")

    spi.wait()
