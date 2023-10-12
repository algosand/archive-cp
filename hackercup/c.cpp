#include <bits/stdc++.h>
using namespace std;
#define int long long
#define x first
#define y second

inline int read() {
	int x = 0, y = 1; char c = getchar();
	while (c < '0' || c > '9') {
		if (c == '-') y = -1;
		c = getchar();
	}
	while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
	return x * y;
}

string name = "replay_value_input.txt";

const int mod = 1e9 + 7;
vector<int> y_values;
vector<pair<int, int>> lasers;
int dp[2][52][52][52][52];

void solve() {
    int N = read(), S = read(), E = read();
    lasers.clear();
    y_values.assign(N, 0);
    for (int i = 0; i < N; i++) {
        int x = read(), y = read();
        lasers.push_back({x, y});
        y_values[i] = y;
    }
    y_values.push_back(S);
    y_values.push_back(E);
    // y value coordinate compression
    sort(y_values.begin(), y_values.end());
    S = lower_bound(y_values.begin(), y_values.end(), S) - y_values.begin();
    E = lower_bound(y_values.begin(), y_values.end(), E) - y_values.begin();
    for (int i = 0; i < N; i++) {
        lasers[i].y = lower_bound(y_values.begin(), y_values.end(), lasers[i].y) - y_values.begin();
    }
    // flip all the y coordinates if values of E > S
    if (E > S) {
        for (int i = 0; i < N; i++) {
            lasers[i].y = N + 1 - lasers[i].y;
        }
        S = N + 1 - S;
        E = N + 1 - E;
    }
    // sort the lasers by x coordinate
    sort(lasers.begin(), lasers.end());
    int x = 0;
    memset(dp[x], 0, sizeof(dp[x]));
    dp[x][N + 1][0][N + 1][0] = 1;
    for (int i = 0; i < N; i++) {
        x ^= 1;
        memset(dp[x], 0, sizeof(dp[x]));
        // set region of current laser's y value
        int region = 0;
        int y = lasers[i].y;
        if (y > S) region = 1;
        else if (y > E) region = 2;
        else region = 3;
        for (int a = 0; a < N + 2; a++) {
            for (int b = 0; b < N + 2; b++) {
                for (int c = 0; c < N + 2; c++) {
                    for (int d = 0; d < N + 2; d++) {
                        int v = dp[x ^ 1][a][b][c][d];
                        if (v == 0) continue;
                        // right
                        if (region == 3) {
                            dp[x][a][b][c][max(d, y)] += v;
                            dp[x][a][b][c][max(d, y)] %= mod;
                        } else {
                            dp[x][a][b][min(c, y)][d] += v;
                            dp[x][a][b][min(c, y)][d] %= mod;
                        }
                        // up
                        if (y >= d) {
                            dp[x][min(a, y)][b][c][d] += v;
                            dp[x][min(a, y)][b][c][d] %= mod;
                        }
                        // left
                        if ((region == 1 && y >= b) || (region != 1 && y <= a)) {
                            dp[x][a][b][c][d] += v;
                            dp[x][a][b][c][d] %= mod;
                        }
                        // down
                        if (y <= c) {
                            dp[x][a][max(b, y)][c][d] += v;
                            dp[x][a][max(b, y)][c][d] %= mod;
                        }
                    }
                }
            }
        }
    }
    int num_configs = 0;
    for (int a = 0; a < N + 2; a++) {
        for (int b = 0; b < N + 2; b++) {
            for (int c = 0; c < N + 2; c++) {
                for (int d = 0; d < N + 2; d++) {
                    num_configs += dp[x][a][b][c][d];
                    num_configs %= mod;
                }
            }
        }
    }
    int res = 1;
    for (int i = 0; i < N; i++) {
        res *= 4;
        res %= mod;
    }
    res = (res - num_configs + mod) % mod;
    cout << res;
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
        cout << "Case #" << i << ": ";
        solve();
        cout << endl;
    }
    return 0;
}

/*
problem solve

g++ "-Wl,--stack,1078749825" c.cpp -o main
*/