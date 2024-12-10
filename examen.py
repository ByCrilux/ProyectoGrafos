import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
class nodo:
    def __init__(self, nombre, ip, prox):
        self.nombre = nombre
        self.ip = ip
        self.prox = prox
        self.listaAdy = []

class grafo:
    def __init__(self):
        self.grafo = {}

    def insertar_nodo(self,cod, nombre, ip, prox):
        if ip not in self.grafo:
            self.grafo[cod] = nodo(nombre, ip, prox)

    def insertar_arista(self, origen, destino):
        if origen in self.grafo and destino in self.grafo:
            self.grafo[origen].listaAdy.append(destino)
            self.grafo[destino].listaAdy.append(origen)

    def que_equipo_tiene_conexion_a_internet(self, origen):
        visitados = set()
        equipos = set()
        self.dfs(origen, visitados, equipos)
        return list(equipos)
            
    def dfs(self, origen, visitados, equipos):
        visitados.add(origen)

        nodo_actual = self.grafo[origen]
        if (nodo_actual.ip.startswith("192.168.0.") or nodo_actual.prox is not None):
            equipos.add(origen)

        for destino in nodo_actual.listaAdy:
            if destino not in visitados:
                self.dfs(destino, visitados, equipos)
    
    def que_equipo_tiene_conexion_a_file_serv(self, origen):
        visitados = set()
        equipos = set()
        self.dfs1(origen, visitados, equipos)
        return list(equipos)
            
    def dfs1(self, origen, visitados, equipos):
        visitados.add(origen)

        nodo_actual = self.grafo[origen]
        if nodo_actual.ip.startswith("100.10.0.") or nodo_actual.prox is None:
            equipos.add(origen)

        for destino in nodo_actual.listaAdy:
            if destino not in visitados:
                self.dfs1(destino, visitados, equipos)
    
    def crear_grafo(self):
            G = nx.Graph()  # Crear un grafo no dirigido

            # Insertar los nodos
            for cod, nodo in self.grafo.items():
                G.add_node(cod, label=nodo.nombre)

            # Insertar aristas
            for origen, nodo in self.grafo.items():
                for destino in nodo.listaAdy:
                    G.add_edge(origen, destino)

            # Configurar la posición de los nodos
            pos = nx.spring_layout(G)  # Distribuir los nodos de manera visual

            # Crear la visualización
            plt.figure(figsize=(12, 12))

            # Dibujar los nodos
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')

            # Dibujar las aristas con desplazamientos aleatorios
            for u, v in G.edges():
                desplazamiento = random.uniform(-0.2, 0.2)
                nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                                    width=2, alpha=0.8,
                                    connectionstyle=f"arc3,rad={desplazamiento}", arrowsize=20)

            # Etiquetas en los nodos
            labelss = nx.get_node_attributes(G, 'label')
            nx.draw_networkx_labels(G, pos, labels=labelss, font_size=10, font_weight='bold')

            # Título
            plt.title("Grafo Completo con Conexiones")
            plt.show()



def graficar(lista):
    G = nx.Graph()
    
    #agregar nodod y aristas
    for nodo_id in lista:
        for adyacente in g.grafo[nodo_id].listaAdy:
            if adyacente in lista:
                G.add_edge(nodo_id, adyacente)

    #ponerle sus nombres
    labels = {nodo_id: g.grafo[nodo_id].nombre for nodo_id in lista}

    pos = nx.spring_layout(G)  # Distribuir los nodos visualmente
    plt.figure(figsize=(8, 6))

    #awui dibuja
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='blue', node_size=500, font_size=10, font_weight="bold")
    
    plt.title("Grafo con los nodos de la lista seleccionada")
    plt.show()
    
if __name__ == '__main__':

    g = grafo()
    g.insertar_nodo(0,'pc0','192.168.0.1','10.10.0.1')
    g.insertar_nodo(1,'pc1', '100.10.0.1', None)
    g.insertar_nodo(2,'pc2','192.168.0.2','10.10.0.1')
    g.insertar_nodo(3,'pc3', '192.168.0.3', '10.10.0.1')
    g.insertar_nodo(4,'pc4', '100.10.0.2', None)
    g.insertar_nodo(5,'pc5', '100.10.0.3', None)
    g.insertar_nodo(6,'pc6','192.168.0.5', '10.10.0.1')
    g.insertar_nodo(7,'pc7','192.168.0.4', '10.10.0.1')
    g.insertar_nodo(8, 'sur1', '100.10.0.4',None)
    g.insertar_nodo(9, 'sur2', '192.168.0.6','10.10.0.1')

    g.insertar_arista(0,1)
    g.insertar_arista(0,2)
    g.insertar_arista(2,3)
    g.insertar_arista(1,4)
    g.insertar_arista(4,3)
    g.insertar_arista(3,7)
    g.insertar_arista(7,6)
    g.insertar_arista(6,9)
    g.insertar_arista(6,5)
    g.insertar_arista(6,8)
    g.insertar_arista(4,5)
    g.insertar_arista(5,8)

    
    con_conexion = g.que_equipo_tiene_conexion_a_internet(1)
    sin_conexion = g.que_equipo_tiene_conexion_a_file_serv(1)
    print("nodos con conexión a internet:")
    for nodoa in con_conexion:
        print(f"{nodoa}: {g.grafo[nodoa].nombre} - {g.grafo[nodoa].ip}")


    print("nodos con conexión a servidor de archivos:")
    for nodoa in sin_conexion:
        print(f"{nodoa}: {g.grafo[nodoa].nombre} - {g.grafo[nodoa].ip}")

    g.crear_grafo()

    graficar(con_conexion)
    graficar(sin_conexion)