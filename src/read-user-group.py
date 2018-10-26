import numpy as np
import re

file_name = '../data/release-youtube-groupmemberships.txt'
output_file_name = "../output/grouping.txt"

THRESHOLD = 500
user_set = set()
group_map = {}

with open(file_name) as f:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        user = int(vertices[0])
        group = int(vertices[1])
        user_set.add(user)

        if group not in group_map:
            group_map[group] = []
        group_map[group].append(user)

print("Total groups: {}\n".format(len(group_map)))
print("Total distinct users: {}\n".format(len(user_set)))

top_groups_list = []
top_group_users = set()
for k, v in group_map.items():
    if len(v) >= THRESHOLD:
        top_groups_list.append(k)
        for user in v:
            top_group_users.add(user)

print("Groups with more than {} users: {}\n".format(THRESHOLD, len(top_groups_list)))
print("Number of users in top groups: {}\n".format(len(top_group_users)))

# convert top group numbers to from 1 to n (n = len(top_groups))
top_N = len(top_groups_list)
top_groups_list.sort()
group_mapping_dict = {}
for i in range(top_N):
    group_mapping_dict[top_groups_list[i]] = i+1

with open(file_name) as f, open(output_file_name, 'w') as output_file:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        user = int(vertices[0])
        group = int(vertices[1])
        if group in group_mapping_dict:
            output_file.write("{} {}\n".format(user, group_mapping_dict[group]))

