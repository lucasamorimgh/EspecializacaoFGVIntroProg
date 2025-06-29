import numpy as np

def rotate_90(A: np.ndarray):
    """
    Retorna matriz (nxn) rotacionada de 90o no sentido horario

    Args:
        A (np.ndarray): matriz (nxn) por rotacionar
    
    Returns:
        ndarray: matriz (nxn) rotacionada
    """
        
    #Transpoe
    B = np.transpose(A)
    
    #Inverte as linhas de B e poe em C
    C = []
    for row in B:
        row_rev = []
        for r in range(len(row)):
            row_rev.append(row[len(row)-r-1])
        C.append(row_rev)

    return np.array(C)

def sum_subdiagonals(A: np.ndarray, k: int):
    """
    Retorna a soma das entradas na subdiagonal de shift k

    Args:
        A (np.ndarray): matriz (nxn) cuja subdiagonal interessa
        k (int): shift da subdiagonal
    
    Returns:
        float: subdiagonal 
    """
        
    #Pecorre a subdiagonal e acumula valores em sum
    sum=0
    for i in range(np.shape(A)[1]):
        try:
            e = A[i+k,i]
        except:
            e = 0
        sum += e
    return sum

def block_matmul(A: np.ndarray, B: np.ndarray, block_size: int):
    """
    Retorna o produto de duas matrizes a partir de blocos

    Args:
        A (np.ndarray): matriz à esquerda do protudo (axb)
        B (np.ndarray): matriz à direita do protudo (bxc)
        block_size (int): tamanho do bloco a ser considerado para o produto
    
    Returns:
        np.ndarray: matriz A * B 
    """
        
    #Mede as dimensoes das matrizes A e B as separa em blocos
    shape_a = np.shape(A)
    shape_b = np.shape(B)
    if shape_a[1] == shape_b[0]:
        #Blocos da A
        A_blocks = []
        A_blocks_shape = [0,0]
        for lins in range(int(np.ceil(shape_a[0]/block_size))):
            A_lins_blocks = []
            A_blocks_shape[0] = max(A_blocks_shape[0],lins+1)
            for cols in range(int(np.ceil(shape_a[1]/block_size))):
                A_blocks_shape[1] = max(A_blocks_shape[1],cols+1)
                A_lc = A[lins*block_size:(lins+1)*block_size, cols*block_size:(cols+1)*block_size]
                A_lins_blocks.append(A_lc)
            A_blocks.append(A_lins_blocks)

        #Blocos da B
        B_blocks = []
        B_blocks_shape = [0,0]
        for lins in range(int(np.ceil(shape_b[0]/block_size))):
            B_lins_blocks = []
            B_blocks_shape[0] = max(B_blocks_shape[0],lins+1)
            for cols in range(int(np.ceil(shape_b[1]/block_size))):
                B_blocks_shape[1] = max(B_blocks_shape[1],cols+1)
                B_lc = B[lins*block_size:(lins+1)*block_size, cols*block_size:(cols+1)*block_size]
                B_lins_blocks.append(B_lc)
            B_blocks.append(B_lins_blocks)

        #Forma a C a partir do produto de blocos
        C_blocks = []
        for l in range(A_blocks_shape[0]):
            C_l_blocks = []
            for c in range(B_blocks_shape[1]):
                A_lcframe = A_blocks[l][0]
                B_lcframe = B_blocks[0][c]
                C_lc = np.zeros(np.shape(A_lcframe@B_lcframe))
                for i in range(A_blocks_shape[1]):
                    C_lc += A_blocks[l][i] @ B_blocks[i][c]
                C_l_blocks.append(C_lc)
            C_blocks.append(C_l_blocks)
            
        return(np.block(C_blocks))