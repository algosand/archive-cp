import os,sys
from io import BytesIO, IOBase
from typing import *
import math
from collections import deque


# Fast IO Region
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

"""
FordFulkeron algorithm for maximum flow problem 
- pluggable augmenting path finding algorithms
- residual graph
- bottleneck capacity
- flow edge class
- depth first search
- Edmonds-Karp algorithm
- capacity scaling algorithm
- dinics algorithm
-- deadend elimination
TODO: May need to merge parallel edges at some point

"""
class FlowEdge:
    def __init__(self, src: int, dst: int, cap: int):
        self.src = src # source node
        self.dst = dst # destination node
        self.cap = cap
        self.flow = 0

    def __repr__(self):
        return f'source node: {self.src}, destination node: {self.dst}, capacity: {self.cap}, flow: {self.flow} ======'

class FordFulkersonMaxFlowV2:
    """
    Ford-Fulkerson algorithm 
    - pluggable augmenting path finding algorithms
    - residual graph
    - bottleneck capacity
    """
    def __init__(self, n: int, edges: List[Tuple[int, int, int]]):
        self.size = n
        self.edges = edges

    def build(self, n: int, edges: List[Tuple[int, int, int]]) -> None:
        self.flowedges = []
        self.adj_list = {}
        self.delta = 0
        for u, v, cap in edges:
            self.flowedges.append(FlowEdge(u, v, cap))
            if u not in self.adj_list:
                self.adj_list[u] = []
            self.adj_list[u].append(len(self.flowedges) - 1)
            self.flowedges.append(FlowEdge(v, u, 0)) # residual edge
            if v not in self.adj_list:
                self.adj_list[v] = []
            self.adj_list[v].append(len(self.flowedges) - 1)
            self.delta = max(self.delta, cap)
        highest_bit_set = self.delta.bit_length() - 1
        self.delta = 1 << highest_bit_set

    def main_dfs(self, source: int, sink: int) -> int:
        self.build(self.size, self.edges)
        maxflow = 0
        while True:
            self.reset()
            cur_flow = self.dfs(source, sink, math.inf)
            if cur_flow == 0:
                break
            maxflow += cur_flow
        return maxflow

    def reset(self) -> None:
        self.vis = [0] * self.size

    def neighborhood(self, node: int) -> List[int]:
        return (i for i in self.adj_list[node])

    def residual_capacity(self, edge: FlowEdge) -> int:
        return edge.cap - edge.flow

    def dfs(self, node: int, sink: int, flow: int) -> int:
        if node == sink:
            return flow
        self.vis[node] = 1
        for index in self.neighborhood(node):
            nei = self.flowedges[index]
            if self.vis[nei.dst] == 0 and self.residual_capacity(nei) > 0:
                cur_flow = self.dfs(nei.dst, sink, min(flow, self.residual_capacity(nei)))
                if cur_flow > 0:
                    nei.flow += cur_flow
                    self.flowedges[index ^ 1].flow -= cur_flow
                    return cur_flow
        return 0
    
    def main_edmonds_karp(self, source: int, sink: int) -> int:
        self.build(self.size, self.edges)
        maxflow = 0
        while True:
            self.reset()
            self.parents = [-1] * len(self.flowedges)
            cur_flow = self.edmonds_karp(source, sink)
            if cur_flow == 0:
                break
            maxflow += cur_flow
        return maxflow

    def edmonds_karp(self, source: int, sink: int) -> int:
        queue = deque([(source, math.inf, -1)])
        self.vis[source] = 1
        while queue:
            node, flow, prev_index = queue.popleft()
            if node == sink:
                break
            for index in self.neighborhood(node):
                nei = self.flowedges[index]
                if self.vis[nei.dst] == 0 and self.residual_capacity(nei) > 0:
                    self.vis[nei.dst] = 1
                    self.parents[index] = prev_index
                    queue.append((nei.dst, min(flow, self.residual_capacity(nei)), index))
        if node == sink:
            while prev_index != -1:
                parent_index = self.parents[prev_index]
                self.flowedges[prev_index].flow += flow
                self.flowedges[prev_index^1].flow -= flow # residual edge
                prev_index = parent_index
            return flow
        return 0

    def main_capacity_scaling(self, source: int, sink: int) -> int:
        self.build(self.size, self.edges)
        maxflow = 0
        while self.delta > 0:
            while True:
                self.reset()
                cur_flow = self.capacity_scaling(source, sink, math.inf)
                if cur_flow == 0:
                    break
                maxflow += cur_flow
            self.delta >>= 1
        return maxflow

    def capacity_scaling(self, node: int, sink: int, flow: int) -> int:
        if node == sink:
            return flow
        self.vis[node] = 1
        for index in self.neighborhood(node):
            nei = self.flowedges[index]
            if self.vis[nei.dst] == 0 and self.residual_capacity(nei) >= self.delta:
                cur_flow = self.capacity_scaling(nei.dst, sink, min(flow, self.residual_capacity(nei)))
                if cur_flow > 0:
                    nei.flow += cur_flow
                    self.flowedges[index ^ 1].flow -= cur_flow
                    return cur_flow
        return 0

    def dinics_bfs(self, source: int, sink: int) -> bool:
        self.distances = [-1] * self.size
        self.distances[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for index in self.neighborhood(node):
                nei = self.flowedges[index]
                if self.distances[nei.dst] == -1 and self.residual_capacity(nei) > 0:
                    self.distances[nei.dst] = self.distances[node] + 1
                    queue.append(nei.dst)
        return self.distances[sink] != -1

    def dinics_dfs(self, node: int, sink: int, flow: int) -> int:
        if flow == 0: return 0
        if node == sink: return flow
        while self.ptr[node] < len(self.adj_list[node]):
            index = self.adj_list[node][self.ptr[node]]
            self.ptr[node] += 1
            nei = self.flowedges[index]
            if self.distances[nei.dst] == self.distances[node] + 1 and self.residual_capacity(nei) > 0:
                cur_flow = self.dinics_dfs(nei.dst, sink, min(flow, self.residual_capacity(nei)))
                if cur_flow > 0:
                    nei.flow += cur_flow
                    self.flowedges[index ^ 1].flow -= cur_flow
                    return cur_flow
        return 0

    def main_dinics(self, source: int, sink: int) -> int:
        self.build(self.size, self.edges)
        maxflow = 0
        while self.dinics_bfs(source, sink):
            self.reset()
            self.ptr = [0] * self.size # pointer to the next edge to be processed (optimizes for dead ends)
            while True:
                cur_flow = self.dinics_dfs(source, sink, math.inf)
                if cur_flow == 0:
                    break
                maxflow += cur_flow
        return maxflow
    
    def general_path_cover(self, source: int, sink: int) -> int:
        self.path, self.paths = [], []
        self.vis = [0] * len(self.flowedges)
        for index in self.neighborhood(source):
            fedge = self.flowedges[index]
            if fedge.flow != 1: continue
            self.vis[index] = 1
            self.path.append(source)
            self.path_dfs(self.flowedges[index].dst, sink, source)
            self.path.pop()
        return self.paths

    def path_dfs(self, node: int, sink: int, parent: int) -> None:
        # print('node', node, 'path', self.path)
        if node == sink:
            self.paths.append([i + 1 for i in self.path + [node]])
            return
        # print('node', node, 'neighbors', list(self.neighborhood(node)))
        for index in self.neighborhood(node):
            fedge = self.flowedges[index]
            if self.vis[index]: continue
            self.vis[index] = 1
            # print('node', node, 'fedge', fedge)
            if fedge.flow == 1:
                self.path.append(node)
                self.path_dfs(fedge.dst, sink, node)
                self.path.pop()
                return

def main():
    n, m = map(int, input().split())
    edges = [None] * m
    for i in range(m):
        u, v = map(int, input().split())
        edges[i] = (u - 1, v - 1, 1)
    source, sink = 0, n - 1
    maxflow = FordFulkersonMaxFlowV2(n, edges)
    mf = maxflow.main_dinics(source, sink)
    # print(maxflow.flowedges)
    print(mf)
    paths = maxflow.general_path_cover(source, sink)
    for path in paths:
        print(len(path))
        print(*path)
    
    
if __name__ == '__main__':
    main()