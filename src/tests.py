import unittest
import numpy as np

from dct import custom_dct, scipy_dct_fft, custom_dct2, scipy_dct2_fft

class TestDct(unittest.TestCase):
    
    def test_custom_dct(self):
        input_vector = [231, 32, 233, 161, 24, 71, 140, 245]
        expected_result = [4.01e+02, 6.60e+00, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01]
        custom_dct_result = custom_dct(input_vector)
        np.testing.assert_allclose(expected_result, custom_dct_result, rtol=0.1, atol=2.0)

    def test_scipy_dct(self):
        input_vector = [231, 32, 233, 161, 24, 71, 140, 245]
        expected_result = [4.01e+02, 6.60e+00, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01]
        scipy_dct_result = np.array(scipy_dct_fft(input_vector))
        np.testing.assert_allclose(expected_result, scipy_dct_result, rtol=0.1, atol=2.0)
        
    def test_custom_dct2(self):
        input_vector = [ 
            [231.0, 32.0, 233.0, 161.0, 24.0, 71.0, 140.0, 245.0],
            [247.0, 40.0, 248.0, 245.0, 124.0, 204.0, 36.0, 107.0],
            [234.0, 202.0, 245.0, 167.0, 9.0, 217.0, 239.0, 173.0],
            [193.0, 190.0, 100.0, 167.0, 43.0, 180.0, 8.0, 70.0],
            [11.0, 24.0, 210.0, 177.0, 81.0, 243.0, 8.0, 112.0],
            [97.0, 195.0, 203.0, 47.0, 125.0, 114.0, 165.0, 181.0],
            [193.0, 70.0, 174.0, 167.0, 41.0, 30.0, 127.0, 245.0],
            [87.0, 149.0, 57.0, 192.0, 65.0, 129.0, 178.0, 228.0] 
        ]
        
        expected_result = [
            [ 1.11e+03, 4.40e+01, 7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02],
            [ 7.71e+01, 1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01],
            [ 4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01],
            [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02],
            [-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01],
            [-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01],
            [7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01],
            [1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00]
        ]
        custom_dct2_result = custom_dct2(input_vector)
        np.testing.assert_allclose(expected_result, custom_dct2_result, rtol=0.1, atol=2.0)

    def test_scipy_dct2(self):
        input_vector = [ 
            [231.0, 32.0, 233.0, 161.0, 24.0, 71.0, 140.0, 245.0],
            [247.0, 40.0, 248.0, 245.0, 124.0, 204.0, 36.0, 107.0],
            [234.0, 202.0, 245.0, 167.0, 9.0, 217.0, 239.0, 173.0],
            [193.0, 190.0, 100.0, 167.0, 43.0, 180.0, 8.0, 70.0],
            [11.0, 24.0, 210.0, 177.0, 81.0, 243.0, 8.0, 112.0],
            [97.0, 195.0, 203.0, 47.0, 125.0, 114.0, 165.0, 181.0],
            [193.0, 70.0, 174.0, 167.0, 41.0, 30.0, 127.0, 245.0],
            [87.0, 149.0, 57.0, 192.0, 65.0, 129.0, 178.0, 228.0] 
        ]
        expected_result = [
            [ 1.11e+03, 4.40e+01, 7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02],
            [ 7.71e+01, 1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01],
            [ 4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01],
            [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02],
            [-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01],
            [-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01],
            [7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01],
            [1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00]
        ]
        scipy_dct2_result = np.array(scipy_dct2_fft(input_vector))
        np.testing.assert_allclose(expected_result, scipy_dct2_result, rtol=0.1, atol=2.0)
   

if __name__ == '__main__':
    unittest.main()
