#HFGT HDF5 output reader by Mehdi Naderi
#August 2025

import h5py
import numpy as np

file_path = r"C:\Users\moham\LIINES Dropbox\Mehdi Naderi\C4-Meg-Convergent-SoS-Anthems\2-MehdiNaderi\liines-python-hfgt-toolbox-V4.4.0\liines-python-hfgt-toolbox-V4.4.0\1_Output_Data\myLFES-Full-EIO-Default-Base-2.hdf5"


def reconstruct_matrix(coords, data, shape):
    if coords.ndim == 1 and coords.size == 2:
        coords = coords.reshape(1, 2)
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    if coords.size == 0:
        return np.zeros((int(shape[0]), int(shape[1])))

    n_rows, n_cols = int(shape[0]), int(shape[1])
    matrix = np.zeros((n_rows, n_cols))
    for (r, c), val in zip(coords, data):
        matrix[int(r), int(c)] = val if np.isscalar(val) else val[0]
    return matrix


def read_mlppos_data(group):
    coords = np.array(group['coords']['value'])
    data = np.array(group['data']['value'])
    shape = np.array(group['myShape']['value']).flatten()
    return reconstruct_matrix(coords, data, shape)

def read_mlpn_data(group):
    coords = np.array(group['coords']['value'])
    data = np.array(group['data']['value'])
    shape = np.array(group['myShape']['value']).flatten()
    return reconstruct_matrix(coords, data, shape)

with h5py.File(file_path, 'r') as f:
    base_path = 'outputData/value'
    mlp_pos_system = read_mlppos_data(f[f'{base_path}/systemProcess/value/MLPPos/value'])
    mlp_neg_system = read_mlpn_data(f[f'{base_path}/systemProcess/value/MLPNeg/value'])

    print("MLPPos (System Process):\n", mlp_pos_system)
    print("\nMLPNeg (System Process):\n", mlp_neg_system)

    diff_system = mlp_pos_system - mlp_neg_system
    print("\n(MLPPos - MLPNeg) (System Process):\n", diff_system)
