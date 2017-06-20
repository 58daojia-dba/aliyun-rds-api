# -*- coding: utf-8 -*-
"""
提供任务状态表的audit_task的mysql层访问
对外暴露的方法会自己维护数据库连接（自己打开关闭连接）
 v0.1.0  2016/07/20  yilai    created
"""

from __future__ import print_function
import time,os
import datetime
import re
import logging
import pymysql
from logging.handlers import RotatingFileHandler
from func import init_logger,print_stack
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest
from ali_rds import AliRds,AppException


def test():
    import unittest
    logfilename = "test.log"
    init_logger(logfilename, logging.DEBUG)
    tests = unittest.TestLoader().discover('tests', pattern='test_ali_rds.py')
    #tests = unittest.TestLoader().discover('tests', pattern='test_config_helper.py')
    #pdb.set_trace()
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    #main()
    test()