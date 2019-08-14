# -*- coding:utf-8 -*-
__author__ = 'JUN SHANG'
from datetime import datetime
import hashlib
from credit_card_shopping.log import logger
from credit_card_shopping.conf.settings import user_login_authentication_count
from credit_card_shopping.modules import accounts


def login_required(func):
    """验证用户是否登录"""

    def wrapper(*args, **kwargs):
        # print('--wrapper--->',args,kwargs)
        if args[0].get('is_authenticated'):
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")

    return wrapper


def acc_auth2(account, password, retry):
    """用户认证"""
    data = accounts.load_current_balance(account)
    all_count = user_login_authentication_count
    # retry_count = user_login_authentication_count + 1
    if data:
        if data['password'] == password:
            exp_time_stamp = datetime.strptime(data['expire_date'], "%Y-%m-%d")
            if datetime.now() > exp_time_stamp:
                print("\033[31;1m用户 [%s] 已经过期了，请重新申请卡!\033[0m" % account)
                exit()
            elif data['status'] == 0:
                print("\033[31;1m用户 [%s] 已经冻结，请到相应的银行解冻!\033[0m" % account)
                exit()
            else:  # passed the authentication
                access_logger = logger.card_log(account, 'access')
                access_logger.info('%s用户进行登录%d次成功' % (account, retry))
                return data
        else:
            access_logger = logger.card_log(account, 'access')
            access_logger.info('%s用户进行登录,但是密码错误，还剩下%d次' % (account, all_count - retry))
            print("\033[31;1m密码错误，还剩下%d次\033[0m" % (all_count - retry))
    else:
        count = all_count - retry
        print('\033[31;1m用户名不存在，还剩下%d次\033[0m' % count)


def acc_login(user_data):
    """用户登录"""
    retry_count = 0
    while retry_count < user_login_authentication_count:
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        m = hashlib.md5()
        m.update(password.encode())
        pwd = m.hexdigest()
        auth = acc_auth2(account=account, password=pwd, retry=retry_count + 1)
        if auth:  # not None means passed the authentication
            print(auth, '登录成功')
            user_data['is_authenticated'] = True
            user_data['account_id'] = auth['cardid']
            print("welcome")
            return auth
        else:
            retry_count += 1
    else:
        print("用户登录太多次了，退出")

        exit()
