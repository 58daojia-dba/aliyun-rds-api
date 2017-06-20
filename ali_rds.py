# -*- coding: utf-8 -*-
'''
阿里rds api的通用接口
 v0.1.0  2016/12/31  yilai    created
'''

import json
import time
from ali_key  import Constant

from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException as exs


class AliRds(object):
    """
    阿里rds api的通用接口
    """
    @staticmethod
    def get_result(request):
        """
        :param request: 请求对象
        :return: 字典类型
        """
        dt=None
        try:
            #start=time.time()
            Client=client.AcsClient(Constant.get_user_key(),Constant.get_user_secret(),Constant.get_region_id(),
                                    True,3,Constant.get_user_agent())
            request.set_accept_format('json')
            result=Client.do_action(request)
            dt = json.loads(result)
            #finish=time.time()
            #print (finish-start)
            return dt
        except exs as e:
            dt = {'Code':e.get_error_code(), 'Message':e.get_error_msg()}
        return dt

    @staticmethod
    def result_is_ok(result,items=None):
        """
        :param items: 测试result[item[0]][item[1]]的长度是否为0
        :param result: get_reuslt返回的结果集，是一个数据字典
        :return: (boolean,{Code,Message})类型，True表示结果正确
        """
        if result is None:
            return False,{u"Code":u"ResultIsNone_My_Defined",u"Message":u"Result is None"}
        if not isinstance(result,dict):
            return False,{u"Code":u"ResultIsNotDict_My_Defined",u"Message":u"Result is dict type"}
        if result.has_key(u"Code"):
            return False,result
        if items is not None:
           r1=result
           for ele in items:
              r1=r1[ele]
           if len(r1) ==0:
               return False, {u"Code": u"ResultItemIsNull_My_Defined", u"Message": u"Result items is None"}
        return True,result

class AppException(Exception):
    """
      定义程序中的逻辑的异常
    """

    def __init__(self, message, errno=0):
        super(AppException, self).__init__()
        self.args = (message, errno)
        self.errmsg = message
        self.errno = errno

def retry(times,interval):
    """
     提供重试功能的
    :param times: 重试次数
    :param interval: 每次重试间隔，秒
    :return:

    如何使用：
    @retry(5,1)
    def test_add(self,a,b):
        #return a+b
        raise AppException("rraise execption")

    .....
    self.test_add(5,10)
    """

    def decorator(f):
        def decorated_function(*args, **kwargs):
            #print times,interval
            error=None
            for i in range(times):
              try:
                data=f(*args, **kwargs)
                return data
              except Exception as err:
                error=err.__str__()
                #print("try==error")
                #logger.warn(error)
              time.sleep(interval)
            if error is not None:
               raise AppException("retry {0} times,last err is {1}".format(times,error))
        return decorated_function
    return decorator

#####上面是正式代码
####下面是如何调用的示例代码,演示重试,重试五次，间隔一秒
@retry(5,1)
def retry_sample():
    return sample()


####下面是如何调用的示例代码,调用一次
def sample():
        #设置请求的参数，下面是慢查询的一个request
        #request的调用可以看具体的源码，仅仅需要看相关request部分就行，这些类仅仅需要看简单的get ,set方法就可以
        #参数的具体含义参考https://help.aliyun.com/document_detail/26223.html
        from aliyunsdkrds.request.v20140815.DescribeSlowLogRecordsRequest import DescribeSlowLogRecordsRequest
        request=DescribeSlowLogRecordsRequest()
        request.set_DBInstanceId('rdsx2y9yieqqer90yl2z')
        #下面可以故意输入错误的set_DBInstanceI=instanceiserror,这样可以模拟重试
        #request.set_DBInstanceId('instanceiserror')
        request.set_EndTime('2017-03-15T15:01Z')
        request.set_StartTime('2017-03-15T00:00Z')
        #request.set_StartTime(1)

        #访问阿里得到结果
        result=AliRds.get_result(request)
        #检查返回结果是否正确
        (ok,message)=AliRds.result_is_ok(result)
        
        #检查返回结果是否正确,下面是更加复杂的方法，会检查items[SQLSlowRecord]返回的数组是否为0，因为AliRds的bug问题
        #(ok,message)=AliRds.result_is_ok(result,["Items","SQLSlowRecord"])

        if ok is False:
            #访问阿里的有问题，抛出异常，
            #如果用retry功能，必须抛出异常，因为retry功能是通过异常来判断是否需要重试的
            raise AppException(message["Message"])

        #下面访问阿里得到正确的结果的处理逻辑
        print result


#####面是测试代码，可以忽略
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    #tests = unittest.TestLoader().discover('tests',pattern='mytest*.py')
    #pdb.set_trace()
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    #测试重试
    retry_sample()
    #测试单次运行
    #sample()
    #test()

