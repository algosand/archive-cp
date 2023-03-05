import os,sys
from io import BytesIO, IOBase
sys.setrecursionlimit(10**6)
from typing import *

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

from collections import deque

def main():
    n, m = map(int, input().split())
    queue = deque(range(n))
    adj_list = [[] for _ in range(n)]
    adj_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        adj_matrix[i][i] = 1
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj_list[u].append(v)
        adj_matrix[u][v] = 1
    res = 0
    while queue:
        node = queue.popleft()
        new_neighbors = []
        for nei in adj_list[node]:
            for nei_nei in adj_list[nei]:
                if not adj_matrix[node][nei_nei]:
                    adj_matrix[node][nei_nei] = 1
                    new_neighbors.append(nei_nei)
        while len(new_neighbors) > 0:
            res += len(new_neighbors)
            new_new_neighbors = []
            for nei in new_neighbors:
                for nei_nei in adj_list[nei]:
                    if not adj_matrix[node][nei_nei]:
                        adj_matrix[node][nei_nei] = 1
                        new_new_neighbors.append(nei_nei)
            new_neighbors = new_new_neighbors
    return res
    

if __name__ == '__main__':
    # main()
    print(main())