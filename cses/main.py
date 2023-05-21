import os,sys
from io import BytesIO, IOBase
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

sys.setrecursionlimit(1_000_000)
# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')

import math

def main():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    points.sort()
    points_y = sorted(points, key=lambda x: x[1])
    euclidean_dist = lambda p1, p2: (p1[0] - p2[0])**2+(p1[1] - p2[1])**2
    def divide(points, points_y):
        n = len(points)
        if n <= 1: return math.inf
        left_points = points[:n//2]
        right_points = points[n//2:]
        left_points_y, right_points_y = [], []
        mid_x = left_points[-1][0]
        mid_y = left_points[-1][1]
        for x, y in points:
            if (x, y) <= (mid_x, mid_y):
                left_points_y.append((x, y))
            else:
                right_points_y.append((x, y))
        # divide
        d = min(divide(left_points, left_points_y), divide(right_points, right_points_y))
        # left [left, mid)
        # right [mid, right)
        # merge
        strip = []
        for x, y in points_y:
            if abs(x - mid_x) <= d:
                strip.append((x, y))
        for i in range(len(strip)):
            for j in range(i+1, len(strip)):
                if strip[j][1] - strip[i][1] >= d: break
                d = min(d, euclidean_dist(strip[i], strip[j]))
        return d
    return divide(points, points_y)
        
if __name__ == '__main__':
    print(main())
    # T = int(input())
    # for _ in range(T):
    #     print(main())
