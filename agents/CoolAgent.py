from collections import deque
from move import Move
# BFS para ter o

class CoolAgent:

    def __init__(self, maze, prize_positions, agent_position, opponent_position, max_turns):
        self.rows    = len(maze)
        self.cols    = len(maze[0])
        self.my_pos  = agent_position
        self.opp_pos = opponent_position
        self.values  = {}
        self.paths   = {}
        self.dists   = {}

    def next_move(self, maze, prize_positions, agent_position, opponent_position):
        self.my_pos  = agent_position
        self.opp_pos = opponent_position
        self.maze    = maze
        self.values  = {pos: val for pos, val in prize_positions.items()}

        if not self.values:
            return Move.STAY

        self._bfs(self.my_pos,  full_path=True)
        self._bfs(self.opp_pos, full_path=False)

        return self._pick()

    def _bfs(self, start, full_path):
        targets = set(self.values)
        visited = {start: None}
        queue   = deque([start])
        found   = 0
        while queue and found < len(targets):
            pos = queue.popleft()
            if pos in targets:
                found += 1
                if full_path:
                    self.paths[pos] = self._reconstruct(visited, pos)
                else:
                    self.dists[pos] = self._depth(visited, pos)
            for nb in self._neighbors(pos):
                if nb not in visited:
                    visited[nb] = pos
                    queue.append(nb)

    def _neighbors(self, pos):
        r, c = pos
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc] != '#':
                yield (nr, nc)

    # reconstruct the shortest path
    def _reconstruct(self, visited, end):
        path, cur = [], end
        while visited[cur] is not None:
            path.append(cur)
            cur = visited[cur]
        return list(reversed(path))

    def _depth(self, visited, end):
        depth, cur = 0, end
        while visited[cur] is not None:
            depth += 1
            cur = visited[cur]
        return depth

    def _pick(self):
        best_pos, best_score = None, -1
        for pos, val in self.values.items():
            if pos not in self.paths:
                continue
            my_dist  = len(self.paths[pos])
            opp_dist = self.dists.get(pos, 999)
            if my_dist == 0:
                return Move.STAY
            score = val / my_dist if opp_dist > my_dist else 0
            if score > best_score:
                best_score, best_pos = score, pos

        if best_pos is None:
            return Move.STAY

        next_pos = self.paths[best_pos][0]
        return self._to_move(next_pos)

    def _to_move(self, next_pos):
        r, c   = self.my_pos
        nr, nc = next_pos
        if nr == r - 1: return Move.UP
        if nr == r + 1: return Move.DOWN
        if nc == c - 1: return Move.LEFT
        if nc == c + 1: return Move.RIGHT
        return Move.STAY