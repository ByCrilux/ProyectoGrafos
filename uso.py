import mysql.connector
from grafo import GrafoTransacciones


try:
    c = mysql.connector.connect(
        host="localhost",   
        user="root",   
        password="ByCrilux",  
        database="cuentasBancarias" 
    )
    
    if c.is_connected():
        print("Conexión exitosa a la base de datos MySQL.")
except mysql.connector.Error as err:
    print(f"Error: {err}")



#crar cuentas
grafo = GrafoTransacciones()
cur = c.cursor()
cur.execute('select * from cuenta')
tabla = cur.fetchall()

for t in tabla:
    grafo.insertar_cuenta(t[0],t[1])

cur.execute('select desde, hacia, importe from transaccion')
tabla = cur.fetchall()

for t in tabla:
    grafo.insertar_transaccion(t[0], t[1], t[2])

#setectar transferencias repetitivas
umbral_frecuencia = 2
umbral_monto = 1200
patrones = grafo.detectar_transferencias_repetitivas(umbral_frecuencia, umbral_monto)
print("Transferencias sospechosas detectadas:")
for patron in patrones:
    print(f"Transferencias sospechosas de {patron[0]} a {patron[1]} con frecuencia: {patron[2]}")

 
umbral_anomalia = 4999
anomalias_dfs_directas = grafo.dfs_detectar_anomalias_directas(umbral_anomalia)
print("Anomalías directas detectadas con DFS:")
for anomalia in anomalias_dfs_directas:
    print(f"Transacción sospechosa de {anomalia[0]} a {anomalia[1]} con monto: {anomalia[2]}")

anomalias_bfs_directas = grafo.bfs_detectar_anomalias_directas(umbral_anomalia)
print("Anomalías directas detectadas con BFS:")
for anomalia in anomalias_bfs_directas:
    print(f"Transacción sospechosa de {anomalia[0]} a {anomalia[1]} con monto: {anomalia[2]}")


grafo.pr1(111)
