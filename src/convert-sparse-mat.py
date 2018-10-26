import numpy, scipy.io
import re
from scipy import sparse

NUM_USER = 1138499
GROUPS = 47
network_file_name = "../output/cleaned-youtube-links.txt"
group_file_name = "../output/grouping.txt"

# # create three lists: row, column, value
# user_list, group_list, value_list = [], [], []
# with open(group_file_name, 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         vertices = re.split('\s+', line)
#         user_list.append(int(vertices[0])-1)   # user starts from 0
#         group_list.append(int(vertices[1])-1)  # group number starts from 0
#         value_list.append(1)
#
# # for i in range(len(user_list)):
# #     print(str(user_list[i]) + " " + str(group_list[i]) + " " + str(value_list[i]))
#
# # convert to sparse matrix
# sparse_matrix = sparse.csr_matrix((value_list, (user_list, group_list)),
#                                   shape=(NUM_USER, GROUPS))
# scipy.io.savemat('youtube.mat', mdict={'group': sparse_matrix})



############################################
from_list, to_list, value_list = [], [], []
with open(network_file_name, 'r') as f:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        from_list.append(int(vertices[0]) - 1)  # user starts from 0
        to_list.append(int(vertices[1]) - 1)  # group number starts from 0
        value_list.append(1)
        # symmetry
        from_list.append(int(vertices[1]) - 1)  # user starts from 0
        to_list.append(int(vertices[0]) - 1)  # group number starts from 0
        value_list.append(1)

# convert to sparse matrix
network_sparse_matrix = sparse.csr_matrix((value_list, (from_list, to_list)), shape=(NUM_USER, NUM_USER))
scipy.io.savemat('network.mat', mdict={'network': network_sparse_matrix})

