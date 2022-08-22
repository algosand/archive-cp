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