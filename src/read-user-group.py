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
        from_v = int(vertices[0])
        to_v = int(vertices[1])
        user_set.add(from_v)

        if to_v not in group_map:
            group_map[to_v] = []
        group_map[to_v].append(from_v)

print("Total groups: {}\n".format(len(group_map)))

top_groups = {}
for k, v in group_map.items():
    if len(v) >= THRESHOLD:
        top_groups[k] = v

print("Distinct users: {}\n".format(len(user_set)))
print("Distinct groups with more than {} users: {}\n".format(THRESHOLD, len(top_groups)))

with open(file_name) as f, open(output_file_name, 'w') as output_file:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        from_v = int(vertices[0])
        to_v = int(vertices[1])
        if to_v in top_groups:
            output_file.write(line)
