# Atcoder Beginner Contest 331

## D. Tile Pattern

### Solution 1:  2D prefix sum + periodicity

```py
from itertools import product

def main():
    N, Q = map(int, input().split())
    grid = [list(input()) for _ in range(N)]
    psum = [[0] * (N + 1) for _ in range(N + 1)]
    for r, c in product(range(1, N + 1), repeat = 2):
        psum[r][c] = psum[r - 1][c] + psum[r][c - 1] - psum[r - 1][c - 1] + (grid[r - 1][c - 1] == "B")
    def g(r, c):
        r_span, c_span = r // N, c // N
        return (
            psum[N][N] * r_span * c_span
            + psum[N][c % N] * r_span
            + psum[r % N][N] * c_span
            + psum[r % N][c % N]
        )
    def f(r1, c1, r2, c2):
        return g(r2, c2) - g(r1, c2) - g(r2, c1) + g(r1, c1)
    for _ in range(Q):
        r1, c1, r2, c2 = map(int, input().split())
        print(f(r1, c1, r2 + 1, c2 + 1))

if __name__ == '__main__':
    main()
```

## E - Set Meal 

### Solution 1:  hash map, sort, offline query

```py
def main():
    N, M, L = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    sides = sorted(range(M), key = lambda i: B[i], reverse = True)
    bad_combos = [set() for _ in range(N)]
    for _ in range(L):
        c, d = map(int, input().split())
        c -= 1
        d -= 1
        bad_combos[c].add(d)
    ans = 0
    for i in range(N):
        for j in sides:
            if j not in bad_combos[i]:
                ans = max(ans, A[i] + B[j])
                break
    print(ans)
    
if __name__ == '__main__':
    main()
```

## F - Palindrome Query 

### Solution 1:  rolling hash on segment tree

```py
class SegmentTree:
    def __init__(self, n, neutral, func, initial_arr):
        self.func = func
        self.neutral = neutral
        self.size = 1
        self.n = n
        while self.size<n:
            self.size*=2
        self.nodes = [neutral for _ in range(self.size*2)] 
        self.build(initial_arr)

    def build(self, initial_arr):
        for i, segment_idx in enumerate(range(self.n)):
            segment_idx += self.size - 1
            val = initial_arr[i]
            self.nodes[segment_idx] = val
            self.ascend(segment_idx)

    def ascend(self, segment_idx):
        while segment_idx > 0:
            segment_idx -= 1
            segment_idx >>= 1
            left_segment_idx, right_segment_idx = 2*segment_idx + 1, 2*segment_idx + 2
            self.nodes[segment_idx] = self.func(self.nodes[left_segment_idx], self.nodes[right_segment_idx])
        
    def update(self, segment_idx, val):
        segment_idx += self.size - 1
        self.nodes[segment_idx] = val
        self.ascend(segment_idx)
            
    def query(self, left, right):
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
    
    def __repr__(self):
        return f"nodes array: {self.nodes}, next array: {self.nodes}"

import random
import math    

mod = 2**61 - 1
base0 = 3

while True:
    k = random.randint(1, mod - 1)
    base = pow(base0, k, mod)
    if base <= ord("z"): continue
    if math.gcd(base, mod - 1) != 1: continue
    break

def main():
    N, Q = map(int, input().split())
    S = input()
    pw = [1] * (N + 1)
    for i in range(N):
        pw[i + 1] = (pw[i] * base) % mod
    segfunc = lambda a, b: ((a[0] + (b[0] * pw[a[1]]) % mod) % mod, a[1] + b[1])
    seg = SegmentTree(N, (0, 0), segfunc, [(ord(ch), 1) for ch in S])
    seg_rev = SegmentTree(N, (0, 0), segfunc, [(ord(ch), 1) for ch in reversed(S)])
    for _ in range(Q):
        t, l, r = input().split()
        if t == "1":
            x, c = int(l) - 1, ord(r)
            seg.update(x, (c, 1))
            seg_rev.update(N - x - 1, (c, 1))
        else:
            l, r = int(l) - 1, int(r) - 1
            h = seg.query(l, r + 1)
            l_rev, r_rev = N - r - 1, N - l - 1
            h_rev = seg_rev.query(l_rev, r_rev + 1)
            if h == h_rev: print("Yes")
            else: print("No")

if __name__ == '__main__':
    main()
```

```cpp

```

## G - Collect Them All 

### Solution 1:  fast fourier transform, dynamic programming, combinatorics, absorbing markov chains

```py
from collections import deque
from itertools import product

class FFT:
    """
    https://github.com/shakayami/ACL-for-python/blob/master/convolution.py
    """
    def primitive_root_constexpr(self, m):
        if m == 2: return 1
        if m == 167772161: return 3
        if m == 469762049: return 3
        if m == 754974721: return 11
        if m == 998244353: return 3
        divs = [0] * 20
        divs[0] = 2
        x = (m - 1) // 2
        while x % 2 == 0: x //= 2
        i = 3
        cnt = 1
        while i * i <= x:
            if x % i == 0:
                divs[cnt] = i
                cnt += 1 
                while x % i == 0: x //= i
            i += 2
        if x > 1:
            divs[cnt] = x
            cnt += 1
        g = 2
        while 1:
            ok = True
            for i in range(cnt):
                if pow(g, (m - 1) // divs[i], m) == 1: 
                    ok = False
                    break
            if ok: return g
            g += 1
    # bit scan forward, finds the rightmost set bit? maybe? 
    def bsf(self, x):
        res = 0
        while x % 2 == 0:
            res += 1
            x //= 2
        return res
    rank2 = 0
    root = []
    iroot = []
    rate2 = []
    irate2 = []
    rate3 = []
    irate3 = []
    def __init__(self, MOD):
        self.mod = MOD
        self.g = self.primitive_root_constexpr(self.mod)
        self.rank2 = self.bsf(self.mod - 1)
        self.root = [0] * (self.rank2 + 1)
        self.iroot = [0] * (self.rank2 + 1)
        self.rate2 = [0] * self.rank2
        self.irate2 = [0] * self.rank2
        self.rate3 = [0] * (self.rank2 - 1)
        self.irate3 = [0] * (self.rank2 - 1)
        self.root[self.rank2] = pow(self.g, (self.mod - 1) >> self.rank2, self.mod)
        self.iroot[self.rank2] = pow(self.root[self.rank2], self.mod - 2, self.mod)
        for i in range(self.rank2 - 1, -1, -1):
            self.root[i] = (self.root[i + 1] ** 2) % self.mod
            self.iroot[i] = (self.iroot[i + 1] ** 2) % self.mod
        prod = iprod = 1
        for i in range(self.rank2 - 1):
            self.rate2[i] = (self.root[i + 2] * prod) % self.mod
            self.irate2[i] = (self.iroot[i + 2] * iprod) % self.mod
            prod = (prod * self.iroot[i + 2]) % self.mod
            iprod = (iprod * self.root[i + 2]) % self.mod
        prod = iprod = 1
        for i in range(self.rank2 - 2):
            self.rate3[i] = (self.root[i + 3] * prod) % self.mod
            self.irate3[i] = (self.iroot[i + 3] * iprod) % self.mod
            prod = (prod * self.iroot[i + 3]) % self.mod
            iprod = (iprod * self.root[i + 3]) % self.mod
    def butterfly(self, a):
        n = len(a)
        h = (n - 1).bit_length()
        LEN = 0
        while LEN < h:
            if h - LEN == 1:
                p = 1 << (h - LEN - 1)
                rot = 1
                for s in range(1 << LEN):
                    offset = s << (h - LEN)
                    for i in range(p):
                        l = a[i + offset]
                        r = a[i + offset + p] * rot
                        a[i + offset] = (l + r) % self.mod
                        a[i + offset + p] = (l - r) % self.mod
                    rot *= self.rate2[(~s & -~s).bit_length() - 1]
                    rot %= self.mod
                LEN += 1
            else:
                p = 1 << (h - LEN - 2)
                rot = 1
                imag = self.root[2]
                for s in range(1 << LEN):
                    rot2 = (rot * rot) % self.mod
                    rot3 = (rot2 * rot) % self.mod 
                    offset = s << (h - LEN)
                    for i in range(p):
                        a0 = a[i + offset]
                        a1 = a[i + offset + p] * rot
                        a2 = a[i + offset + 2 * p] * rot2
                        a3 = a[i + offset + 3 * p] * rot3
                        a1na3imag = (a1 - a3) % self.mod * imag
                        a[i + offset] = (a0 + a1 + a2 + a3) % self.mod
                        a[i + offset + p] = (a0 + a2 - a1 - a3) % self.mod
                        a[i + offset + 2 * p] = (a0 - a2 + a1na3imag) % self.mod
                        a[i + offset + 3 * p] = (a0 - a2 - a1na3imag) % self.mod
                    rot *= self.rate3[(~s & -~s).bit_length() - 1]
                    rot %= self.mod
                LEN += 2
    def butterfly_inv(self, a):
        n = len(a)
        h = (n - 1).bit_length()
        LEN = h
        while LEN:
            if LEN == 1:
                p = 1 << (h - LEN)
                irot = 1
                for s in range(1 << (LEN - 1)):
                    offset = s << (h - LEN + 1)
                    for i in range(p):
                        l = a[i + offset]
                        r = a[i + offset + p]
                        a[i + offset] = (l + r) % self.mod
                        a[i + offset + p] = (l - r) * irot % self.mod
                    irot *= self.irate2[(~s & -~s).bit_length() - 1]
                    irot %= self.mod
                LEN -= 1
            else:
                p = 1 << (h - LEN)
                irot = 1
                iimag = self.iroot[2]
                for s in range(1 << (LEN - 2)):
                    irot2 = (irot * irot) % self.mod
                    irot3 = (irot * irot2) % self.mod
                    offset = s << (h - LEN + 2)
                    for i in range(p):
                        a0 = a[i + offset]
                        a1 = a[i + offset + p]
                        a2 = a[i + offset + 2 * p]
                        a3 = a[i + offset + 3 * p]
                        a2na3iimag = (a2 - a3) * iimag % self.mod
                        a[i + offset] = (a0 + a1 + a2 + a3) % self.mod
                        a[i + offset + p] = (a0 - a1 + a2na3iimag) * irot % self.mod
                        a[i + offset + 2 * p] = (a0 + a1 - a2 - a3) * irot2 % self.mod
                        a[i + offset + 3 * p] = (a0 - a1 - a2na3iimag) * irot3 % self.mod
                    irot *= self.irate3[(~s & -~s).bit_length() - 1]
                    irot %= self.mod
                LEN -= 2
    def convolution(self, a, b):
        n = len(a)
        m = len(b)
        if not (a) or not (b): return []
        if min(n, m) <= 40: # naive solution
            res = [0] * (n + m - 1)
            for i, j in product(range(n), range(m)):
                res[i + j] += a[i] * b[j]
                res[i + j] %= self.mod
            return res
        z = 1 << (n + m - 2).bit_length()
        a = a + [0] * (z - n)
        b = b + [0] * (z - m)
        self.butterfly(a)
        self.butterfly(b)
        c = [(a[i] * b[i]) % self.mod for i in range(z)]
        self.butterfly_inv(c)
        iz = pow(z, self.mod - 2, self.mod)
        for i in range(n + m - 1):
            c[i] = (c[i] * iz) % self.mod
        return c[: n + m - 1]
    
def mod_inverse(x):
    return pow(x, mod - 2, mod) % mod

mod = 998244353
def main():
    N, M = map(int, input().split())
    C = list(map(int, input().split()))
    fft = FFT(mod)
    queue = deque()
    for c in C:
        X = [0] * (c + 1)
        X[0] = 1
        X[c] = -1
        queue.append(X)
    while len(queue) > 1:
        a = queue.popleft()
        b = queue.popleft()
        queue.append(fft.convolution(a, b))
    ans = 0
    for k in range(N):
        ans += N * mod_inverse(N - k) * queue[0][k] % mod
        ans %= mod
    if M % 2 == 0:
        ans *= -1
        ans %= mod
    print(ans)
if __name__ == '__main__':
    main()
```