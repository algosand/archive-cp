# Custom Comparators


## Priority Queue

```cpp
struct priorityComp {
    // returns true mean it comes before in weak ordering, but means it comes after in priority queue.
    // So return false means it comes before in priority queue.
    bool operator()(const pair<int, int>& a, const pair<int, int>& b) const {
        if (a.first != b.first) return a.first > b.first;
        return a.second < b.second;
    }
};
```

## Vector 

sorting edges containing object Edge in descending order of w variable

```cpp
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w > b.w; // Descending order
    })
```
