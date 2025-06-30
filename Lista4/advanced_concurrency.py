import threading
import random
import time
import numpy as np
from datetime import datetime, timedelta

#Oriundo da lista 3
def calc_retornos_simples(prices: np.ndarray):
    """
    Retorna vetor de retornos associado a um vetor de preços

    Args:
        prices (np.ndarray): vetor de preços
    
    Returns:
        ndarray: vetor de retornos
    """
        
    #Forma lista de retornos
    ret = []

    #Percorrendo os preços de 1 a último, calcula retornos e appenda
    for i in range(len(prices)-1):
        r = prices[i+1]/prices[i] -1
        ret.append(r)

    return np.array(ret)

#Oriundo da lista 3
def  sma(returns: np.ndarray, window: int):
    """
    Retorna vetor de medias moveis dos retornos em um vetor de retornos

    Args:
        returns (np.ndarray): vetor de retornos
        window (int): tamanho da janela para aferição da media movel
    
    Returns:
        ndarray: vetor de medias moveis dos retornos
    """

    #Forma lista de medias moveis
    ma_all = []

   #Percorrendo os dias, calcula a media (movel) dos retornos (quando ha janela) e appenda
    for t in range(len(returns)):
        if t >= window-1:
            rslice = returns[t-window+1:t+1]
            
            #Soma movel seguida da media e appenda
            sum = 0
            for r in rslice:
                sum += r
            ma = sum / window

            ma_all.append(ma)

    return np.array(ma_all)

def calcular_medias_moveis(acoes: dict[str, np.ndarray], janela: int):
    """
    Calcula médias moveis das ações e preços apresentados

    Args:
        acoes (dict[str, np.ndarray]): dicionario com, nas keys, as ações consideradas e nos valores, seus vetor de preços
        janela (int): tamanho da janela para aferição da media movel
    
    Returns:
        dict: dicionário com as ações consideradas e as respectivas médias móveis de seus retornos
    """

    #dicionario com as medias moveis aferidas
    sma_all = {a[0]:[] for a in acoes.items()}
    
    #funcao de calculo das medias moveis de cada ação
    lock = threading.Lock()
    def calcsma(acao):
        def calcsma_acao():
            nonlocal sma_all
            with lock:
                sma_all[acao].append(sma(calc_retornos_simples(acoes[acao]), janela))
        return calcsma_acao

    #faz o threading para o calculos e registros das medias moveis
    threads = []
    for acao in acoes:
        t = threading.Thread(target=calcsma(acao))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    return sma_all 

#resultado = calcular_medias_moveis({"PETR":np.array([13,14,15,16,17]),"ABEV":np.array([23,24,25,26,27])}, 2)
#print(resultado)

def calcular_volatilidade(retornos: np.ndarray, janela: int, num_threads:int):
    """
    Calcula desvios padrão moveis de uma série de retornos apresentados

    Args:
        retornos (np.ndarray): vetor de retornos cujos desvios padrão moveis se quer calcular
        janela (int): tamanho da janela para aferição dos desvios padrão moveis
        num_threads (int): numero de threads que se quer empregar no cálculo
    
    Returns:
        dict: dicionário com as ações consideradas e as respectivas médias móveis de seus retornos
    """
    
    #lista de índices dos cálculos que serão percorridos, associado a qual thread os calculará
    unitcalcidx = [(x,x % num_threads) for x in range(np.shape(retornos)[0]) if x >= janela-1]

    #lista de desvios padrao
    std_list = []

    #define funcão que percorre cada batch de calculo de um thread, calcula e appenda os resultados em std_list
    lock = threading.Lock()    
    def calcvolbatch(n):
        def calcvolbatch_do():
            for i in [x[0] for x in unitcalcidx if x[1] == n]:
                with lock:
                    std_list.append((i,float(round(np.std(retornos[i-janela+1:i+1]),2))))
        return calcvolbatch_do

    threads = []
    for n in range(num_threads):
        t = threading.Thread(target=calcvolbatch(n))
        t.start()
        threads.append(t)

    #lista de desvios padrao ordenados
    std_final = [x[1] for x in sorted(std_list, key=lambda x: x[0])]
    return np.array(std_final)

#resultado = calcular_volatilidade(np.array([0.13,0.13,0.13,0.36,0.27,0.13,0.24,0.05,0.36,0.27,0.13,0.24,0.05,0.36,0.27,0.13,0.24,0.34,0.35,0.36]), 3, 4)
#print(resultado)
