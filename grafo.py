from nodo import Nodo
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random

class GrafoTransacciones:
    def __init__(self):
        self.cuentas = {}

    def insertar_cuenta(self, id_cuenta, nombre_prop): #nodo
        if id_cuenta not in self.cuentas:
            self.cuentas[id_cuenta] = Nodo(id_cuenta, nombre_prop)
            return True
        return False
    
    def get_nombre_cuenta(self, id_cuenta):
        if id_cuenta in self.cuentas:
            return self.cuentas[id_cuenta].nombre_cuenta

    def eliminar_cuenta(self, id_cuenta):
        if id_cuenta in self.cuentas:
            del self.cuentas[id_cuenta]
            for cuenta in self.cuentas.values():
                cuenta.transacciones = [tx for tx in cuenta.transacciones if tx[0] != id_cuenta]
            return True
        return False

    def insertar_transaccion(self, desde, hacia, monto):#arista
        if desde in self.cuentas and hacia in self.cuentas:
            self.cuentas[desde].transacciones.append((hacia, monto))
            return True
        return False

    def eliminar_transaccion(self, desde, hacia):
        if desde in self.cuentas:
            self.cuentas[desde].transacciones = [tx for tx in self.cuentas[desde].transacciones if tx[0] != hacia]
            return True
        return False

    def detectar_transferencias_repetitivas(self, umbral_frecuencia, umbral_monto):
        patrones_sospechosos = []

        for cuenta in self.cuentas.values():
            transferencias = {}
            for destino, monto in cuenta.transacciones:
                if monto >= umbral_monto:
                    if destino not in transferencias:
                        transferencias[destino] = 0
                    transferencias[destino] += 1

            for destino, frecuencia in transferencias.items():
                if frecuencia > umbral_frecuencia:
                    patrones_sospechosos.append((cuenta.id_cuenta, destino, frecuencia))

        return patrones_sospechosos

    def dfs(self, cuenta, visitados, anomalias, umbral, cuentas):
        visitados.add(cuenta)
        for destino, monto in cuentas[cuenta].transacciones:
            if monto > umbral:
                anomalias.add((cuenta, destino, monto))
            if destino not in visitados:
                self.dfs(destino, visitados, anomalias, umbral, cuentas)

    def dfs_detectar_anomalias_directas(self, umbral):
        visitados = set()
        anomalias = set()
        for inicio in self.cuentas:
            self.dfs(inicio, visitados, anomalias, umbral, self.cuentas)

        return list(anomalias)
    
    def bfs_detectar_anomalias_directas(self, umbral):
        lis = set()
        for inicio in self.cuentas:
            visitados = set()
            cola = [inicio]
            anomalias = set()

            while cola:
                cuenta = cola.pop(0)
                if cuenta not in visitados:
                    visitados.add(cuenta)
                    for destino, monto in self.cuentas[cuenta].transacciones:
                        if monto > umbral:
                            anomalias.add((cuenta, destino, monto))
                        cola.append(destino)
            lis.update(anomalias) #update para evitar duplicados
        
        return list(lis)
    
    def pr1(self, inicio):
        mst = {}
        if inicio not in self.cuentas:
            return None
        for nro, monto in self.cuentas[inicio].transacciones:
            if nro not in mst:
                mst[nro] = (nro, monto)
            else:
                nroActual, montActual = mst[nro]
                if monto >= montActual:
                    mst[nroActual] = (nroActual, monto)

        G = nx.MultiDiGraph()
        G.add_node(inicio, label=self.get_nombre_cuenta(inicio))
        for cuentas in mst.values():
            id_cuenta = cuentas[0]
            G.add_node(id_cuenta, label=self.get_nombre_cuenta(id_cuenta))

        i = 0
        edge_labels = {}  #pesos)
        for transaccion in mst.values():
            G.add_edge(inicio, transaccion[0], weight=float(transaccion[1]), key=i)
            edge_labels[(inicio, transaccion[0], i)] = transaccion[1] 
            i += 1

        pos = nx.circular_layout(G)
        plt.figure(figsize=(12, 12))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')

        # trazar las aristas con un pequeño desplazamiento
        for u, v, key, data in G.edges(data=True, keys=True):
            desplazanmiento = random.uniform(-0.2, 0.2)  # Un desplazamiento aleatorio pequeño

            # Dibujar la arista con el desplazamiento aplicado
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v, key)], width=1, alpha=0.9, edge_color='gray', 
                                connectionstyle=f"arc3,rad={desplazanmiento}", arrowsize=20, arrows=True)

        # Aseguramos que los nodos de G tengan el atributo 'label'
        for cuenta_id in G.nodes():
            if cuenta_id in self.cuentas:
                G.nodes[cuenta_id]['label'] = self.cuentas[cuenta_id].nombre_cuenta
        # Etiquetas de los nodos (mostrando el nombre de la cuenta en lugar del número de la cuenta)
        labelss = nx.get_node_attributes(G, 'label')  # Obtenemos el nombre de la cuenta
        nx.draw_networkx_labels(G, pos, labels=labelss, font_size=7, font_weight='bold')

        # Etiquetas de las aristas (pesos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

        plt.title("Grafo de Transacciones Bancarias")
        plt.show()


    def crear_grafo(self):
        G = nx.MultiDiGraph()       
        #insertar los nodos
        for cuenta in self.cuentas.values():
            G.add_node(cuenta.id_cuenta)
        
        #insertar aritas
        for cuenta in self.cuentas.values():
            for i, transaccion in enumerate(cuenta.transacciones):
                hacia, monto = transaccion
                G.add_edge(cuenta.id_cuenta, hacia, weight=float(monto), key=i)

        #graficar el grafo
        pos = nx.circular_layout(G)  #guarda los nodos
        plt.figure(figsize=(12, 12))

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')# este dibuja los nodos

        # Dibujar las aristas con un pequeño desplazamiento
        for u, v, key, data in G.edges(data=True, keys=True):
            desplazamiento = random.uniform(-0.2, 0.5)  #desplazamiento aleatorio pequeño

            nx.draw_networkx_edges(G, pos, edgelist=[(u, v, key)], width=1, alpha=0.9, edge_color='gray', 
                                   connectionstyle=f"arc3,rad={desplazamiento}", arrowsize=20, arrows=True)

            for cuenta_id in G.nodes():
                if cuenta_id in self.cuentas:
                    G.nodes[cuenta_id]['label'] = self.cuentas[cuenta_id].nombre_cuenta + '-' + str(self.cuentas[cuenta_id].id_cuenta)

            labelss = nx.get_node_attributes(G, 'label')  # Obtenemos el nombre de la cuenta
        nx.draw_networkx_labels(G, pos,labels=labelss, font_size=7, font_weight='bold')
        plt.title("Grafo de Transacciones")
        plt.show()

    def gradoUsuarioSaliente(self, origen):
        '''# Crear un grafo dirigido (MultiDiGraph permite múltiples aristas entre los mismos nodos)
        G = nx.MultiDiGraph()
        
        # Insertar nodos con nombre de cuenta como atributo
        for cuenta in self.cuentas.values():
            # Aquí agregamos el nombre como atributo 'label' del nodo
            G.add_node(cuenta.id_cuenta, label=cuenta.nombre_cuenta)
        
        # Insertar aristas (transacciones) con un peso
        for cuenta in self.cuentas.values():
            for i, transaccion in enumerate(cuenta.transacciones):
                hacia, monto = transaccion
                # Agregar cada transacción con un peso distinto y clave única para cada transacción
                G.add_edge(cuenta.id_cuenta, hacia, weight=float(monto), key=i)  # Usamos 'key' para diferenciarlas'''

        # Verificamos si el nodo 'origen' existe en el grafo
        if origen in self.cuentas:
            # Obtener las transacciones salientes
            transacciones_salientes = [transaccion for transaccion in self.cuentas[origen].transacciones]
        
            # Crear un grafo solo con las transacciones salientes del nodo origen
            G1 = nx.MultiDiGraph()

            # Insertar las transacciones salientes al grafo G1
            for destino, monto in transacciones_salientes:
                # Agregar cada transacción al grafo G1, con un peso único
                G1.add_edge(origen, destino, weight=float(monto))

            # Graficar el grafo con las transacciones salientes
            pos = nx.circular_layout(G1)  # Disposición de los nodos (podrías usar circular_layout también)

            plt.figure(figsize=(12, 12))  # Ajusté el tamaño de la figura

            # Dibujar los nodos con color y tamaño de círculo adecuado
            nx.draw_networkx_nodes(G1, pos, node_size=1000, node_color='lightblue')

            # Dibujar las aristas con un pequeño desplazamiento (si deseas un efecto visual diferente)
            for u, v, key, data in G1.edges(data=True, keys=True):
                # Crear un pequeño desplazamiento en las aristas para que no se sobrepongan
                displacement = random.uniform(-0.2, 0.5)  # Un desplazamiento aleatorio pequeño

                # Dibujar la arista con el desplazamiento aplicado
                nx.draw_networkx_edges(G1, pos, edgelist=[(u, v, key)], width=1, alpha=0.9, edge_color='gray', 
                                       connectionstyle=f"arc3,rad={displacement}", arrowsize=40, arrows=True)

            # Aseguramos que los nodos de G1 tengan el atributo 'label'
            for cuenta_id in G1.nodes():
                if cuenta_id in self.cuentas:
                    G1.nodes[cuenta_id]['label'] = self.cuentas[cuenta_id].nombre_cuenta

            # Etiquetas de los nodos (mostrando el nombre de la cuenta en lugar del número de la cuenta)
            labelss = nx.get_node_attributes(G1, 'label')  # Obtenemos el nombre de la cuenta
            nx.draw_networkx_labels(G1, pos, labels=labelss, font_size=7, font_weight='bold')

            plt.title(f"Grafo de Transacciones Bancarias para el nodo {origen}")
            plt.show()

    def gradoUsuarioEntrante(self, destino):
        '''G = nx.MultiDiGraph()
        #insertar nodos en G
        for cuenta in self.cuentas.values():
            G.add_node(cuenta.id_cuenta, label=cuenta.nombre_cuenta)
        
        #insertar arista
        for cuenta in self.cuentas.values():
            for i, transaccion in enumerate(cuenta.transacciones):
                hacia, monto = transaccion
                G.add_edge(cuenta.id_cuenta, hacia, weight=float(monto), key=i)'''

        #existe el destino en las cuentas?
        if destino in self.cuentas:
            transacciones_entrantes = []
            for cuenta in self.cuentas.values():
                #filtrado de cuentas destino 
                transacciones_entrantes.extend([(cuenta.id_cuenta, monto) for (hacia, monto) in cuenta.transacciones if hacia == destino])
        
            # Crear un grafo solo con las transacciones entrantes al nodo destino
            G1 = nx.MultiDiGraph()

            # Insertar las transacciones entrantes al grafo G1
            for origen, monto in transacciones_entrantes:
                # Agregar cada transacción al grafo G1, con un peso único
                G1.add_edge(origen, destino, weight=float(monto))

            # Aseguramos que los nodos de G1 tengan el atributo 'label'
            for cuenta_id in G1.nodes():
                if cuenta_id in self.cuentas:
                    G1.nodes[cuenta_id]['label'] = self.cuentas[cuenta_id].nombre_cuenta

            # Graficar el grafo con las transacciones entrantes
            pos = nx.circular_layout(G1)  # Disposición de los nodos (podrías usar circular_layout también)

            plt.figure(figsize=(12, 12))  # Ajusté el tamaño de la figura

            # Dibujar los nodos con color y tamaño de círculo adecuado
            nx.draw_networkx_nodes(G1, pos, node_size=500, node_color='lightblue')

            # Dibujar las aristas con un pequeño desplazamiento (si deseas un efecto visual diferente)
            for u, v, key, data in G1.edges(data=True, keys=True):
                # Crear un pequeño desplazamiento en las aristas para que no se sobrepongan
                displacement = random.uniform(-0.2, 0.5)  # Un desplazamiento aleatorio pequeño

                # Dibujar la arista con el desplazamiento aplicado
                nx.draw_networkx_edges(G1, pos, edgelist=[(u, v, key)], width=1, alpha=0.9, edge_color='gray', 
                                       connectionstyle=f"arc3,rad={displacement}", arrowsize=20, arrows=True)

            # Etiquetas de los nodos (mostrando el nombre de la cuenta en lugar del número de la cuenta)
            labels = nx.get_node_attributes(G1, 'label')  # Ahora debería contener los nombres
            nx.draw_networkx_labels(G1, pos, labels=labels, font_size=12, font_weight='bold')

            plt.title(f"Grafo de Transacciones Entrantes para el nodo {destino}")
            plt.show()
        

