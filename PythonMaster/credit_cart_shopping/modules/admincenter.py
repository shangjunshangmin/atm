# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
__date__ = '2019/7/27 0027 下午 11:14'
import os, sys
from credit_card_shopping.core.auth import login_required
from credit_card_shopping.modules import accounts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
db_path = BASE_DIR + r'\db\user_info'


@login_required
def banks(account):
    # 定义一个查询发行信用卡函数
    print('\033[33;1m尊敬的用户您的发行信用卡是%s'
          '\n卡号为:%s,开户日期为:%s,信用卡有效期至:%s'
          '\n我们将会真挚的为您服务！！！'
          % (account['account_data']['cardname'], account['account_data']["cardid"], account["enroll_date"], account["expire_date"]))


@login_required
def freezing(account):
    # 定义一个冻结信用卡函数
    username = account['account_data']['username']
    data = accounts.load_current_balance(username)
    if data['status'] == 0:
        print('\033[31;1m当前信用卡已冻结\033[0m')
    if data['status'] == 1:
        free = input('\033[33;1m当前信用卡未冻结,按任意键选择冻结 按b返回>>>\033[0m')
        if free != 'b':
            data['status'] = 0
            accounts.dump_account(data)
            print('\033[31;1m当前信用卡已冻结\033[0m')


@login_required
def defrosting(account):
    # 定义一个解冻函数
    username = account['account_data']['username']
    data = accounts.load_current_balance(username)
    if data['status'] == 1:
        print('\033[31;1m当前信用卡未冻结\033[0m')
    if data['status'] == 0:
        free = input('\033[33;1m当前信用卡已冻结,按任意键选择解冻 按b返回>>>\033[0m')
        if free != 'b':
            data['status'] = 1
            accounts.dump_account(data)
            print('\033[31;1m当前信用卡已冻结\033[0m')


@login_required
def limit(account):
    # 定义一个提升信用额度函数
    username = account['account_data']['username']
    data = accounts.load_current_balance(username)
    print('\033[33;1m尊敬的用户您当前信用额度是 %s元' % data["credit"])
    limit = input('\033[34;1m是否选择提升信用额度  按任意键确认提示  按Q取消提升>>>')
    if limit.capitalize() != 'Q':
        while True:
            lines = input('\033[35;1m请输入提升信用额度>>>\033[0m')
            if lines.isdigit():
                lines = int(lines)
                if lines <= 2000:
                    limits = data['credit'] + lines
                    accounts.dump_account(data)
                    print('\033[31;1m当前信用额度提升为：%s元 \033[0m' % limits)
                    break
                else:
                    print('\033[31;1m提升额度超出提升范围\033[0m')
            else:
                print('\033[31;1m请输入有效提升额度\033[0m')
