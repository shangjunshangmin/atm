# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
from credit_card_shopping.conf import settings

import logging, sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def card_log(username, log_type):
    # 定义一个信用卡日志函数
    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = settings.DATABASE['log_path'] % (username, settings.LOG_TYPES[log_type])
    log_directory=settings.DATABASE['log_directory']%(username,)
    print(log_directory)
    print('日志文件地址',log_file)
    if not os.path.isdir(log_directory):
        os.makedirs(log_directory)

    fh = logging.FileHandler(log_file)

    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def shop_log(username, log):
    # 定义一个购物日志函数
    log_path = settings.shop_log_path % username

    logger = logging.getLogger('shopping')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_path, encoding='utf-8')
    fh.setLevel(logging.INFO)

    fh_format = logging.Formatter('%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    fh.setFormatter(fh_format)

    logger.addHandler(fh)
    logger.info(log)

    logger.removeHandler(fh)
