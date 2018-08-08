#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

import os
import time
import logging
import configparser

class LogHelper():
    """
    初始化logger，读取目录及文件名称
    """
    def __init__(self):
        configoper = configparser.ConfigParser()
        configoper.read('config.py', encoding='utf-8')
        self.logdir_name = configoper['loginfo']['logdir_name']
        self.logfile_name = configoper['loginfo']['logfile_name']

    def create_dir(self):
        """
        创建目录
        :return: 文件名称
        """
        _LOGDIR = os.path.join(os.path.dirname(__file__), self.logdir_name)
        _TIME = time.strftime('%Y-%m-%d', time.gmtime()) + '-'
        _LOGNAME = _TIME + self.logfile_name
        LOGFILENAME = os.path.join(_LOGDIR, _LOGNAME)
        if not os.path.exists(_LOGDIR):
            os.mkdir(_LOGDIR)
        return LOGFILENAME

    def create_logger(self, logfilename):
        """
        创建logger对象
        :param logfilename:
        :return: logger对象
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logfilename)
        handler.setLevel(logging.INFO)
        formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formater)
        logger.addHandler(handler)
        return logger
