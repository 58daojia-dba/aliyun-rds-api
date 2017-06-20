# -*- coding: utf-8 -*-
from __future__ import print_function
import ConfigParser


"""
Constant类定义了用户名，密码
"""
class Constant(object):
    """
    版本号标识
    0.1.1 加入超时重试和判断返回结果数值是否为null（alirds bug）
    """
    CONFIG_DIR = '/etc/ali_key.conf'
    CONFIG_OPTIONS = ['version', 'user_key', 'user_secret', 'region_id', 'user_agent']

    # This stores the configuration for every opt
    default_config= dict()

    @staticmethod
    def load_config():
        if len(Constant.default_config) == 0:
            #print ("load")
            config_parser = ConfigParser.RawConfigParser()
            config_parser.read(Constant.CONFIG_DIR)
            if not config_parser.has_section('default'):
                raise AppException("could not find default section in file={0}".format(Constant.CONFIG_DIR))
            default_config = Constant.default_config
            try:
              for opt in Constant.CONFIG_OPTIONS:
                opt_value = config_parser.get('default', opt)
                default_config[opt] = opt_value
            except Exception as err:
                raise AppException("could not find key={0}".format(opt))


    @staticmethod
    def get_user_key():
        Constant.load_config()
        return Constant.default_config["user_key"]

    @staticmethod
    def get_user_secret():
        Constant.load_config()
        return Constant.default_config["user_secret"]

    @staticmethod
    def get_region_id():
        Constant.load_config()
        return Constant.default_config["region_id"]

    @staticmethod
    def get_user_agent():
        Constant.load_config()
        return Constant.default_config["user_agent"]

class AppException(Exception):
    """
      定义程序中的逻辑的异常
    """

    def __init__(self, message, errno=0):
        super(AppException, self).__init__()
        self.args = (message, errno)
        self.errmsg = message
        self.errno = errno
