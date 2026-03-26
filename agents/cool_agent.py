from collections import deque
from move import Move


class CoolAgent:

    def __init__(self, maze, prize_positions, agent_position, opponent_position, max_turns):
        self.rows = len(maze)
        self.cols = len(maze[0])

    def _debug(self, poi, target, opp_dists):
        print(f"\n--- turn | my_pos={self.my_pos} opp_pos={self.opp_pos} ---")
        for pos, (val, path) in sorted(poi.items(), key=lambda x: len(x[1][1])):
            my_dist = len(path)
            opp_dist = opp_dists.get(pos, 999)
            flag = " <-- target" if pos == target else ""
            print(f"  {pos} val={val} my={my_dist} opp={opp_dist}{flag}")

    def next_move(self, maze, prize_positions, agent_position, opponent_position):
        self.maze    = maze
        self.my_pos  = agent_position
        self.opp_pos = opponent_position

        # Se não existirem poi, ele não move
        if not prize_positions:
            return Move.STAY

        poi    = self._get_poi(prize_positions)
        best   = self._compare(poi)
        return self._move(poi, best)

    # --- 1. retrieval ---

    def _get_poi(self, prize_positions):

        targets = set(prize_positions)
        visited = {self.my_pos: None}
        queue   = deque([self.my_pos])
        poi     = {}

        while queue and len(poi) < len(targets):
            pos = queue.popleft()
            if pos in targets:
                poi[pos] = (prize_positions[pos], self._reconstruct(visited, pos))
            for nb in self._neighbors(pos):
                if nb not in visited:
                    visited[nb] = pos
                    queue.append(nb)

        return poi


    def _reconstruct(self, visited, end):
        path, cur = [], end
        while visited[cur] is not None:
            path.append(cur)
            cur = visited[cur]
        return list(reversed(path))

    def _neighbors(self, pos):
        r, c = pos
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc] != '#':
                yield (nr, nc)

    # --- 2. comparison ---

    def _compare(self, poi):
        opp_dists            = self._bfs_opp(set(poi))
        best_pos, best_score = None, -1

        for pos, (val, path) in poi.items():
            my_dist  = len(path)
            opp_dist = opp_dists.get(pos, 999)
            if my_dist == 0:
                return pos
            score = val / my_dist if opp_dist > my_dist else 0
            if score > best_score:
                best_score, best_pos = score, pos
        self._debug(poi, best_pos, opp_dists)
        return best_pos

    def _bfs_opp(self, targets):
        visited = {self.opp_pos: 0}
        queue   = deque([self.opp_pos])
        dists   = {}

        while queue and len(dists) < len(targets):
            pos = queue.popleft()
            if pos in targets:
                dists[pos] = visited[pos]
            for nb in self._neighbors(pos):
                if nb not in visited:
                    visited[nb] = visited[pos] + 1
                    queue.append(nb)

        return dists

    # --- 3. movement ---

    def _move(self, poi, target):
        if target is None:
            return Move.STAY

        _, path = poi[target]
        if not path:
            return Move.STAY

        r,  c  = self.my_pos
        nr, nc = path[0]
        if nr == r - 1: return Move.UP
        if nr == r + 1: return Move.DOWN
        if nc == c - 1: return Move.LEFT
        if nc == c + 1: return Move.RIGHT
        return Move.STAY