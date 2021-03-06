# Shortest Routes I

## Solution: Classic Dijkstra Algorithm to find shortest distance to all nodes from a single source node. 

```py
from collections import defaultdict
from math import inf
from heapq import heappush, heappop

def dijkstra(src):
    dist = [inf]*(n+1)
    minheap = []
    heappush(minheap, (0, src))
    while minheap:
        distance, city = heappop(minheap)
        if dist[city] < inf: continue
        dist[city] = distance
        for ncity, nw in graph[city]:
            ndistance = distance + nw
            if ndistance < dist[ncity]:
                heappush(minheap, (ndistance, ncity))
    return " ".join(map(str, dist[1:]))

if __name__ == '__main__':
    n, m = map(int, input().split())
    graph = defaultdict(list)
    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a].append((b,c))
    print(dijkstra(1))
```