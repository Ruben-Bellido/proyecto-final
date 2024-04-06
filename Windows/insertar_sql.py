import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tiempo"
)


def insertar():
    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    # Consulta SQL para insertar datos
    consulta_sql = "INSERT INTO `tiempo`.`temperaturas`(`Maxima`,`Minima`,`ciudad`,`latitud`,`longitud`)VALUES(%s, %s, %s,%s, %s)"
    datos_a_insertar = (12.1, 3.0,'Prueba',45.6,36.4)

    try:
        # Ejecutar la consulta para cada conjunto de datos a insertar
        cursor.executemany(consulta_sql, datos_a_insertar)

        # Confirmar la transacción
        conexion.commit()
        print("Datos insertados correctamente.")

    except mysql.connector.Error as error:
        # En caso de error, deshacer la transacción
        conexion.rollback()
        print(f"No se pudo insertar datos: {error}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

insertar()