# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
__date__ = '2019/7/27 0027 下午 11:36'
from credit_card_shopping.conf import settings
from credit_card_shopping.modules import accounts
from credit_card_shopping.log import logger

from credit_card_shopping.core import main
# transaction logger


def make_transaction( account_data, tran_type, amount, **others):
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:

        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
            account_data['balance'] = new_balance
            accounts.dump_account(account_data)
            logger.card_log(account_data['username'], 'transaction').info(
                "用户:%s   操作:%s    金额:%s   利息:%s" %
                (account_data['username'], tran_type, amount, interest))
            return account_data
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest
            # check credit
            if new_balance < 0:
                print('''\033[31;1m账号[%s] 不够 [-%s], 你现在的余额：
                [%s]''' % (account_data['username'], (amount + interest), old_balance))
                logger.card_log(account_data['username'], 'transaction').info(
                    "用户:%s  操作:%s  金额:%s   利息:%s 现在账户余额：%s 不够" %
                    (account_data['username'], tran_type, amount, interest,account_data['balance']))
            else:
                account_data['balance'] = new_balance
                accounts.dump_account(account_data)  # save the new balance back to file
                logger.card_log(account_data['username'], 'transaction').info(
                    "用户:%s   操作:%s    金额:%s   利息:%s" %
                    (account_data['username'], tran_type, amount, interest))
                return account_data
    else:
        print("交易类型 [%s] 不存在!" % tran_type)
