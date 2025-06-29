import numpy as np

def replace_negatives(v: np.ndarray, new_value: float):
    """
    Substitui os valores negativos de um array por um novo valor

    Args:
        v (np.ndarray): array cujos negativos se quer substituir
        new_value (float): novo valor, que substuirá os negativos
    
    Returns:
        ndarray: array pós substituições
    """

    #Copia v
    v_copy = v.copy()

    #Cria máscara de entradas negativas
    neg_filter = v_copy < 0

    # Altera as entradas da máscara para new_value
    v_copy[neg_filter] = new_value

    return v_copy

def local_peaks(series: np.ndarray): 
    """
    Toma uma serie temporal e retorna um vetor de índices dos seus máximos locais e 
    um vetor dos seus respectivos valores (peaks) 

    Args:
        series (np.ndarray): serie temporal
    Returns:
        Tuple[np.ndarray, np.ndarray]: tupla (indices, peaks)
    """

    n = np.shape(series)[0]
    indices = []
    peaks = []
    for i in range(n):
        if i > 0 and i < n-1:
            if series[i-1] < series[i] and series[i] > series[i+1]:
                indices.append(i)
                peaks.append(series[i])

    return (np.array(indices),np.array(peaks))


print(local_peaks(np.array([1,2,3,1,2,4,1])))

