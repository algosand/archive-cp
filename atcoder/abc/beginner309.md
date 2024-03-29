# Atcoder Beginner Contest 309

## What is used at the top of each submission

```py
import os,sys
from io import BytesIO, IOBase
sys.setrecursionlimit(10**6)
from typing import *
# only use pypyjit when needed, it usese more memory, but speeds up recursion in pypy
# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')
# sys.stdout = open('output.txt', 'w')

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
                    
if __name__ == '__main__':
    print(main())
    # main()
    # sys.stdout.close()
```

## A - Nine

### Solution 1:  math + modulus

since a < b it turns out it only is going to be yes if a is indivisible by 3 and b == a + 1

```py
def main():
    a, b = map(int, input().split())
    res = "Yes" if a % 3 and b == a + 1 else "No"
    print(res)

if __name__ == '__main__':
    main()
```

## B - Rotate

### Solution 1:  deque + flatten outside border



```py
from collections import deque

def main():
    n = int(input())
    grid = [list(map(int, input().split())) for _ in range(n)]
    outside = deque()
    for c in range(n):
        outside.append(grid[0][c])
    for r in range(1, n):
        outside.append(grid[r][n-1])
    for c in range(n-2, -1, -1):
        outside.append(grid[n-1][c])
    for r in range(n-2, 0, -1):
        outside.append(grid[r][0])
    for c in range(1, n):
        grid[0][c] = outside.popleft()
    for r in range(1, n):
        grid[r][n-1] = outside.popleft()
    for c in range(n-2, -1, -1):
        grid[n-1][c] = outside.popleft()
    for r in range(n-2, -1, -1):
        grid[r][0] = outside.popleft()
    res = '\n'.join([' '.join(map(str, row)) for row in grid])
    print(res)

if __name__ == '__main__':
    main()
```

## C - Medicine

### Solution 1:  sort + two pointers

```py
def main():
    n, k = map(int, input().split())
    meds = [None] * n
    cur = 0
    for i in range(n):
        a, b = map(int, input().split())
        meds[i] = (a, b)
        cur += b
    meds.sort()
    i = 0
    day = 1
    while cur > k:
        day = meds[i][0]
        while i < n and meds[i][0] == day:
            cur -= meds[i][1]
            i += 1
    print(day)

if __name__ == '__main__':
    main()
```

## D - Add One Edge

### Solution 1: undirected graph + bfs + deque

```py
from collections import deque

def main():
    n1, n2, m = map(int, input().split())
    adj_list = [[] for _ in range(n1 + n2 + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj_list[u].append(v)
        adj_list[v].append(u)
    vis = [0] * (n1 + n2 + 1)
    def bfs(src):
        queue = deque([(src, 0)])
        vis[src] = 1
        while queue:
            node, dist = queue.popleft()
            for nei in adj_list[node]:
                if vis[nei]: continue
                vis[nei] = 1
                queue.append((nei, dist + 1))
        return dist
    res = bfs(1) + bfs(n1 + n2) + 1
    print(res)

if __name__ == '__main__':
    main()
```

## E - Family and Insurance

### Solution 1:  directed graph + tree + bfs

The trick is just keep the track of the remaining descendants that can be covered by the current insurance

```py
from collections import deque, Counter

def main():
    n, m  = map(int, input().split())
    parent = [0] * 2 + list(map(int, input().split()))
    queries = Counter()
    for i in range(m):
        x, y = map(int, input().split())
        queries[x] = max(queries[x], y + 1)
    adj_list = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        adj_list[parent[i]].append(i)
    queue = deque([(1, queries[1])])
    vis = [0] * (n + 1)
    vis[1] = 1
    res = 0
    while queue:
        node, depth = queue.popleft()
        if depth > 0: res += 1
        for nei in adj_list[node]:
            if vis[nei]: continue
            vis[nei] = 1
            queue.append((nei, max(depth - 1, queries[nei])))
    print(res)

if __name__ == '__main__':
    main()
```

## F - Box in Box

### Solution 1:  sort + offline queries + minimum segment tree + coordinate compression

This is good segment tree problem you can sort It turns out that you can use any permutation of h, w, d with some rotation of a rectangular prism.  So then what you can do is consider the problem of sorting by h in ascending order, so that for j > i it is true that hj >= hi.  So smaller ones processed first, But since they can be equal you will want to sort wi in descending order.  Then what can be done is created a segment tree that will hold the minimum di for each wi.  Need to use coordinate compression on wi and segment tree.  Then can query a range from [0, wi - 1] with segment tree to get minimum di and if di < dj, it is already guaranteed wi < wj and that hi < hj.  so that is the solution.

```py
import math

class SegmentTree:
    def __init__(self, n: int, neutral: int, func):
        self.func = func
        self.neutral = neutral
        self.size = 1
        self.n = n
        while self.size<n:
            self.size*=2
        self.nodes = [neutral for _ in range(self.size*2)]

    def ascend(self, segment_idx: int) -> None:
        while segment_idx > 0:
            segment_idx -= 1
            segment_idx >>= 1
            left_segment_idx, right_segment_idx = 2*segment_idx + 1, 2*segment_idx + 2
            self.nodes[segment_idx] = self.func(self.nodes[left_segment_idx], self.nodes[right_segment_idx])
        
    def update(self, segment_idx: int, val: int) -> None:
        segment_idx += self.size - 1
        self.nodes[segment_idx] = self.func(self.nodes[segment_idx], val)
        self.ascend(segment_idx)
            
    def query(self, left: int, right: int) -> int:
        stack = [(0, self.size, 0)]
        result = self.neutral
        while stack:
            # BOUNDS FOR CURRENT INTERVAL and idx for tree
            segment_left_bound, segment_right_bound, segment_idx = stack.pop()
            # NO OVERLAP
            if segment_left_bound >= right or segment_right_bound <= left: continue
            # COMPLETE OVERLAP
            if segment_left_bound >= left and segment_right_bound <= right:
                result = self.func(result, self.nodes[segment_idx])
                continue
            # PARTIAL OVERLAP
            mid_point = (segment_left_bound + segment_right_bound) >> 1
            left_segment_idx, right_segment_idx = 2*segment_idx + 1, 2*segment_idx + 2
            stack.extend([(mid_point, segment_right_bound, right_segment_idx), (segment_left_bound, mid_point, left_segment_idx)])
        return result
    
    def __repr__(self) -> str:
        return f"nodes array: {self.nodes}, next array: {self.nodes}"

def main():
    n = int(input())
    boxes = [None] * n
    widths = set()
    compressed = {}
    for i in range(n):
        triplet = sorted(map(int, input().split()))
        boxes[i] = triplet
        widths.add(triplet[1])
    for i, w in enumerate(sorted(widths)):
        compressed[w] = i
    min_seg_tree = SegmentTree(len(widths), math.inf, min)
    # box[i] = (hi, wi, di)
    # sort by ascending order of h, and descending order in w
    boxes.sort(key = lambda box: (box[0], -box[1]))
    for _, w, d in boxes:
        left, right = 0, compressed[w]
        min_d = min_seg_tree.query(left, right)
        if min_d < d: return print("Yes")
        min_seg_tree.update(right, d)
    print("No")

if __name__ == '__main__':
    main()
```

## G - Ban Permutation

### Solution 1:  bitmask window + dynamic programming + inclusion exclusion principle + factorial

Instead of solving the problem for |Pi - i| >= X , try solving the problem with dynamic programming for |Pi - i| < X 
And then use inclusion exclusion principle to get the answer for |Pi - i| >= X.  

Inclusion Exclusion principle is needed for this because thereare overlapping, and you want to take the union of all the sets.  It is similar to derangement problem and I used that one to help understand why this works. 

![images](images/ban_permutation_1.png)
![images](images/ban_permutation_2.png)
![images](images/ban_permutation_3.png)
![images](images/ban_permutation_4.png)

```py
def factorials(n, mod):
    fact = [1]*(n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i - 1] * i) % mod
    return fact

def main():
    N, X = map(int, input().split())
    mod = 998244353
    fact = factorials(N, mod)
    window_size = 2 * X - 1
    dp = [[0] * (1 << window_size)]
    dp[0][0] = 1
    for i in range(N):
        ndp = [[0] * (1 << window_size) for _ in range(i + 2)]
        for taken in range(i + 1):
            for mask in range(1 << window_size):
                if dp[taken][mask] == 0: continue
                for disp in range(-X + 1, X):
                    if i + disp < 0 or i + disp >= N: continue
                    window_index = disp + X - 1
                    if mask & (1 << window_index): continue
                    new_mask = (mask | (1 << window_index)) >> 1
                    # taking valid i where |P_i - i| < X
                    ndp[taken + 1][new_mask] += dp[taken][mask]
                # not taking an integer, but upgrading the mask for the window
                new_mask = mask >> 1
                ndp[taken][new_mask] += dp[taken][mask]
        dp = ndp
    res = 0
    for taken in range(N + 1):
        cur = 0
        for mask in range(1 << window_size):
            cur = (cur + dp[taken][mask]) % mod
        if taken & 1:
            res = (res - cur * fact[N - taken]) % mod
        else:
            res = (res + cur * fact[N - taken]) % mod
    print(res)
    
if __name__ == '__main__':
    main()
```