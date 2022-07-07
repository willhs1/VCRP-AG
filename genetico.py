import math
import random

from rota import Rota


class Genetico:
    def __init__(self, Q, dic_city, factory, N=100, taxa_cross: float = 0.7, taxa_mutacao: float = 0.05,
                 elitismo=False):
        self.taxa_cross = taxa_cross
        self.taxa_mutacao = taxa_mutacao
        self.elitismo = elitismo
        self.N = N
        self.Q = Q
        self.dic_city = dic_city
        self.factory = factory
        self.population = []
        for i in range(N):
            self.population.append(Rota(Q, dic_city, factory))

    def normalizacao(self, rank: int):
        minimo = 1.0
        maximo = 100
        return minimo + (maximo - minimo) * (self.N - rank) / (self.N - 1)

    @property
    def ranking(self):
        dict_rank = {}
        l_rank = self.population.copy()
        l_rank.sort()
        for i in range(len(l_rank)):
            dict_rank[i + 1] = l_rank[i], self.normalizacao(i + 1)
        return dict_rank

    def roleta(self):
        l_somada = []
        soma_atual = 0
        dict_rank = self.ranking
        for i in range(len(dict_rank)):
            soma_atual += dict_rank[i + 1][1]
            l_somada.append(soma_atual)
        sorteio = random.random() * soma_atual
        for i in range(len(l_somada)):
            if l_somada[i] >= sorteio:
                return i + 1

    def selecao(self):
        selecionados = []
        while len(selecionados) < self.N:
            selecionados.append(self.roleta())
        return selecionados

    def remove_fac(self, rota):
        return [i for i in rota.rota if i != self.factory]

    def cycle_cross(self, rota1, rota2):
        # print(rota1,rota2)
        trajeto1 = self.remove_fac(rota1)
        trajeto2 = self.remove_fac(rota2)
        # print(f'Originais:\n{trajeto1}\n{trajeto2}')
        bias = -1
        for i in range(len(trajeto1)):
            if trajeto1[i] != trajeto2[i]:
                bias = i
                break
        if bias == -1:  # Caso de pais iguais
            return rota1, rota2
        lista_indices = [bias]
        while True:
            bias = trajeto1.index(trajeto2[bias])
            if bias in lista_indices:
                break
            lista_indices.append(bias)
        # print(f'Indices q vão ser trocados:\n{lista_indices}')
        trajeto1_2 = trajeto1.copy()
        trajeto2_1 = trajeto2.copy()
        for indice in lista_indices:
            trajeto1_2[indice] = trajeto2[indice]
            trajeto2_1[indice] = trajeto1[indice]
        nova_rota1 = Rota(self.Q, self.dic_city, self.factory, inicializar=False)
        nova_rota2 = Rota(self.Q, self.dic_city, self.factory, inicializar=False)
        nova_rota1.nova_rota(trajeto1_2)
        nova_rota2.nova_rota(trajeto2_1)
        return nova_rota1, nova_rota2

    def crossover(self, selecionados):
        filhos = []
        dict_rank = self.ranking
        if self.elitismo:
            filhos.append(dict_rank[1][0])
        for i in range(math.floor(len(selecionados) / 2)):
            P1 = dict_rank[selecionados[2 * i]][0]
            P2 = dict_rank[selecionados[2 * i + 1]][0]
            # print(f'Pais: \n{i} {P1.rota} {P2.rota}')
            if random.random() < self.taxa_cross:
                # print('Cross')
                F1, F2 = self.cycle_cross(P1, P2)
            else:
                # print('Not Cross')
                F1 = P1
                F2 = P2
                # print(f'{i} {F1} {F2}')
            # print(f'Filhos: \n{i} {F1.rota} {F2.rota}')
            filhos.append(F1)
            filhos.append(F2)
        if self.elitismo:
            filhos.sort()
            filhos = filhos[:-1]
        return filhos

    def mutacao(self, filhos):
        mutados = []
        for filho in filhos:
            customers = self.remove_fac(filho)
            # print(f'Original: {customers} {len(customers)}')
            for index, city in enumerate(customers):
                if random.random() < self.taxa_mutacao:
                    swap = random.choice([i for i in range(len(customers)) if i != index])
                    temp = customers[index]
                    customers[index] = customers[swap]
                    customers[swap] = temp
                    # print(f'mutation no indice {index} pelo {swap}')
            mutado = Rota(self.Q, self.dic_city, self.factory, inicializar=False)
            # print(f'Mutado: {customers} {len(customers)}')
            mutado.nova_rota(customers)
            # print(mutado)
            mutados.append(mutado)
        return mutados

    def new_generation(self):
        selecionados = self.selecao()
        filhos = self.crossover(selecionados)
        mutados = self.mutacao(filhos)
        self.population = mutados
