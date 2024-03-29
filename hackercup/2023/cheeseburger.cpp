#include <bits/stdc++.h>
using namespace std;
#define int long long

inline int read() {
	int x = 0, y = 1; char c = getchar();
	while (c < '0' || c > '9') {
		if (c == '-') y = -1;
		c = getchar();
	}
	while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
	return x * y;
}

// string name = "cheeseburger_corollary_2_sample_input.txt";
// string name = "cheeseburger_corollary_2_validation_input.txt";
string name = "cheeseburger_corollary_2_input.txt";


void solve(int t) {
    int A = read(), B = read(), C = read();
    int res = 0LL;
    res = max(res, C / A);
    res = max(res, 2 * (C / B) - 1);
    if (C >= A) {
        res = max(res, 2 * ((C - A) / B) + 1);
    }
    if (C >= 2 * A) {
        res = max(res, 2 * ((C - 2 * A) / B) + 2);
    }
    cout << "Case #" << t << ": " << res << endl;
}

int32_t main() {
	ios_base::sync_with_stdio(0);
    cin.tie(NULL);
    string in = "inputs/" + name;
    string out = "outputs/" + name;
    freopen(in.c_str(), "r", stdin);
    freopen(out.c_str(), "w", stdout);
    int T = read();
    for (int i = 1; i <= T ; i++) {
        solve(i);
    }
    return 0;
}
