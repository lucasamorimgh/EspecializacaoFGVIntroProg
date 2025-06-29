import numpy as np

def simular_precos(S0: float, sigma: float, days: int):
    """
    Retorna vetor de preços aleatórios dados horizonte de tempo, preço inciial e desvio padrão dos choques

    Args:
        S0 (float): Preço inicial do vetor de preços
        sigma (float): Desvio padrão dos choques normais
        days (int): horizonte de tempo
    
    Returns:
        ndarray: vetor de preços aleatórios dados horizonte de tempo, preço inciial e desvio padrão dos choques
    """
    #Forma lista de preços
    result = [S0]

    #Percorrendo os dias e appendando o ultimo resultado acrescido de um choque normal
    for t in range(days):
        eps = np.random.normal(0.0,sigma)
        result.append(result[len(result)-1]+eps)
    
    return np.array(result)
        

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


def calc_retornos_log(prices: np.ndarray):
    """
    Retorna vetor de log retornos associado a um vetor de preços

    Args:
        prices (np.ndarray): vetor de preços
    
    Returns:
        ndarray: vetor de log retornos
    """
        
    #Forma lista de log retornos
    logret = []

    #Percorrendo os preços de 1 a último, calcula logretornos e appenda
    for i in range(len(prices)-1):
        r = np.log(prices[i+1]/prices[i])
        logret.append(r)

    return np.array(logret)

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

def  rolling_std(returns: np.ndarray, window: int, days_size: int= 0):
    """
    Retorna vetor de desvios padrao moveis dos retornos em um vetor de retornos

    Args:
        returns (np.ndarray): vetor de retornos
        window (int): tamanho da janela para aferição da media movel
        days_size (int): ajuste no denominador do desvio padrão
    
    Returns:
        ndarray: vetor de desvios padrao moveis dos retornos
    """
        
    #Pega o vetor de medias moveis
    ma = sma(returns,window)

    #Forma lista de desvios padrao moveis
    sd_all = []

   #Percorrendo os dias, calcula a devio padrao (movel) dos retornos (quando ha janela) e appenda
    for t in range(len(returns)):
        if t >= window-1:
            rslice = returns[t-window+1:t+1]
            
            #Soma de quadrados movel seguida do desvio padrao e appenda
            sumsq = 0
            for r in rslice:
                sumsq += (r-ma[t-window+1]) ** 2
            sd = (sumsq / (window - days_size)) ** 0.5

            sd_all.append(sd)

    return np.array(sd_all)

