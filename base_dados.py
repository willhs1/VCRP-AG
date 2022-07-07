import numpy as np
import requests


class Ponto:
    def __init__(self, x):
        self.x = np.array(x)
        self.d = 0

    def __str__(self):
        return f"{self.x} : {self.d}"

    def __repr__(self):
        return str(self);


class Base_dados:
    def __init__(self, data_url):
        self.data_url = data_url
        text = requests.get(data_url).text
        self.data_list = text.splitlines()
        self.otimo = self.data_list[1][11:]
        self.dict_ponto = {}

    @property
    def n_nos(self):
        n_nos = 0
        for x in self.data_list:
            if 'DIMENSION' in x:
                n_nos = int(x.split()[2])
                break
        return n_nos

    @property
    def Q(self):
        Q = 0.0
        for x in self.data_list:
            if 'CAPACITY' in x:
                Q = float(x.split()[2])
        return Q

    def fill_dict_ponto(self):
        indice_coord = self.data_list.index('NODE_COORD_SECTION')
        indice_demanda = self.data_list.index('DEMAND_SECTION')
        fim_demanda = self.data_list.index('DEPOT_SECTION')
        self.dict_ponto = {}
        for i in range(indice_demanda - indice_coord - 1):
            row = self.data_list[indice_coord + i + 1].split()
            ponto = Ponto([float(row[1]), float(row[2])])
            self.dict_ponto[i + 1] = ponto

        for i in range(fim_demanda - indice_demanda - 1):
            row = self.data_list[indice_demanda + i + 1].split()
            self.dict_ponto[i + 1].d = float(row[1])
