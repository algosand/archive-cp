# String Algorithms

## String Matching

1. Z algorithm
1. KMP algorithm

### Solution 2:  KMP Algorithm + longest common prefix

```py
def main():
    text = input()
    pat = input()
    n, m = len(text), len(pat)
    def lcp(s):
        dp = [0] * m
        j = 0
        for i in range(1, m):
            if s[i] == s[j]:
                j += 1
                dp[i] = j
                continue
            while j > 0 and s[i] != s[j]:
                j -= 1
            dp[i] = j
        return dp
    def kmp(text, pat):
        j = cnt = 0
        for i in range(n):
            while j > 0 and text[i] != pat[j]:
                j = lcp_arr[j - 1]
            if text[i] == pat[j]:
                j += 1
            if j == m:
                cnt += 1
                j = lcp_arr[j - 1]
        return cnt
    lcp_arr = lcp(pat)
    res = kmp(text, pat)
    print(res)

if __name__ == '__main__':
    main()
```

## Minimal Rotation

### Solution 1:  tournament algorithm + dual elimination + O(nlogn) time complexity

```cpp
string min_string_rotation(string& s) {
    char min_char = *min_element(s.begin(), s.end());
    deque<int> champions;
    int n = s.size();
    for (int i = 0;i<n;i++) {
        if (s[i] == min_char) {
            champions.push_back(i);
        }
    }
    while (champions.size() > 1) {
        int champion1 = champions.front();
        champions.pop_front();
        int champion2 = champions.front();
        champions.pop_front();
        if (champion2 < champion1) swap(champion1, champion2);
        int current_champion = champion1;
        for (int left = champion1, right = champion2, sz = champion2-champion1; sz > 0; sz--, left++, right++) {
            if (left == n) left = 0;
            if (right == n) right = 0;
            if (s[left] < s[right]) break;
            if (s[left] > s[right]) {
                current_champion = champion2;
                break;
            }
        }
        champions.push_back(current_champion);
    }
    int champion_index = champions.front();
    return s.substr(champion_index) + s.substr(0, champion_index);
}

int main() {
    ios_base::sync_with_stdio(false);
	cin.tie(NULL);
    string s;
    cin>>s;
    cout<<min_string_rotation(s)<<endl;
}
```

## Longest Palindrome

### Solution 1:  Manacher's algorithm

This gives TLE on 4 testcases in cses, so while it should work, it is too slow for cses

```py
def main():
    neutral = '#'
    s = '$' + input()
    arr = []
    for ch in s:
        arr.extend([ch, neutral])
    arr.append('^')
    n = len(arr)
    p = [0]*n
    left = right = 1
    max_length = start = end = 0
    for i in range(1,n-1):
        p[i] = max(0, min(right-i, p[left + (right - i)]))
        while arr[i-p[i]] == arr[i+p[i]]:
            p[i] += 1
        if i+p[i] > right:
            left, right = i-p[i], i+p[i]
        if p[i] > max_length:
            start, end = left+1, right
            max_length = p[i]
    return ''.join(filter(lambda x: x!=neutral, arr[start:end]))
if __name__ == '__main__':
    print(main())
```

This solutions passes very quickly online

```cpp
#include <bits/stdc++.h>
using namespace std;
const char neutral = '#';

int main() {
    string s;
    // freopen("input.txt","r",stdin);
    cin>>s;
    int n = s.size();
    // freopen("output.txt", "w", stdout);
    s = '$' + s;
    vector<char> arr(2*n+3);
    for (int i = 0;i<=n;i++) {
        arr[2*i] = s[i];
        arr[2*i+1] = neutral;
    }
    arr.end()[-1] = '^';
    vector<int> p(2*n+1);
    int left = 1, right = 1, max_length = 0, start = 0, end = 0;
    for (int i = 1;i<=2*n;i++) {
        p[i] = max(0, min(right-i, p[left+(right-i)]));
        while (arr[i-p[i]] == arr[i+p[i]]) {
            p[i]++;
        }
        if (i+p[i] > right) {
            left = i-p[i], right = i+p[i];
        }
        if (p[i] > max_length) {
            start = left+1, end = right;
            max_length = p[i];
        }
    }
    string longest_palindrome = "";
    for (int i = start;i<end;i++) {
        if (arr[i]==neutral) continue;
        longest_palindrome += arr[i];
    }
    cout<<longest_palindrome<<endl;
}
```