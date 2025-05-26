import psycopg2 as ps

def conexion_BBDD(nombre_BBDD, usuario, contraseña, anfitrion, puerto):

    conn = ps.connect(
                    dbname = nombre_BBDD, 
                    user = usuario,
                    password = contraseña,
                    host = anfitrion,
                    port = puerto)

    return conn

def ejecutor_querys(cur, query):
    cur.execute(query)
    return cur.fetchall()
