import threading
import random
import time
import numpy as np
from datetime import datetime, timedelta

def simular_traders(num_traders: int, num_ordens: int):
    """
    Simula um book de ofertas de compras e vendas

    Args:
        num_traders (int): número de traders na simulação
        num_ordens (int): número de ordens que cada trader envia na simulação
    
    Returns:
        dict: dicionário com ordens de compra e venda
    """

    #define o order_book inicial
    order_book = [dict([]),dict([])] #books de compra e venda, respect.
    
    #define a função de inclusão de ordens no book, com lock
    lock = threading.Lock()
    def incl_ordem_maker(trader,qtd,px):
        def incl_ordem():
            if qtd >= 0:
                nova_chave = max(order_book[0].keys(), default=-1) + 1
                with lock:
                    order_book[0][nova_chave] = (trader,qtd,px)
            else:
                nova_chave = max(order_book[1].keys(), default=-1) + 1
                with lock:
                    order_book[1][nova_chave] = (trader,qtd,px)
        return incl_ordem
    
    #define o conjunto de ordens a ser incluida no book (preços e quantidades são definidos adiante)
    ordens = [(trader, ordem) for trader in range(num_traders) for ordem in range(num_ordens)]
    #aqui aleatorizamos as ordens, para não privilegiar nenhum trader
    #pode ficar (trader1,1) depois de (trader1,2), mas não usamos a segunda componente,
    #pois ao book só importa a ordem de chegada das ordens no book
    #favor considerar que estou usando o pacote random não para resolver a pergunta, 
    #mas para tornar a resposta mais legal
    random.shuffle(ordens) 

    #faz o threading para a inclusao das ordens no book
    threads = []
    for (trader,ordem) in ordens:
        #quantidades e preços aleatórios
        t = threading.Thread(target=incl_ordem_maker(trader,random.randint(-100, 100),round(random.uniform(10, 15),2)))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
  
    compras = [{k: v} for k, v in order_book[0].items()]
    vendas = [{k: v} for k, v in order_book[1].items()]

    return {'buy': compras, 'sell': vendas}

#print(simular_traders(4,2))

def simular_feeds_de_dados(acoes: list[str], tempo_total: int):
    """
    Simula feed de preços de ações durante uma janela de monitoramento

    Args:
        acoes (list[str]): lista de tickers monitorados
        tempo_total (int): duração total do monitoramento
    
    Returns:
        dict: estado final dos preços dos ativos
    """
    
    #define um objeto que marcará todos os preços do ensaio
    prices = {k: [] for k in acoes}

    #registra o time inicial e final do experimento
    tempo_inicial = datetime.now()
    tempo_final = tempo_inicial +  timedelta(seconds=tempo_total)

    #define função que espera tempo aleatorio entre cotações e registra as novas cotações
    lock = threading.Lock()
    def feed_dados(acao):
        def feed_dados_acao():
            while datetime.now() < tempo_final:
                time.sleep(min(3,np.random.exponential(scale=2)))
                tempo_cotacao = datetime.now()
                if tempo_cotacao <= tempo_final:
                    with lock:
                        prices[acao].append((tempo_cotacao, round(random.uniform(10, 15),2)))
        return feed_dados_acao
    
    #define funcao que imprime os preços vigentes de 5s em 5s
    def price_print():
        while datetime.now() < tempo_final:
            time.sleep(5)
            with lock:
                prices_to_print = [{k: v[-1]} for k, v in prices.items()]
            print("O preços vigentes são:")
            print(prices_to_print)
    
    #faz o threading para o registro dos preços das ações e impresões periódicas dos preços vigentes
    threads = []
    for acao in acoes:
        t = threading.Thread(target=feed_dados(acao))
        t.start()
        threads.append(t)

    tprint = threading.Thread(target=price_print)
    tprint.start()
    threads.append(tprint)

    for thread in threads:
        thread.join()

    #retorna os preços finais
    final_prices = [{k: v[-1]} for k, v in prices.items()]
    return final_prices

#precos_finais = simular_feeds_de_dados(["PETR","ABEV"],10)
#print("Os preços finais sao:")
#print(precos_finais)