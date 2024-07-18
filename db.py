import psycopg2
from psycopg2 import pool

# Crear un pool de conexiones
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    database ="biblioteca3a",
    user="postgres",
    password="gnieva",
    host="localhost",
    port="5432"
)

def conectar():
    return connection_pool.getconn()

def desconectar(conn):
    connection_pool.putconn(conn)
