import random
from functools import total_ordering
from typing import *


@total_ordering
class Rota():
    def __init__(self,Q:float,dic_city:Dict[int,'Ponto'],factory:int,inicializar=True):
        self.Q_max=Q
        self.Q=Q
        self.dic_city=dic_city
        self.factory=factory
        self.rota=[factory]
        if inicializar:
            self.start()
    @property
    def cidades_disponiveis(self):
        return [i for i in self.dic_city.keys() if self.can_add_city(i) ] 

    def euclidiana(self,p1,p2):
        dist=0
        for n in range(len(p1)):
            dist+=(p1[n]-p2[n])**2
        return dist**0.5
    
    @property
    def distancia_trajeto(self):
        dist=0
        for i in range(len(self.rota)-1):
            ponto1=self.dic_city[self.rota[i]].x
            ponto2=self.dic_city[self.rota[i+1]].x
            dist+=self.euclidiana(ponto1,ponto2)
        return dist
    
    def can_add_city(self,city:int):
        return True if self.Q-self.dic_city[city].d >0 and city not in self.rota else False
    
    def nova_rota(self,trajeto):
        self.rota=[self.factory]
        self.last_fac=0
        for i,city in enumerate(trajeto):
            if self.can_add_city(city):
                self.rota.append(city)
                self.Q-=self.dic_city[city].d
            else:
                self.rota.append(self.factory)
                self.Q=self.Q_max
                if self.can_add_city(city):
                    self.rota.append(city)
                    self.Q-=self.dic_city[city].d
        self.rota.append(self.factory)
        self.Q=self.Q_max

    def start(self):
        while True:
            lista_cidades = self.cidades_disponiveis
            if not lista_cidades:
                if self.rota[-1] != self.factory:
                    self.rota.append(self.factory)
                    self.Q=self.Q_max
                else:
                    break
            else:
                city=random.choice(lista_cidades)
                self.rota.append(city)
                self.Q-=self.dic_city[city].d
  
    def __lt__(self,o):
        return self.distancia_trajeto<o.distancia_trajeto

    def __eq__(self,o):
        return self.distancia_trajeto==o.distancia_trajeto

    def __str__(self) -> str:
        return f'{self.rota} \nDT {self.distancia_trajeto}\n'
  
    def __repr__(self) -> str:
        return str(self)
