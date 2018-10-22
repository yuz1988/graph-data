import numpy as np
import re

file_name = 'data/release-youtube-groupmemberships.txt'

user_set = set()
group_map = {}

with open(file_name) as f:
    lines = f.readlines()
    for line in lines:
        vertices = re.split('\s+', line)
        from_v = int(vertices[0])
        to_v = int(vertices[1])
        user_set.add(from_v)
        group_map[to_v] = group_map.get(to_v, 0) + 1

top_groups = []
for k, v in group_map.items():
    if v >= 500:
        top_groups.append(k)


print("Distinct users: {}\n".format(len(user_set)))
print("Distinct groups: {}\n".format(len(top_groups)))

