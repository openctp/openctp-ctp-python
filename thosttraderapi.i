%module(directors="1") thosttraderapi

%pythonbegin %{
# openctp-ctp is supported by openctp(https://github.com/openctp).
# Author: Jedore(https://github.com/Jedore)
#
# BSD 3-Clause License
#
# Copyright (c) 2022, openctp
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
%}

%{
#include "ThostFtdcTraderApi.h"
#include <codecvt>
#include <locale>
#include <vector>
#include <string>
using namespace std;
#ifdef _MSC_VER
const static locale g_loc("zh-CN");
#else
const static locale g_loc("zh_CN.GB18030");
#endif %}

%feature("doxygen:ignore:system", range="line");
%feature("doxygen:ignore:company", range="line");
%feature("doxygen:ignore:history", range="line");
%feature("doxygen:ignore:file", range="line");
// %feature("doxygen:ignore:brief", range="line");
%feature("doxygen:alias:d{8}") "\d{8}"
%feature("doxygen:alias:d{4}") "\d{4}"
%feature("doxygen:alias:d{3}") "\d{3}"
%feature("doxygen:alias:d{1}") "\d{1}"

%feature("python:annotations", "c");
%feature("director") CThostFtdcTraderSpi;

%typemap(out) char[ANY], char[] {
    //if ("$1_name" == "Content" && "$symname" == "CThostFtdcSettlementInfoField_Content_get") {
    if ("$symname" == "CThostFtdcSettlementInfoField_Content_get") {
        $result = PyBytes_FromString($1);
    } else {
        if ($1){
            size_t l = strlen($1);
            if (l == 0) {
                resultobj = SWIG_FromCharPtr("");
            } else {
                const std::string &gbk($1);
                std::vector<wchar_t> wstr(gbk.size());
                wchar_t* wstrEnd = nullptr;
                const char* gbEnd = nullptr;
                mbstate_t state = {};
                int res = use_facet<codecvt<wchar_t, char, mbstate_t>> (g_loc).in(state, gbk.data(), gbk.data() + gbk.size(), gbEnd, wstr.data(), wstr.data() + wstr.size(), wstrEnd);
                if (codecvt_base::ok == res) {
                    wstring_convert<codecvt_utf8<wchar_t>> cutf8;
                    std::string result = cutf8.to_bytes(wstring(wstr.data(), wstrEnd));
                    resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size());
                } else {
                    std::string result;
                    resultobj = SWIG_FromCharPtrAndSize(result.c_str(), result.size());
                }
            }
        }
    }
}

%typemap(out) char {
    if ($1 == '\0'){
        $result = SWIG_FromCharPtr("");
    } else {
        char tmp[1]={0};
        sprintf(tmp, "%c", $1);
        $result = SWIG_FromCharPtr(tmp);
    }
}

%feature("director:except") {
  if ($error != NULL) {
    if (PyErr_ExceptionMatches(PyExc_SystemExit)) {
      throw Swig::DirectorMethodException("Exception: SystemExit");
    } else if (PyErr_ExceptionMatches(PyExc_SystemError)) {
      throw Swig::DirectorMethodException("Exception: SystemError");
    } else {
      PyErr_Print();
    }
  }
}

%ignore THOST_FTDC_VTC_BankBankToFuture;
%ignore THOST_FTDC_VTC_BankFutureToBank;
%ignore THOST_FTDC_VTC_FutureBankToFuture;
%ignore THOST_FTDC_VTC_FutureFutureToBank;
%ignore THOST_FTDC_FTC_BankLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BrokerLaunchBankToBroker;
%ignore THOST_FTDC_FTC_BankLaunchBrokerToBank;
%ignore THOST_FTDC_FTC_BrokerLaunchBrokerToBank;

%include "ThostFtdcUserApiDataType.h"
%include "ThostFtdcUserApiStruct.h"
%include "ThostFtdcTraderApi.h"