import configparser
from pathlib import Path

import pymysql
from decimal import Decimal
from datetime import datetime
import pymongo

BASE_DIR = Path(__file__).parent.parent.parent

config = configparser.RawConfigParser()
config.read(BASE_DIR / 'uwsgi/settings.ini', encoding="utf-8-sig")
DB_HOST = config['MYSQL']['host']
DB_USER = config['MYSQL']['user']
DB_PASSWORD = config['MYSQL']['password']
DB_PORT = config['MYSQL']['port']
DB_NAME = config['MYSQL']['db']


class Mongodb:
    _host = '139.9.47.194'
    _port = 27017
    _user = 'root'
    _passwd = 'Lucky9527*'
    _database = 'jt'

    @classmethod
    def connect(cls, host=None, user=None, password=None, port=None, db=None):
        h = Mongodb._host if host is None else host
        p = Mongodb._port if port is None else port
        u = Mongodb._user if user is None else user
        pwd = Mongodb._passwd if password is None else password
        d = Mongodb._database if db is None else db
        cli = pymongo.MongoClient(host=h, port=p, username=u, password=pwd, authSource=d)
        db = cli[d]
        return db


class MySQL:
    _ip = DB_HOST
    _user = DB_USER
    _passwd = DB_PASSWORD
    _port = DB_PORT
    _database = ""

    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    @classmethod
    def connect(cls, ip=None, user=None, passwd=None, port=None, database=None,
                ss_cursor=False):
        params = dict()
        params['host'] = MySQL._ip if ip is None else ip
        params['user'] = MySQL._user if user is None else user
        params['passwd'] = MySQL._passwd if passwd is None else passwd
        params['port'] = int(MySQL._port) if port is None else int(port)
        params['db'] = MySQL._database if database is None else database
        params['charset'] = 'utf8'
        if ss_cursor:
            params['cursorclass '] = pymysql.cursors.SSCursor
        db = pymysql.connect(**params)
        ret = cls(db)
        return ret

    def run(self, sql):
        print('excute sql:', sql, sep='\n')
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except pymysql.MySQLError as e:
            print(e)
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def execute(self, sql):
        print('excute sql:', sql, sep='\n')
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except pymysql.MySQLError as e:
            print(e)
            self.db.rollback()
            return False

    def select(self, sql: str, hold: bool = False):
        try:
            self.cursor.execute(sql)
            while 1:
                row = self.cursor.fetchone()
                if row is not None:
                    yield row
                else:
                    break
        except pymysql.MySQLError as e:
            print(e)
        finally:
            if not hold:
                self.db.close()

    def count(self, sql: str, hold: bool = False) -> int:
        cnt = 0
        for row in self.select(sql, hold):
            cnt += 1
        return cnt

    def close(self):
        self.db.close()

    @classmethod
    def make_insert_sql(cls, db, table, inputdata):
        """输入表名、一条list记录，返会insert SQL"""
        sql = f"insert into {db}.{table} values("
        i = 1
        for data in inputdata:
            col = "''"
            if data is None:
                col = 'null'
            elif isinstance(data, int) or isinstance(data, float) or isinstance(
                    data, Decimal):
                col = f"{data}"
            elif isinstance(data, str):
                col = f"'{data}'"
            elif isinstance(data, datetime):
                col = f"'%s'" % data.strftime('%Y-%m-%d %H:%M:%S')
            sql = sql + col
            if i != len(inputdata):
                sql = sql + ','
            i += 1
        sql = sql + ');'
        return sql
