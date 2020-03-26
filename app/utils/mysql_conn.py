# -*- coding: utf-8 -*-
# author:pross

from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接
    获取连接对象:conn = Mysql.getConn()
    释放连接对象:conn.close()
    """
    # 连接池对象
    __pool = None

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，生成操作游标
        self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(cls):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if Mysql.__pool is None:
            __pool = PooledDB(creator=pymsql,
                              mincached=1,
                              maxcached=20,
                              use_unicode=False,
                              cursorclass=DictCursor,
                              host=db_config.DBHOST,
                              port=db_config.DBPORT,
                              user=db_config.DBUSER,
                              passwd=db_config.DBPWD,
                              db=db_config.DBNAME,
                              charset=db_config.DBCHAR
                              )
        return __pool.connection()
