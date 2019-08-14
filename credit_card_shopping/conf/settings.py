# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_directory=BASE_DIR + r'\log\card_log'
print(log_directory)
DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR,
    "log_path": BASE_DIR + r'\log\card_log\%s_log/%s',
    'log_directory': BASE_DIR + r'\log\card_log\%s_log'
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},

}
# 用户登录验证次数
user_login_authentication_count = 3
# 商品存放地址
shop_path = BASE_DIR + r'\db\product_list'
# 购物车存放地址
shop_car_path = BASE_DIR + r'\db\shop_car\%s_shopcar.txt'
shop_log_path=BASE_DIR + r'\log\shop_log\%s_shop.log'
