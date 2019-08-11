# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
__date__ = '2019/7/27 0027 下午 11:14'

import os
import sys
import json
from credit_card_shopping.db import db_handler
# from credit_card_shopping.core.main import card_info
from credit_card_shopping.core import main
from credit_card_shopping.modules import accounts, transaction
from credit_card_shopping.log import logger
from credit_card_shopping.core.auth import login_required
from credit_card_shopping.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
log_path = settings.DATABASE["log_path"]
db_path = '%s/%s' % (settings.DATABASE['path'], settings.DATABASE['name'])


@login_required
def account_info(user_account):
    # 定义一个查看用户信息的函数
    username = user_account['account_data']['username']
    data = accounts.load_current_balance(username)
    print("\033[33;1m我的账户信息："
          "\n持卡人: %s "
          "\n卡号: %s"
          "\n存款: ￥%s"
          "\n可提现额度: ￥%s \033[0m"
          % (user_account['account_data']["username"], user_account['account_data']["cardid"], data["balance"],
             data["credit"]))
    input('\033[33;1m按任意键返回上一级菜单>>>:\033[0m')


@login_required
def repay(user_account):
    # 定义一个用户存款函数
    username = user_account['account_data']['username']
    account_data = accounts.load_current_balance(username)
    print("\033[33;1m您的当前存款为: ￥%s " % account_data["balance"])
    while True:
        repays = input('\033[33;1m请输入存款金额并确认存款，按Q取消存款>>>\033[0m')
        if repays.capitalize() == 'Q':
            break
        else:
            if repays.isdigit():
                repays = int(repays)
                transaction.make_transaction(account_data=account_data, tran_type="repay", amount=repays)
                break
            else:
                print('\033[31;1m请输入有效存款金额\033[0m')


@login_required
def withdraw(acc_data):
    """
    提现
    """
    account_data = accounts.load_current_balance(acc_data['account_data']['username'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1m输入提现金额，退出b:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(account_data=account_data, tran_type='withdraw',
                                                       amount=withdraw_amount)
            if new_balance:
                print('\033[42;1m余额为:%s\033[0m' % (new_balance['balance']))
            else:
                print('余额%s,不足' % acc_data['account_data']['balance'])
        else:
            print('\033[31;1m[%s] 输入有误，应该输入数字!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


@login_required
def transfer(user_account):
    # 定义一个用户转账的函数
    count = 0
    while count < 3:
        transfer = input('\033[33;1m请输入需转账人用户名,取消转账c>>>\033[0m')
        if transfer == 'c':
            break
        db_path_user1 = db_path + '\%s.json' % transfer  # 需被转账用户
        login_account_username = user_account['account_data']["username"]
        if transfer == login_account_username:
            print('\033[31;1m转账不能转给自己\033[0m')
        else:
            if os.path.isfile(db_path_user1):
                # 判断用户文件是否存在
                account_data_transfer = accounts.load_current_balance(transfer)  # 转账用户
                account_data_user = accounts.load_current_balance(login_account_username)  # 当前用户
                print('\033[33;1m转账用户信用卡号为:\033[0m \033[32;1m %s \033[0m' % transfer)
                while True:
                    inputs = input('\033[33;1m取消转账:按Q|q取消>>>\033[0m')
                    if inputs.capitalize() == 'Q':
                        break
                    money = input('\033[33;1m请输入需转账金额:\033[0m')
                    if money.isdigit():
                        money = int(money)
                        if money > account_data_user["balance"]:  # 判断转账金额是否大于存款
                            print('\033[31;1m对不起您的存款不足,无法转账\033[0m')
                        else:
                            print('\033[31;1m转账用户卡号: %s 转账金额:￥%s\033[0m'
                                  % (account_data_transfer["username"], money))
                            inputs = input('\033[33;1m请再次确认转账信息数据:按Q|q取消>>>\033[0m')
                            if inputs.capitalize() == 'Q':
                                break
                            else:
                                data = transaction.make_transaction(account_data=account_data_user,
                                                                    tran_type='transfer',
                                                                    amount=money)
                                print('ok')
                                if data:
                                    account_data_transfer['balance'] = account_data_transfer['balance'] + money
                                    accounts.dump_account(account_data_transfer)


                    else:
                        print('\033[31;1m请输入有效转账金额\033[0m')
            else:
                count += 1
                print('\033[31;1m该用户不存在,请重新输入还剩 %s 次机会\033[0m' % (3 - count))


def paycheck(user_account):
    """

    账单
    """
    if not os.path.isfile(log_path % (user_account['account_data']["username"], 'transactions.log')):
        print('\033[31;1m当前用户无流水记录\033[0m', log_path % (user_account['account_data']["username"], "transactions.log"))

    else:
        print(log_path % (user_account['account_data']["username"],"transactions.log"))
        with open(log_path % (user_account['account_data']["username"], 'transactions.log'), 'rb',
                  encoding='utf-8') as fh:
            for line in fh:
                print(line)
