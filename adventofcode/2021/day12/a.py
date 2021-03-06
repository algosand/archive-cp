from collections import defaultdict
with open("inputs/input.txt", "r") as f:
    raw_data = [(x,y) for x, y in f.read().splitlines().split('-')]
    graph = defaultdict(list)
    for x, y in raw_data:
        graph[x].append(y)
        graph[y].append(x)
    visited = {'start'}
    def dfs(parent, node):
        if node == 'end':
            return 1
        paths = 0
        for nei in graph[node]:
            if (parent.islower() and nei==parent) or nei in visited:
                continue
            if nei.islower():
                visited.add(nei)
            paths += dfs(node, nei)
            if nei.islower():
                visited.remove(nei)
        return paths
    print(dfs('none', 'start'))
# sys.stdout.close