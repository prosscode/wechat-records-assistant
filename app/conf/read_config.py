# -*- coding: utf-8 -*-
# author:pross

import os
import configparser

# 得到上级目录路径
path = os.path.split(os.path.realpath(__file__))[0]
# 得到配置文件目录，配置文件目录为path下的\config.ini
config_path = os.path.join(path, 'db_config.ini')
# 调用配置文件读取
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')


class ReadConfig():

    def get_db_config(self, name):
        value = config.get('DATABASE_DEV', name)
        return value


if __name__ == '__main__':
    print(path)
    print('config_path', config_path)  # 打印输出config_path测试内容是否正确
    print('通过config.get拿到配置文件中DATABASE的host的对应值:', ReadConfig().get_db_config('password'))
