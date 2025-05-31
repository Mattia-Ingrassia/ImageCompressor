import os
import numpy as np
import timeit
import matplotlib.pyplot as plt

from dct import custom_dct2, scipy_dct2_fft

PATH_MATRICES = "benchmark_matrices"

def order_paths(paths):
    # Order paths by creation time, since the matrices are generated sequentially in crescent order
    new_paths = []
    for path in paths:
        new_paths.append(os.path.join(PATH_MATRICES, path))
    sorted_files = sorted(new_paths, key=os.path.getctime)
    return sorted_files

if __name__ == "__main__":
    
    custom_times = []
    fft_times = []
    matrix_sizes = []
    
    paths = os.listdir(PATH_MATRICES)
    ordered_paths = order_paths(paths)

    for matrix_path in ordered_paths:

        matrix = np.load(matrix_path)        

        # Perform custom dct2 and track execution time

        start_time_custom = timeit.default_timer()
        custom_results = custom_dct2(matrix)
        end_time_custom = timeit.default_timer()
        elapsed_time_custom = end_time_custom - start_time_custom
        
        custom_times.append(elapsed_time_custom)

        # Perform scipy dct2 and track execution time

        start_time_fft = timeit.default_timer()
        fft_results = scipy_dct2_fft(matrix)
        end_time_fft = timeit.default_timer()
        elapsed_time_fft = end_time_fft - start_time_fft
        
        fft_times.append(elapsed_time_fft)

        matrix_sizes.append(len(matrix))



    # Plot the results
    plt.figure(figsize=(10, 6))

    plt.plot(matrix_sizes, custom_times , marker='s', label="Custom DCT")
    plt.plot(matrix_sizes, fft_times, marker='^', label="Scipy DCT with FFT")

    # Format the plot
    plt.xlabel('Matrix Sizes')
    plt.ylabel('Execution time (seconds) (log scale)')
    plt.title('Comparison of FFT DCT and Standard DCT by Execution Time')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig("DCT_comparison.png")

