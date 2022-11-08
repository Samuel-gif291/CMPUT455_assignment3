"""
simulation_util.py

Utility functions shared by simulation-based players Go3 and Go4

"""

from gtp_connection import point_to_coord, format_point
from board_base import GO_POINT, PASS
from board import GoBoard

import numpy as np
import sys
from typing import List, Tuple

MOVE_PAIR = Tuple[str,float]

def byPercentage(pair: MOVE_PAIR) -> float:
    return pair[1]

def percentage(wins: int, numSimulations: int) -> float:
    return float(wins) / float(numSimulations)

def writeMoves(board: GoBoard, moves: List[GO_POINT], count: List[int], numSimulations: int) -> None:
    """
    Write simulation results for each move.
    """
    gtp_moves = []
    for i in range(len(moves)):
        move_string = "Pass"
        if moves[i] != PASS:
            x, y = point_to_coord(moves[i], board.size)
            move_string = format_point((x, y))
        gtp_moves.append((move_string, 
                          percentage(count[i], numSimulations)))
    sys.stderr.write("win rates: {}\n".format(sorted(gtp_moves,
                     key = byPercentage, reverse = True)))
    sys.stderr.flush()

def select_best_move(board: GoBoard, moves: List[GO_POINT], moveWins: List[int]) -> GO_POINT:
    """
    Move select after the search.
    """
    max_child: int = np.argmax(moveWins)
    return moves[max_child]
