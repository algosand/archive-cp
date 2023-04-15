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

from collections import deque, Counter

def main():
    n, a, b, p, q = map(int, input().split())
    in_queue = set([(a, b, 0)])
    queue = deque([(a, b, 0)])
    memo = Counter()
    while queue:
        pos1, pos2, turn = queue.popleft()
        print('pos1, pos2, turn', pos1, pos2, turn)
        print('memo', memo)
        in_queue.remove((pos1, pos2, turn))
        if turn == 0:
            for i in range(1, p + 1):
                new_pos = min(pos1 + i, n)
                state = (new_pos, pos2, turn ^ 1)
                memo[state] += 1
                if state in in_queue or new_pos == n: continue
                in_queue.add(state)
                queue.append(state)
        else:
            for i in range(1, q + 1):
                new_pos = min(pos2 + i, n)
                state = (pos1, new_pos, turn ^ 1)
                memo[state] += 1
                if new_pos == n: break
                if state in in_queue: continue
                in_queue.add(state)
                queue.append(state)
    print(memo)
    a_win = b_win = 0
    for p1, p2, t in memo:
        if p1 == n:
            a_win += memo[(p1, p2, t)]
        elif p2 == n:
            b_win += memo[(p1, p2, t)]
    print(a_win, b_win)
            

if __name__ == '__main__':
    main()
