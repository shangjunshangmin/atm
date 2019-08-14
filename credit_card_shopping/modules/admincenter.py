# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'

import os
import sys
import hashlib
import json
from datetime import datetime, timedelta
from credit_card_shopping.modules import accounts
from credit_card_shopping.core.auth import login_required
from credit_card_shopping.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
db_path = BASE_DIR + r'\db\accounts'
now_username = ''


def choice_user():
    """
     选择需要操作的用户名

    """
    while True:
        user_account = []
        db_accounts_path = os.path.join(settings.DATABASE['path'], settings.DATABASE['name'])
        db_accounts_files = os.listdir(db_accounts_path)
        for i in db_accounts_files:
            data = accounts.load_current_balance(i.split('.')[0])
            if data['type'] == 0:
                user_account.append(data['username'])
        user_choice_number = []
        print('''\033[31;0m------------请选择需要操作的账户-----------\033[0m''')
        for number in range(len(user_account)):
            user_choice_number.append(number)
            print('%s : %s' % (number, user_account[number]))
        user_choice = input('\033[35;1m请选择操作用户>>>:\033[0m').strip()
        if user_choice.isdigit() and int(user_choice) in user_choice_number:
            acknowledgement = input('再次确认是否是这个用户%s,选择b重新选择，选择c退出这项操作，其它任意键确认' % user_account[int(user_choice)])
            if acknowledgement == 'b':
                print('重新选择用户')
            elif acknowledgement == 'c':
                print('退出这项操作，重新选择')
            else:
                global now_username
                now_username = user_account[int(user_choice)]
                break

        else:
            print('\033[31;1m请输入有效操作方式\033[0m')


@login_required
def banks(account):
    # 定义一个查询发行信用卡函数
    while True:
        reconfirm = input('\033[33;1m请再次确认是否发放信用卡，按b取消，其它任意键确认>>>\033[0m')
        if reconfirm == 'b':
            break
        db_accounts_path = os.path.join(settings.DATABASE['path'], settings.DATABASE['name'])
        # db_accounts_files = os.listdir(db_accounts_path)
        # user_file_name = []
        # for user_file in db_accounts_files:
        #     user_file_name.append(user_file.split('.')[0])
        username = input('\033[33;1m请输入信用卡用户名>>>\033[0m').lower()
        password = input('\033[33;1m请输入信用卡用户名>>>\033[0m').lower()
        m = hashlib.md5()
        m.update(password.encode())
        pwd = m.hexdigest()
        user_file_path = os.path.join(db_accounts_path, '%s.json' % username)
        if os.path.isfile(user_file_path):
            print('用户已经存在，请重新输入用户名')
            continue
        else:
            user_file_content = {"type": 0, "status": 1, "credit": 15000, 'pay_day': 22,
                                 "enroll_date": datetime.now().strftime('%Y-%m-%d'),
                                 'cardid': 123, 'password': pwd, 'username': username,
                                 "balance": 15000,
                                 "expire_date": (datetime.now() + timedelta(weeks=24)).strftime('%Y-%m-%d'),
                                 "cardname": '招商银行'}
            with open(user_file_path, 'w') as f:
                json.dump(user_file_content, f)
                print('\033[33;1m尊敬的用户您的发行信用卡是%s'
                      '\n卡号为:%s,开户日期为:%s,信用卡有效期至:%s'
                      '\n我们将会真挚的为您服务！！！'
                      % (user_file_content["cardname"], user_file_content["cardid"], user_file_content["enroll_date"],
                         user_file_content["expire_date"]))
                break


@login_required
def freezing(account):
    # 定义一个冻结信用卡函数
    choice_user()
    username = now_username
    if username:
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
    choice_user()
    username = now_username
    if username:
        data = accounts.load_current_balance(username)
        if data['status'] == 1:
            print('\033[31;1m当前信用卡未冻结\033[0m')
        if data['status'] == 0:
            free = input('\033[33;1m当前信用卡已解冻,按任意键选择解冻 按b返回>>>\033[0m')
            if free != 'b':
                data['status'] = 1
                accounts.dump_account(data)
                print('\033[31;1m当前信用卡已解冻\033[0m')


@login_required
def limit(account):
    # 定义一个提升信用额度函数
    choice_user()
    username = now_username
    if username:
        data = accounts.load_current_balance(username)
        print('\033[33;1m尊敬的用户您当前信用额度是 %s元' % data["credit"])
        limit = input('\033[34;1m是否选择提升信用额度  按任意键确认提示  按Q取消提升>>>')
        if limit.capitalize() != 'Q':
            while True:
                lines = input('\033[35;1m请输入提升信用额度>>>\033[0m')
                if lines.isdigit():
                    lines = int(lines)
                    if lines <= 2000:
                        data['credit'] = data['credit'] + lines
                        accounts.dump_account(data)
                        print('\033[31;1m当前信用额度提升为：%s元 \033[0m' % data['credit'])
                        break
                    else:
                        print('\033[31;1m提升额度超出提升范围\033[0m')
                else:
                    print('\033[31;1m请输入有效提升额度\033[0m')
