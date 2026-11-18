import heapq
from math import hypot
from pyamaze import maze, agent, textLabel

def manhattan(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
def euclidean(a, b): return hypot(a[0]-b[0], a[1]-b[1])

DIRS = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

def a_star(m, start, goal, heuristic=manhattan):
    g = {start: 0}
    came_from, closed, explored = {}, set(), []
    open_heap = [(heuristic(start, goal), 0, start)]

    while open_heap:
        _, cost, cell = heapq.heappop(open_heap)
        if cell in closed:
            continue
        closed.add(cell)
        explored.append(cell)

        if cell == goal:
            path = [cell]
            while cell != start:
                cell = came_from[cell]
                path.append(cell)
            return path[::-1], explored

        for d, (dr, dc) in DIRS.items():
            if m.maze_map[cell][d]:
                nxt = (cell[0] + dr, cell[1] + dc)
                ng = cost + 1
                if ng < g.get(nxt, float('inf')):
                    g[nxt] = ng
                    came_from[nxt] = cell
                    heapq.heappush(open_heap, (ng + heuristic(nxt, goal), ng, nxt))

    return None, explored   # unreachable

if __name__ == '__main__':
    m = maze(10, 10)
    m.CreateMaze()                      # goal defaults to (1,1)
    start, goal = (m.rows, m.cols), (1, 1)

    path, explored = a_star(m, start, goal, euclidean)
    if path is None:
        print("No path exists.")
    else:
        print(f"Path found: {len(path)-1} steps, {len(explored)} cells explored")
        search = agent(m, *start, color='yellow', footprints=True, filled=True)
        final = agent(m, *start, color='red', footprints=True)
        m.tracePath({search: explored}, delay=20)
        m.tracePath({final: path})
        textLabel(m, 'A* Path Length (steps)', len(path) - 1)
    m.run()
