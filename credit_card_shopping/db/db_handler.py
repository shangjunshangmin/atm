# -*- coding: utf-8 -*-
__author__ = 'JUN SHANG'
import json, time, os
from credit_card_shopping.conf import settings


def file_db_handle(conn_params):
    """选择读取文件"""
    # print('file db:', conn_params)
    # db_path ='%s/%s' %(conn_params['path'],conn_params['name'])
    return file_execute


def db_handler():
    """根据settings中的配置选择读取文件还是mysql数据库"""
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass  # todo


def file_execute(sql, **kwargs):
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])

    # print(sql, db_path)
    sql_list = sql.split("where")
    # print(sql_list)
    if sql_list[0].startswith("select") and len(sql_list) > 1:  # has where clause
        column, val = sql_list[1].strip().split("=")

        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            # print(account_file)
            if os.path.isfile(account_file):

                with open(account_file, 'rb') as f:
                    account_data = json.load(f)
                    return account_data
            else:
                print('没有这个用户，请重新输入')

    elif sql_list[0].startswith("update") and len(sql_list) > 1:  # has where clause
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")
                with open(account_file, 'w') as f:
                    json.dump(account_data, f)
                return True
