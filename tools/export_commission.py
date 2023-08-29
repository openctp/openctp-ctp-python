"""
    导出合约手续费率
"""
import inspect
import time
from queue import Queue

from openctp_ctp import tdapi

# 交易前置地址 可以在 http://121.37.80.177:50080/detail.html 查看SimNow前置地址; 或其他支持 CTPAPI 的前置地址
td_front = 'tcp://180.168.146.187:10130'

# 账号/密码 从 OpenCTP 公众号申请
user = '209025'
password = 'xxx'

broker_id = '9999'
authcode = '0000000000000000'
appid = 'simnow_client_test'

Q_INSTRUMENT = Queue()  # type: Queue[dict|None]
Q_RATE = Queue()  # type: Queue[dict|None]
Q_MARKET = Queue()  # type: Queue[dict|None]


def copy_field(src):
    dst = type(src)()
    for name, value in inspect.getmembers(src):
        if name[0].isupper():
            setattr(dst, name, value)
    return dst


class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    """ 交易回调实现类 """

    def __init__(self, _api: tdapi.CThostFtdcTraderApi):
        super().__init__()
        self._api = _api

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("> 交易前置连接成功")

        # 认证请求
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = broker_id
        req.UserID = user
        req.AppID = appid
        req.AuthCode = authcode
        self._api.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("> 交易前置连接断开: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                          pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print(f"> 认证失败: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
            return

        print("> 认证成功")

        if pRspInfo is None or pRspInfo.ErrorID == 0:
            # 登录请求
            req = tdapi.CThostFtdcReqUserLoginField()
            req.BrokerID = broker_id
            req.UserID = user
            req.Password = password
            req.UserProductInfo = "openctp"
            self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print(f"> 登录失败: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
            return

        print("> 登录成功:", pRspUserLogin.UserID, "TradingDay=", pRspUserLogin.TradingDay)

        print("> 查询所有合约")
        req = tdapi.CThostFtdcQryInstrumentField()
        req.BrokerID = broker_id
        req.InvestorID = user
        req.InstrumentID = 'RI309'
        self._api.ReqQryInstrument(req, 0)

    def OnRspQryInstrument(self, pInstrument: tdapi.CThostFtdcInstrumentField,
                           pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 查询合约响应 """
        if pRspInfo and pRspInfo.ErrorID:
            print(f"> 查询合约失败: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
        else:
            for v, m in inspect.getmembers(pInstrument):
                if v[0].isupper():
                    print(v, m)
            Q_INSTRUMENT.put_nowait({
                "ExchangeID": pInstrument.ExchangeID,
                "InstrumentID": pInstrument.InstrumentID,
                "ProductID": pInstrument.ProductID,
                "VolumeMultiple": pInstrument.VolumeMultiple,
            })

        if bIsLast:
            print("> 接收合约完成, 数量:", Q_INSTRUMENT.qsize())
            Q_INSTRUMENT.put_nowait(None)
            print("> 查询所有行情")
            req = tdapi.CThostFtdcQryDepthMarketDataField()
            self._api.ReqQryDepthMarketData(req, 0)

    def OnRspQryInstrumentCommissionRate(self, pInstrumentCommissionRate: tdapi.CThostFtdcInstrumentCommissionRateField,
                                         pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 查询合约手续费率响应 """
        if pRspInfo and pRspInfo.ErrorID:
            print(f"> 查询合约响应失败: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
            return

        # print(f"查询合约手续费率响应成功: InstrumentID={pInstrumentCommissionRate.InstrumentID}")
        if pInstrumentCommissionRate:
            Q_RATE.put_nowait({
                "ExchangeID": pInstrumentCommissionRate.ExchangeID,
                "InstrumentID": pInstrumentCommissionRate.InstrumentID,
                "OpenRatioByMoney": pInstrumentCommissionRate.OpenRatioByMoney,
                "OpenRatioByVolume": pInstrumentCommissionRate.OpenRatioByVolume,
                "CloseRatioByMoney": pInstrumentCommissionRate.CloseRatioByMoney,
                "CloseRatioByVolume": pInstrumentCommissionRate.CloseRatioByVolume,
                "CloseTodayRatioByMoney": pInstrumentCommissionRate.CloseTodayRatioByMoney,
                "CloseTodayRatioByVolume": pInstrumentCommissionRate.CloseTodayRatioByVolume,
            })
        else:
            Q_RATE.put_nowait(None)

    def OnRspQryDepthMarketData(self, pDepthMarketData: tdapi.CThostFtdcDepthMarketDataField,
                                pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 请求查询行情响应 """
        if pRspInfo and pRspInfo.ErrorID:
            print("> 请求查询行情响应失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
        else:
            Q_MARKET.put_nowait({
                "ExchangeID": pDepthMarketData.ExchangeID,
                "InstrumentID": pDepthMarketData.InstrumentID,
                "LastPrice": pDepthMarketData.LastPrice,
            })

        if bIsLast:
            Q_MARKET.put_nowait(None)


def process_export(td_api: tdapi.CThostFtdcTraderApi):
    """ 处理并导出手续费率 """

    # dict_instrument = {}
    # dict_rate = {}
    dict_market = {}

    while True:
        try:
            market = Q_MARKET.get()
            if market is None and not Q_MARKET.qsize():
                break

            dict_market[market["ExchangeID"] + market["InstrumentID"]] = market

        except Exception as err:
            print('接收行情异常:', err)
            exit(-1)

    print("> 接收行情完成, 数量:", len(dict_market))

    count_instrument = 0
    with open('合约手续费率.csv', mode='w', encoding='utf8') as fp:
        fp.write(
            '交易所,合约,品种,合约乘数,开仓费率,平仓费率,平今仓费率,最新价,1手开仓手续费,1手平仓手续费,1手平今仓手续费\n')
        while True:
            try:
                time.sleep(1)
                instrument = Q_INSTRUMENT.get()
                if instrument is None:
                    print('no')
                    break

                # dict_instrument[instrument.InstrumentID] = instrument

                # 查询手续费率
                req = tdapi.CThostFtdcQryInstrumentCommissionRateField()
                req.BrokerID = broker_id
                req.InvestorID = user
                req.InstrumentID = instrument["InstrumentID"]
                ret = td_api.ReqQryInstrumentCommissionRate(req, 0)
                if ret != 0:
                    print('sleep', count_instrument)
                    time.sleep(1)
                    ret = td_api.ReqQryInstrumentCommissionRate(req, 0)
                    if ret != 0:
                        print('请求手续费率失败:', instrument["InstrumentID"], ret)
                        continue

                market = dict_market.get(instrument["ExchangeID"] + instrument["InstrumentID"])
                if market is None:
                    print(f'合约 {instrument["InstrumentID"]} 无行情')
                    continue

                rate = Q_RATE.get()
                if rate is None:
                    print(f'合约 {instrument["InstrumentID"]} 无手续费')
                    continue

                if rate["InstrumentID"] != instrument["InstrumentID"] or rate["ExchangeID"] != instrument["ExchangeID"]:
                    print(f'合约 {instrument["InstrumentID"]} 手续费异常: ', rate, instrument)
                    continue

                fp.write(f'{instrument["ExchangeID"]},{instrument["InstrumentID"]},{instrument["ProductID"]},'
                         f'{instrument["VolumeMultiple"]},{rate["OpenRatioByMoney"]},{rate["CloseRatioByMoney"]},'
                         f'{rate["CloseTodayRatioByMoney"]},{market["LastPrice"]}\n')

                count_instrument += 1
                print(count_instrument, Q_INSTRUMENT.qsize())
                if count_instrument >= 100:
                    break

            except Exception as err:
                print("异常:", err)
                exit(-1)

    print('写入合约:', count_instrument)
    # print('合约数量:', len(dict_instrument), '手续费率数量:', len(dict_rate), '行情数量:', len(dict_market))

    # save to csv


if __name__ == '__main__':
    # 实例化交易请求类
    api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(user)  # type: tdapi.CThostFtdcTraderApi
    print("CTP交易API版本号:", api.GetApiVersion())
    print("交易前置地址:", td_front)
    # 实例化交易回调实现类
    spi = CTdSpiImpl(api)
    # 注册交易前置地址
    api.RegisterFront(td_front)
    # 交易请求实例 注册 交易回调实例
    api.RegisterSpi(spi)
    # 订阅私有流
    api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
    # 订阅公有流
    api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
    # 初始化交易实例
    api.Init()

    print('导出合约手续费率开始')
    process_export(api)
    print('导出合约手续费率结束')

    # 阻塞 等待
    # print("Press Enter key to exit ...")
    # input()

    # 释放实例
    api.Release()
