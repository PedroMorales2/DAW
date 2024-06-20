import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='bd_golden_store')