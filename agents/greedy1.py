from move import Move


class Groupgreedy1:

    def __init__(self, maze, prize_positions, agent_position, opponent_position, max_turns):
        """
        Called once at the start of the game.
        Use this method to initialize your agent and perform any pre-computation.

        Parameters:
            maze             : tuple[str, ...] - the maze layout as a tuple of strings.
                               Each string is a row, indexed from top (row 0) to bottom.
                               Each character is a column, indexed from left (col 0) to right.
                               Cell symbols:
                                   '#' - wall (impassable)
                                   '.' - free corridor
                                   '1'-'9', 'A'-'F' - prize with value 1-15
                                   'X' - Player 1 starting position
                                   'Y' - Player 2 starting position

            prize_positions  : dict[(int, int), int] - dictionary mapping (row, col) to prize value.
                               Example: {(1, 3): 4, (2, 7): 10, (5, 2): 4}
                               Prizes already collected are removed from this dictionary.

            agent_position   : (int, int) - your agent's current position as (row, col).
                               At the start of the game this corresponds to your initial position.

            opponent_position: (int, int) - opponent's current position as (row, col).

            max_turns        : int - maximum total number of turns in the game
                               (sum of both agents' turns).
        """
        pass

    def _manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _find_nearest_prize(self, prize_positions, agent_position):
        """Find the nearest prize using Manhattan distance."""
        if not prize_positions:
            return None
        return min(prize_positions.keys(), 
                   key=lambda p: self._manhattan_distance(agent_position, p))

    def next_move(self, maze, prize_positions, agent_position, opponent_position):
        """
        Called once per turn. Must return one of the five Move enum values.

        Parameters:
            maze             : tuple[str, ...] - current maze state (collected prizes
                               appear as free corridors '.').

            prize_positions  : dict[(int, int), int] - prizes still available on the maze.

            agent_position   : (int, int) - your agent's current position as (row, col).

            opponent_position: (int, int) - opponent's current position as (row, col).

        Returns:
            Move - one of: Move.UP, Move.DOWN, Move.RIGHT, Move.LEFT, Move.STAY

        Notes:
            - Move.UP    decreases the row index by 1.
            - Move.DOWN  increases the row index by 1.
            - Move.RIGHT increases the column index by 1.
            - Move.LEFT  decreases the column index by 1.
            - Moving into a wall is invalid and treated as Move.STAY.
            - Returning None or an invalid value is treated as Move.STAY.
            - Two agents may occupy the same cell simultaneously (no penalty).
            - You may use instance attributes (self.*) to store state between calls.
        """
        if not prize_positions:
            return Move.STAY
    
        target = self._find_nearest_prize(prize_positions, agent_position)
        row, col = agent_position
        target_row, target_col = target
    
        if target_row < row:
            return Move.UP
        elif target_row > row:
            return Move.DOWN
        elif target_col < col:
            return Move.LEFT
        elif target_col > col:
            return Move.RIGHT
        return Move.STAY