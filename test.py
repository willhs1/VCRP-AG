from genetico import *
from base_dados import*
from tqdm import tqdm


def main():
    data_url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n19-k2.vrp"
    bd = Base_dados(data_url)
    bd.fill_dict_ponto()
    Q = bd.Q
    dict_ponto = bd.dict_ponto
    g = Genetico(Q, dict_ponto, 1, N=100, taxa_mutacao=.1)
    melhor_atual = (g.ranking[1])[0]
    it_max = 1000
    melhores = {0: melhor_atual}
    medias = {0: sum([d.distancia_trajeto for d in g.population])/len(g.population)}
    for it in tqdm(range(it_max)):
        g.new_generation()
        melhores[it + 1] = (g.ranking[1])[0]
        medias[it+1] = sum([d.distancia_trajeto for d in g.population]) / len(g.population)
        if melhor_atual > (g.ranking[1])[0]:
            melhor_atual = (g.ranking[1])[0]
        if it % 10 == 0:
            print(melhor_atual, medias[it+1])
    print(melhores)
    print(melhor_atual)


if __name__ == '__main__':
    main()