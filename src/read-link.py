import re

# input file name
in_file_name = '../data/release-youtube-links.txt'

# output file name
out_link_file_name = '../output/cleaned-youtube-links.txt'
out_user_mapping_file_name = '../output/user-sparse-to-dense-mapping.txt'

user_set = set()
adj_map = {}   # adjacency list

with open(in_file_name) as f:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        from_v = int(vertices[0])
        to_v = int(vertices[1])
        if from_v != to_v:
            if from_v not in adj_map:
                adj_map[from_v] = set()
            if to_v not in adj_map:
                adj_map[to_v] = set()
            adj_map[from_v].add(to_v)
            adj_map[to_v].add(from_v)
            user_set.add(from_v)
            user_set.add(to_v)

print("Number of distinct users: {}\n".format(len(user_set)))

# create sparse to dense (consecutive from 0) user mapping.
user_list = list(user_set)
user_list.sort()
sparse_to_dense_user_mapping = {}
dense_to_sparse_user_mapping = {}
with open(out_user_mapping_file_name, 'w') as out:
    for i in range(len(user_list)):
        dense_to_sparse_user_mapping[i] = user_list[i]
        sparse_to_dense_user_mapping[user_list[i]] = i
        out.write("{} {}\n".format(user_list[i], i))
print("User sparse to dense mapping file has been written.\n")


# generate compressed adjacency list.
compressed_adj_list = []
for i in range(len(user_list)):
    neighbor_list = adj_map[dense_to_sparse_user_mapping[i]]
    compressed_user_list = []
    for user in neighbor_list:
        compressed_user_list.append(sparse_to_dense_user_mapping[user])
    compressed_user_list.sort()
    compressed_adj_list.append(compressed_user_list)

# write compressed links to file, keep links: from_v < to_v.
with open(out_link_file_name, 'w') as output_file:
    for i in range(len(compressed_adj_list)):
        for j in compressed_adj_list[i]:
            if i < j:
                output_file.write("{} {}\n".format(i, j))
