from flask import Flask, render_template, jsonify
import time

app = Flask(__name__,template_folder="")

graph = {
    0: [1, 2],
    1: [3, 4],
    2: [5, 6],
    3: [7, 8],
    4: [9],
    5: [10],
    6: [11],
    8: [12],
    9: [13],
    10: [14]
}

# Functions to handle BFS and DFS traversal
def bfs_traverse(start):
    visited_bfs = []
    queue = [start]
    visited = set()

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            visited_bfs.append(node)
            queue.extend(graph.get(node, []))
            time.sleep(0.1)  # Simulate delay for visualization
    return visited_bfs

def dfs_traverse(start):
    visited_dfs = []
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            visited_dfs.append(node)
            stack.extend(graph.get(node, []))
            time.sleep(0.1)  # Simulate delay for visualization
    return visited_dfs


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bfs')
def bfs():
    result = bfs_traverse(0)
    return jsonify(result)


@app.route('/dfs')
def dfs():
    result = dfs_traverse(0)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
