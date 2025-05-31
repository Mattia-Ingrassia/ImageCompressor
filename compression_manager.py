import warnings
import imageio.v3 as iio
import numpy as np
import os

from dct import scipy_dct2_fft, scipy_idct2_fft

OUTPUT_FOLDER = "output_images"

def compression(image_path, block_size, frequences_cut):
    # Check on the frequences_cut value
    if(frequences_cut < 0) or  (frequences_cut > block_size*2 - 2):
        warnings.warn("Error: frequences_cut value is not valid")
    
    # Open the image in a grayscale format
    image = iio.imread(image_path, pilmode='L')

    rows, columns = image.shape

    # Calculate the number of blocks in the original image
    blocks_per_row = rows // block_size
    blocks_per_column = columns // block_size
    
    # Cut the remaining elements that are not part of a block
    image = image[:blocks_per_row * block_size, :blocks_per_column * block_size]

    # Split the image into blocks of size block_size x block_size
    # Initially, it reshapes the image into (blocks_per_row, block_size, remaining_blocks, block_size)
    # Then, it swaps axes to group block dimensions together
    # Lastly, it reshapes the image into (total_blocks, block_size, block_size)
    # for example, having a 160x160 image with a block size of 8, it will result in a three dimenisional vector split into (400 blocks, 8, 8)
    image = image.reshape(blocks_per_row, block_size, -1, block_size).swapaxes(1, 2).reshape(-1, block_size, block_size)

    image_new = []
    for block in image:
        # Perform scipy dct2 on each block
        coef_matrix = scipy_dct2_fft(block)
        coef_matrix = np.array(coef_matrix)
        coef_matrix_cut = np.zeros(shape=(block_size, block_size))

        # Perform frequences cut using given values
        for k in range(block_size):
            for l in range (block_size):
                if (k + l) < frequences_cut:
                    coef_matrix_cut[k, l] = coef_matrix[k, l]
        
        # Perform scipy idct2 on the matrix obtained combining the operations above
        ff = scipy_idct2_fft(coef_matrix_cut)
        ff = np.array(ff)
        # Round the elements of the block, clipping the values inside the (0, 255) scale 
        ff = np.around(ff, 0)
        ff = np.clip(ff, 0, 255)
        image_new.append(ff)
        

    image_new = np.array(image_new)

    # Rebuild the compressed image by reshaping the 3d vector:
    # Initially, it reshapes blocks back into grid structure (blocks_per_row, blocks_per_column, block_size, block_size)  
    # blocks_rearranged = blocks_grid.transpose(0, 2, 1, 3)
    # Then, it rearranges dimensions to group pixels that belong to the same image row
    # From (blocks_per_row, blocks_per_column, block_size, block_size) To   (blocks_per_row, block_size, blocks_per_column, block_size)
    # Finally, it reshapes to final 2D image by combining block dimensions: (height, width) where height = blocks_per_row * block_size
    
    blocks_grid = image_new.reshape(blocks_per_row, blocks_per_column, block_size, block_size)
    blocks_rearranged = blocks_grid.transpose(0, 2, 1, 3)
    final_image = blocks_rearranged.reshape(
        blocks_per_row * block_size, 
        blocks_per_column* block_size
    )
    
    # Convert matrix data to uint for conversion issues
    final_image = final_image.astype(np.uint8)

    # Saves the compressed image in the output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{file_name}.bmp")
    iio.imwrite(output_path, final_image)
    
    return output_path
