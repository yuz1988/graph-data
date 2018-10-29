import re

# input file name
in_file_name = '../data/release-youtube-links.txt'
in_group_file_name = '../data/release-youtube-groupmemberships.txt'

# output file name
out_link_file_name = '../output/cleaned-youtube-links.txt'
out_user_mapping_file_name = '../output/user-sparse-to-dense-mapping.txt'
out_group_file_name = "../output/grouping.txt"

THRESHOLD = 500

user_set = set()
adj_map = {}  # adjacency map

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

# Create sparse to dense (consecutive from 0) user mapping.
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

# Generate compressed adjacency list.
compressed_adj_list = []
for i in range(len(user_list)):
    neighbor_list = adj_map[dense_to_sparse_user_mapping[i]]
    compressed_user_list = []
    for user in neighbor_list:
        compressed_user_list.append(sparse_to_dense_user_mapping[user])
    compressed_user_list.sort()
    compressed_adj_list.append(compressed_user_list)

# Write compressed links to file, keep links: from_v < to_v.
with open(out_link_file_name, 'w') as output_file:
    for i in range(len(compressed_adj_list)):
        for j in compressed_adj_list[i]:
            if i < j:
                output_file.write("{} {}\n".format(i, j))

# Process group membership.
group_map = {}
with open(in_group_file_name) as f:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        user = int(vertices[0])
        group = int(vertices[1])
        if user in user_set:
            if group not in group_map:
                group_map[group] = []
            group_map[group].append(sparse_to_dense_user_mapping[user])


print("Total groups: {}\n".format(len(group_map)))

top_groups_list = []
top_group_users = set()
for k, v in group_map.items():
    if len(v) >= THRESHOLD:
        top_groups_list.append(k)
        for user in v:
            top_group_users.add(user)

print("Groups with more than {} users: {}\n".format(THRESHOLD, len(top_groups_list)))
print("Number of users in top groups: {}\n".format(len(top_group_users)))

# Convert top group numbers to from 1 to n (n = len(top_groups))
top_N = len(top_groups_list)
top_groups_list.sort()
group_mapping_dict = {}
for i in range(top_N):
    group_mapping_dict[top_groups_list[i]] = i

with open(in_group_file_name) as f, open(out_group_file_name, 'w') as output_file:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        user = int(vertices[0])
        group = int(vertices[1])
        if (group in group_mapping_dict) and (user in user_set):
            output_file.write("{} {}\n".format(sparse_to_dense_user_mapping[user],
                                               group_mapping_dict[group]))
