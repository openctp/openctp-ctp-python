"""
    行情API demo
"""
import random

from openctp_ctp_667 import mdapi


class CMdSpiImpl(mdapi.CThostFtdcMdSpi):
    def __init__(self, md_api):
        super().__init__()
        self.md_api = md_api

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("OnFrontConnected")
        req = mdapi.CThostFtdcReqUserLoginField()
        self.md_api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: mdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        print(f"OnRspUserLogin: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")
        if len(instruments) == 0:
            print("No instruments.")
            return
        self.md_api.SubscribeMarketData([i.encode('utf-8') for i in instruments], len(instruments))

    def OnRtnDepthMarketData(self, pDepthMarketData: mdapi.CThostFtdcDepthMarketDataField):
        """ 深度行情 """
        print("InstrumentID:", pDepthMarketData.InstrumentID, " LastPrice:", pDepthMarketData.LastPrice,
              " Volume:", pDepthMarketData.Volume, " PreSettlementPrice:", pDepthMarketData.PreSettlementPrice,
              " PreClosePrice:", pDepthMarketData.PreClosePrice, " TradingDay:", pDepthMarketData.TradingDay)

    def OnRspSubMarketData(self, pSpecificInstrument: mdapi.CThostFtdcSpecificInstrumentField,
                           pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 订阅行情应答 """
        print("OnRspSubMarketData:ErrorID=", pRspInfo.ErrorID, " ErrorMsg=", pRspInfo.ErrorMsg)


if __name__ == '__main__':
    md_front = random.choice(('tcp://180.168.146.187:10131',
                              'tcp://180.168.146.187:10211',
                              'tcp://180.168.146.187:10212',
                              'tcp://180.168.146.187:10213'))
    instruments = ('au2305', 'rb2305', 'TA305', 'i2305', 'IF2302')

    md_api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi("market")
    print("ApiVersion: ", md_api.GetApiVersion())
    md_spi = CMdSpiImpl(md_api)
    md_api.RegisterFront(md_front)
    md_api.RegisterSpi(md_spi)
    md_api.Init()

    print("press Enter key to exit ...")
    input()
