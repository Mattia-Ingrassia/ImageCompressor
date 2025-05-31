import numpy as np
import os

OUTPUT_PATH = "benchmark_matrices/"


def matrix_generator(n):
    """
    Generate random square matrices with casual numbers in a range (-2000, 2000).
    The matrices are saved in the OUTPUT_PATH folder with .npy format.
    
    Args:
        n (int): Size of the square matrix (n x n).
    
    Returns:
        None.
    
    Notes:
        - A given seed (23) is used to grant reproducibility.

    """
    rng = np.random.default_rng(23)
    
    np.random.seed(23)
    matrix = rng.uniform(-2000, 2000, size=(n, n))

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    filename = os.path.join(OUTPUT_PATH, f"matrix_{n}x{n}.npy")
    
    np.save(filename, matrix)



if __name__ == "__main__":
    sizes = []
    # Generates squared matrices with crescent size following powers of two (as an example, from 2^3 (8x8) to 2^13 (8192×8192))
    for i in range(3,12): 
        sizes.append(pow(2,i))
    
    for size in sizes:
        matrix_generator(size)

