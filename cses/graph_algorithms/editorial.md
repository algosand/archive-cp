# Graph Algorithms

## Building Teams

### Solution: Check graph is bipartite with 2 colors

```c++
vector<int> colors;
vector<vector<int>> graph;
const string IMP = "IMPOSSIBLE";
bool isBipartite(int n) {
    queue<int> q;
    for (int u = 1;u<=n;u++) {
        if (colors[u]==-1) {
            colors[u]=0;
            q.push(u);
            while (!q.empty()) {
                int v = q.front();
                q.pop();
                for (int w : graph[v]) {
                    if (colors[w]==-1) {
                        colors[w] = colors[v]^1;
                        q.push(w);
                    } else {
                        if (colors[w]==colors[v]) {
                            return false;
                        }
                    }
                }
            }
        }
    }
    return true;
}
int main() {
    int n, m, a, b;
    cin >> n >> m;
    graph.resize(n+1);
    for (int i = 0;i<m;i++) {
        cin>>a>>b;
        graph[a].push_back(b);
        graph[b].push_back(a);
    }
    colors.assign(n+1,-1);
    if (isBipartite(n)) {
        for (int i = 1;i<=n;i++) {
            cout << colors[i]+1 << " ";
        }
        cout<<endl;
    } else {
        cout << IMP << endl;
    }

}
```

## School Dance

### Solution: Maximum Bipartite Matching with Kuhn's algorithm
O(nm) time 

```c++
vector<bool> visited;
vector<int> match;
vector<vector<int>> graph;
bool dfs(int u) {
    if (visited[u]) return false;
    visited[u] = true;
    for (int& v : graph[u]) {
        if (match[v] == -1 || dfs(match[v])) {
            match[v] = u;
            return true;
        }
    }
    return false;
}
int main() {
    int n, m, k, boy, girl;
    } directed graph from boy nodes to girl nodes
    for (int i = 0;i<k;i++) {
        cin>>boy>>girl;
        graph[boy].push_back(girl);
    }
    match.assign(m+1,-1);
    for (int u=1;u<=n;u++) {
        visited.assign(n+1, false);
        dfs(u);
    }
    int cnt = accumulate(match.begin(), match.end(), 0, [](const auto& a, const auto& b) {
        return a + (b!=-1);
    });
    cout<<cnt<<endl;
    for (int i = 1;i<=m;i++) {
        if (match[i]!=-1) {
            printf("%d %d\n", match[i], i);
        }
    }
}
```