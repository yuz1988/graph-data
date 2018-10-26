import numpy, scipy.io
import re
from scipy import sparse

A = [1,6,3,7]
B = [6,4,1,5]
C = [1,1,1,1]

network_sparse_matrix = sparse.coo_matrix((C, (A, B)), shape=(8, 8))
scipy.io.savemat('network.mat', mdict={'network': network_sparse_matrix})