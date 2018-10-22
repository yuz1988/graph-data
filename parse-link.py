import numpy as np
import re

file_name = 'data/release-youtube-links.txt'
output_file_name = 'output/cleaned-youtube-links.txt'

removed_line_cnt = 0
total_line_cnt = 0
weired_cnt = 0
nodes_set = set()
edges_set = set()

with open(file_name) as f, open(output_file_name, 'w') as output_file:
    lines = f.readlines()
    for line in lines:
        total_line_cnt += 1
        vertices = re.split('\s+', line)
        from_v = int(vertices[0])
        to_v = int(vertices[1])
        from_to_edge = str(from_v) + " " + str(to_v)
        to_from_edge = str(to_v) + " " + str(from_v)
        if (from_to_edge in edges_set) or (to_from_edge in edges_set):
            removed_line_cnt += 1
        else:
            output_file.write("{} {}\n".format(from_v, to_v))
            edges_set.add(from_to_edge)
            nodes_set.add(from_v)
            nodes_set.add(to_v)
            if to_v < from_v:
                weired_cnt += 1

print("Total lines: {}\n".format(total_line_cnt))
print("Removed lines: {}\n".format(removed_line_cnt))
print("Remaining edges: {}\n".format(len(edges_set)))
print("Distinct nodes: {}\n".format(len(nodes_set)))
print("Unique edges with reverse order: {}\n".format(weired_cnt))

