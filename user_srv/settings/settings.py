from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

#使用peewee的连接池，使用mixin防止连接断开
class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


MYSQL_DB = "yuan_user_srv"
MYSQL_HOST = "192.168.150.130"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

db = ReconnectMysqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)
