import threading
import time
import random
from datetime import datetime, timedelta

def gerenciar_risco(total_risco: float, estrategias: list[tuple[str,float]], tempo_total: int):
    """
    Simula buget de risco sendo tomado por diferentes estratégias

    Args:
    total_risco (float): budget de risco
    estrategias (list[tuple[str,float,float]]): lista que guarda duplas com nome da estratégia e
        risco que ela consome, respectivamente
    tempo_total (int): duração total do experimento

    Returns:
    dict: risco total consumido por cada estrategia
    """
    
    #define as variaveis de risco do experimento
    risco_total_atual = 0
    risco_total_consumido_por_estrategia = {k[0]: 0 for k in estrategias}

    #define tempos inicial e final
    tempo_inicial = datetime.now()
    tempo_final = tempo_inicial + timedelta(seconds=tempo_total)

    #define função que, por estratégia, insere risco nas variaveis de risco do experimento
    lock = threading.Lock()
    def inserir_risco(estrategia):
        def inserir_risco_estrategia():
            nonlocal risco_total_atual
            nonlocal risco_total_consumido_por_estrategia
            while datetime.now() < tempo_final:
                with lock:
                    if total_risco - risco_total_atual > next(v[1] for v in estrategias if v[0] == estrategia):
                        risco_total_atual += next(v[1] for v in estrategias if v[0] == estrategia)
                        risco_total_consumido_por_estrategia[estrategia] += next(v[1] for v in estrategias if v[0] == estrategia)
                    else:
                        time.sleep(1)
        return inserir_risco_estrategia

    #faz o threading
    threads = []
    for e in [v[0] for v in estrategias]:
        t = threading.Thread(target=inserir_risco(e))
        t.start()
        threads.append(t)        
    
    for thread in threads:
        thread.join()

    return risco_total_consumido_por_estrategia

#resultado = gerenciar_risco(100, [("daytrade",5),("pairs",2)],20)
#print(resultado)

def monitorar_acoes(acoes: list[str], valor_alvo: float, tempo_total: int):
    """
    Monitora quais ações atingiram ou ultrapassaram um valor alvo, em uma janela de tempo de observação

    Args:
    acoes (list): lista de ações observadas
    valor_alvo (float): valor alvo monitorado
    tempo_total (int): duração total do experimento

    Returns:
    list: lista com as ações que atingiram ou ultrapassaram um valor alvo
    """

    #define preços inicias de cada ação e listacompartilhada vazia
    prices = {a: round(random.uniform(17, 18),2) for a in acoes}
    listacompartilhada = []

    #define tempos inicial e final do experimento
    tempo_inicial = datetime.now()
    tempo_final = tempo_inicial + timedelta(seconds=tempo_total)

    #define a funcao que para cada acao atualiza precos, verifica o valor alvo e atualiza a lista compartilhada
    lock_prices = threading.Lock()
    lock_listacompartilhada = threading.Lock()
    def monitorar(a):
        def monitorar_acao():
            while datetime.now() < tempo_final:
                with lock_prices:
                    valor_anterior = prices[a]
                time.sleep(random.uniform(0.1, 0.5))
                with lock_prices:
                    valor_atual = valor_anterior * (1+random.uniform(-0.1, 0.1))
                    prices[a] = valor_atual
                with lock_listacompartilhada:
                    if a not in listacompartilhada and valor_anterior <= valor_alvo and valor_alvo <= valor_atual:
                        listacompartilhada.append(a)
                    
        return monitorar_acao

    #faz o threading
    threads = []
    for a in acoes:
        t = threading.Thread(target=monitorar(a))
        t.start()
        threads.append(t)  

    for thread in threads:
        thread.join()

    return listacompartilhada

#print(monitorar_acoes(["PETR","ABEV","ITUB","BBSA","WEGE"],20, 12))