
# Part 1

We just need to count the digits that have a unique number of on segments.  This is 2,3,4,7.
I can create a set and then just count the number of these that have that size int he output of the patterns


```py
A = f.read().splitlines()
sizeDigitMap = {2,4,3,7}
outputs = [x[x.find('|')+2:].split() for x in A]
cnt = sum(1 for out in outputs for pat in out if len(pat) in sizeDigitMap)
print(cnt)
```

# Part 2
This problem can be solved a couple ways.  One way is with permutations 
Still need to explore the permutation method. 
DFS + backtracking algorithm with OOP
So I use the fact that there are a certain number of on segments that need to be on in common for 
a pattern to be valid.  Such as maybe 1 and 2 need to always have 2 segments in common. so given each 
alphabet character represents a specific segment being on.  We don't know which segment. But with this
comparison between them we can say for certain if a having a character assigned to a segment is appropriate. 

Another way to approach this would be with generating all permutations of having characters
represent certain segments.  Then just need to check that it works as well.  

```py
class SevenSegmentSearch:
    def __init__(self):
        self.baseMap = {0 : 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf', 5: 'abdfg', 6: 'abdefg',
        7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
        # list of list data structure for storing the number of wires in common between digits
        self.inCommon = [[len(set(self.baseMap[i])&set(self.baseMap[j])) for i in range(10)] for j in range(10)]
        data = self.loadData()
        self.outputs = [x[x.find('|')+2:].split() for x in data]
        self.inputs = [x[:x.find('|')].split() for x in data]
        self.vis = set()
        self.patterns = list()

    def loadData(self, path = "inputs/input.txt"):
        with open(path, "r") as f:
            A = f.read().splitlines()
        return A
    
    def getOutput(self, i):
        self.patterns = ['$']*10
        self.vis = set()
        self.dfs(i, 0)
        patToDig = self.setCharDigits()
        outputDigits = 0
        for word in self.outputs[i]:
            sword = "".join(sorted(word)) # sort of the word
            outputDigits = (outputDigits*10) + patToDig[sword]
        return outputDigits

    def computeSumOutputs(self):
        return sum(self.getOutput(i) for i in range(len(self.inputs)))
            
    def setCharDigits(self):
        patToDig = dict()
        for dig, pat in enumerate(self.patterns):
            patToDig[pat] = dig
        return patToDig

    def dfs(self, index, jindex):
        """
        index: index of the inputs, it is a single line of 10 character strings
        jindex: the index of the 10 character string in the current inputs[index]
        """
        if jindex == 10:
            for i in range(10):
                for j in range(i+1, 10):
                    if len(set(self.patterns[i])&set(self.patterns[j])) != self.inCommon[i][j]:
                        return False
            return True
        word = "".join(sorted(self.inputs[index][jindex]))
        if word in self.vis:
            return False
        for digit in range(10):
            charLength = len(self.baseMap[digit])
            if charLength == len(word) and self.patterns[digit]=='$' and word not in self.vis:
                self.patterns[digit] = word
                self.vis.add(word)
                if self.dfs(index, jindex + 1):
                    return True
                self.patterns[digit] = '$'
                self.vis.remove(word)
        return False

if __name__ == "__main__":
    s = SevenSegmentSearch()
    print(s.computeSumOutputs())
```

Uses logic to solve with if statements. Using frozenset because it is immutable set that is hashable and can be a key in a dictionary in python. 

This was another way to solve.  It turned out that you can separate the 2,3,5 and 0,6,9 into 
sets that have 5 and 6 segments respectively. Then there exist relationships that would
indicate the digit.  For example if length if 5 and it has 2 segments in common with the 1 digit. 
It must be a 3.  

```py
class SevenSegmentSearch:
    def dataLoader(self, path = "inputs/input.txt"):
        with open("inputs/input.txt", "r") as f:
            loadedData = f.read().splitlines()
        for data in loadedData:
            rawPatterns, rawDigits = map(str.split, data.split('|'))
            patterns = tuple(map(lambda x: (frozenset(x), len(x)), rawPatterns))
            digits = tuple(map(lambda x: frozenset(x), rawDigits))
            yield patterns, digits

    def deduceMapping(self, patterns):
        # pattern to digit mapping
        p2d = dict()
        for p, plen in patterns:
            if plen == 2:
                p2d[p] = 1
            elif plen == 3:
                p2d[p] = 7
            elif plen == 4:
                p2d[p] = 4
            elif plen == 7:
                p2d[p] = 8
        d2p = {v: k for k, v in p2d.items()}
        for p, plen in patterns:
            # 3 or 5 or 2, all have length of 5
            if plen==5:
                if len(p & d2p[1]) == 2:
                    p2d[p] = 3
                elif len(p&d2p[4]) == 3:
                    p2d[p] = 5
                else:
                    p2d[p] = 2
            elif plen==6:
                if len(p&d2p[4])==4:
                    p2d[p] = 9
                elif len(p&d2p[7])==2:
                    p2d[p] = 6
                else:
                    p2d[p] = 0
        return p2d

    def getOutput(self):
        totalCnt = 0
        for pattern, digit in self.dataLoader():
            p2d = self.deduceMapping(pattern)
            cnt = 0
            for dig in digit:
                cnt = cnt*10 + p2d[dig]
            totalCnt += cnt
        return totalCnt
```