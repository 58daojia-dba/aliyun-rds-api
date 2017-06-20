# -*- coding: utf-8 -*-
import re
import unittest
from aliyunsdkrds.request.v20140815.DescribeSlowLogRecordsRequest import DescribeSlowLogRecordsRequest
from ali_rds import AliRds

class AliRdsTestCase(unittest.TestCase):
    def setUp(self):
        #print("init")
        pass

    def tearDown(self):
        #print("teardown")
        pass

    def test_get_result(self):
        #正确的参数
        request=DescribeSlowLogRecordsRequest()
        request.set_DBInstanceId('rdsx2y9yieqqer90yl2z')
        request.set_EndTime('2016-12-25T15:01Z')
        request.set_StartTime('2016-12-25T15:00Z')
        result=AliRds.get_result(request)
        print result
        self.assertEquals(True,result.has_key("RequestId"))



    def t_test_get_result(self):
        #正确的参数
        request=DescribeSlowLogRecordsRequest()
        request.set_DBInstanceId('rdsx2y9yieqqer90yl2z')
        request.set_EndTime('2016-12-25T15:01Z')
        request.set_StartTime('2016-12-25T15:00Z')
        result=AliRds.get_result(request)
        print result
        self.assertEquals(True,result.has_key("RequestId"))
        #for (k,v) in  result.items():
        #    print k
        request=DescribeSlowLogRecordsRequest()
        request.set_DBInstanceId('rdsx2y9yieqqer90yl2z')
        request.set_EndTime('2016-12-25T15:01Z')
        #错误的时间标识
        request.set_StartTime(1)
        result=AliRds.get_result(request)
        self.assertEquals(u'InvalidStartTime.Malformed',result["Code"])

        request=DescribeSlowLogRecordsRequest()
        result=AliRds.get_result(request)
        self.assertEquals(u'MissingParameter',result["Code"])

    def t_test_result_is_ok(self):
        result=None
        (ok,message)=AliRds.result_is_ok(result)
        self.assertEquals(u"ResultIsNone_My_Defined",message["Code"])

        result=1
        (ok,message)=AliRds.result_is_ok(result)
        self.assertEquals(u"ResultIsNotDict_My_Defined",message["Code"])

        request=DescribeSlowLogRecordsRequest()
        request.set_DBInstanceId('rdsx2y9yieqqer90yl2z')
        request.set_EndTime('2016-12-25T15:01Z')
        request.set_StartTime(1)
        result=AliRds.get_result(request)
        (ok,message)=AliRds.result_is_ok(result)
        #print message
        self.assertEquals(False,ok)