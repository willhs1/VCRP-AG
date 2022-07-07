from genetico import *
from base_dados import*
from tqdm import tqdm


def main():
    data_url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n19-k2.vrp"
    # data_url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n22-k8.vrp"
    # data_url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n45-k5.vrp"
    bd = Base_dados(data_url)
    bd.fill_dict_ponto()
    Q = bd.Q
    dict_ponto = bd.dict_ponto
    g = Genetico(Q, dict_ponto, 1, N=50, taxa_mutacao=.01)
    melhor_atual = (g.ranking[1])[0]
    it_max = 1000
    melhores = {0: melhor_atual}
    medias = [sum([d.distancia_trajeto for d in g.population])/len(g.population)]
    for it in tqdm(range(it_max)):
        g.new_generation()
        melhores[it + 1] = (g.ranking[1])[0]
        medias.append(sum([d.distancia_trajeto for d in g.population]) / len(g.population))
        if melhor_atual > (g.ranking[1])[0]:
            melhor_atual = (g.ranking[1])[0]
        if (it+1) % 100 == 0:
            media_lst_100 = medias[it-99:it+1]
            print(melhor_atual, sum(media_lst_100)/len(media_lst_100))
    print(melhores)
    print(melhor_atual)


if __name__ == '__main__':
    main()