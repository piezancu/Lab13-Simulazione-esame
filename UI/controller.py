import flet as ft

from UI.view import View
from database.DAO import DAO
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getYears()
        self._listShape = DAO.getAllShapes()
        self.anno = None
        self.forma = None

    def fillDD(self):
        for year in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(year))

        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))

        self._view.update_page()

    def setYear(self, e):
        self.anno = self._view.ddyear.value
        print(self.anno)

    def setShape(self, e):
        self.forma = self._view.ddshape.value
        print(self.forma)

    def handle_graph(self, e):
        self._model.buildGraph(self.anno, self.forma)
        n_nodi, n_archi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente"
                                                    f"il grafo ha {n_nodi} nodi e {n_archi} archi"))
        diz = self._model.getVicini()
        for stato in diz:
            self._view.txt_result.controls.append(ft.Text(f"{stato} - somma su archi vicini: {diz[stato]}"))
        self._view.update_page()

    def handle_path(self, e):
        best_path, peso_max = self._model.calcolaPercorso()
        self._view.txtOut2.controls.append(
            ft.Text(f"Peso del cammino: {peso_max}"))
        for arco, dist in best_path:
            self._view.txtOut2.controls.append(ft.Text(f"{arco[0]} ---> {arco[1]}: peso = {arco[2]['weight']}, distanza = {dist}"))
        self._view.update_page()
