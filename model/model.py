import copy

from geopy.distance import geodesic
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.peso_max = 0
        self.best_path = None

    # GRAFO
    def buildGraph(self, year, shape):
        stati = DAO.getAllStates()
        self._graph.add_nodes_from(stati)
        for stato in stati:
            self._idMap[stato.id] = stato
        weighted_edges = DAO.getEdges(year, shape, self._idMap)
        self._graph.add_weighted_edges_from(weighted_edges)
        print(f"Grafo creato correttamente, il grafo ha {len(self._graph.nodes)} nodi e {len(self._graph.edges)} archi")

    def getVicini(self):
        diz_stato_peso = {}
        for stato in self._graph.nodes:
            diz_stato_peso[stato] = 0
            for vicino in nx.neighbors(self._graph, stato):
                peso = int(self._graph[stato][vicino]["weight"])
                diz_stato_peso[stato] += peso

        return diz_stato_peso

    def getYears(self):
        return DAO.getAllYears()

    def getShapes(self):
        return DAO.getAllShapes()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    # RICORSIONE
    def calcolaPercorso(self):
        self.best_path = []
        self.peso_max = 0

        for nodo_iniziale in self._graph.nodes:
            parziale = []
            self.ricorsione(nodo_iniziale, parziale, None, [nodo_iniziale])

        return self.best_path, self.peso_max

    def ricorsione(self, nodo_corrente, parziale, peso_precedente, parz_nodi):

        archi_ammissibili = self.getArchiViciniAmmiss(nodo_corrente, peso_precedente, parz_nodi)

        if not archi_ammissibili:
            peso_parziale = self.sommaDist(parziale)
            if peso_parziale > self.peso_max:
                self.peso_max = peso_parziale
                self.best_path = copy.deepcopy(parziale)

        for arco in archi_ammissibili:
            nodo_successivo = arco[1]
            parziale.append((arco, self.calcolaDist(arco[0], arco[1])))
            parz_nodi.append((arco[1]))
            self.ricorsione(nodo_successivo, parziale, arco[2]['weight'], parz_nodi)
            parziale.pop()
            parz_nodi.pop()
        return

    def getArchiViciniAmmiss(self, nodo, peso_precedente, parz_nodi):
        archi_vicini = self._graph.edges(nodo, data=True)
        archi_vicini_ammis = []
        for arco in archi_vicini:
            if peso_precedente is None or (arco[2]['weight'] > peso_precedente and arco[1] not in parz_nodi):
                archi_vicini_ammis.append(arco)
        # archi_vicini_ammis.sort(key=lambda x: x[2]['weight'])
        return archi_vicini_ammis

    def sommaDist(self, parziale):
        sum_dist = 0
        for arco, dist in parziale:
            sum_dist += self.calcolaDist(arco[0], arco[1])
        return sum_dist

    def calcolaDist(self, s1, s2):
        distance = geodesic((s1.Lat, s1.Lng), (s2.Lat, s2.Lng)).kilometers
        return distance
