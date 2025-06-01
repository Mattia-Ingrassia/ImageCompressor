
import numpy as np
from scipy.fft import dct, dctn, idctn

def scipy_dct_fft(func_array):
    return dct(func_array, type=2, norm="ortho")

def scipy_dct2_fft(func_array):
    return dctn(func_array, type=2, norm="ortho")

def scipy_idct2_fft(func_array):
    return idctn(func_array, type=2, norm="ortho")

def custom_dct(func_array, D = None):
    n = len(func_array)
    if D is None:
        D = _compute_d(n)
    coeff_array = np.dot(D, func_array)
    return coeff_array

def custom_dct2(func_array_2d):
    coef_array_2d = np.copy(func_array_2d)
    N = len(func_array_2d)
    D = _compute_d(N)   

    for j in range(N):
        coef_array_2d[:, j] = custom_dct(coef_array_2d[:, j], D)
    
    for j in range(N):
        coef_array_2d[j, :] = custom_dct(coef_array_2d[j, :], D)

    return coef_array_2d

def _compute_d(n):
    alpha_array = np.zeros(n)
    alpha_array[0] = 1.0 / np.sqrt(n)
    alpha_array[1:] = np.sqrt(2.0 / n)
    D = np.empty([n, n])

    for l in range(n):
        for j in range(n):
            D[l][j] = alpha_array[l] * np.cos( l * np.pi * (2*j+1) / (2*n))
    
    return D


