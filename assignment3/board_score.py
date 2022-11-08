"""
board_score.py
Implements functions to:
- compute the final score on a Go board
- determine the winner.
"""

import numpy as np
from board_base import where1d, BORDER, BLACK, EMPTY, WHITE
from board_base import GO_COLOR, GO_POINT, PASS, NO_POINT
from board import GoBoard

def score_board(board: GoBoard, komi: float) -> float:
    """ Score board from Black's point of view """
    score: float = -komi
    counted: np.ndarray[np.bool_] = np.full(board.maxpoint, False, dtype=np.bool_)
    for pt in range(board.maxpoint):
        point: GO_POINT = GO_POINT(pt)
        color: GO_COLOR = board.get_color(point)
        if color == BORDER or counted[point]:
            continue
        if color == BLACK:
            score += 1
        elif color == WHITE:
            score -= 1
        else:
            black_flag = False
            white_flag = False
            empty_points = where1d(board.connected_component(point))
            for p_int in empty_points:
                p: GO_POINT = GO_POINT(p_int)
                counted[p] = True 
                # TODO faster to boolean-or the whole array
                if board.find_neighbor_of_color(p, BLACK) != NO_POINT:
                    black_flag = True
                if board.find_neighbor_of_color(p, WHITE) != NO_POINT:
                    white_flag = True
                if black_flag and white_flag:
                    break
            if black_flag and not white_flag:
                score += len(empty_points)
            if white_flag and not black_flag:
                score -= len(empty_points)
    return score

def winner(board: GoBoard, komi: float) -> GO_COLOR:
    score: float = score_board(board, komi)
    if score > 0:
        return BLACK
    elif score < 0:
        return WHITE
    else:
        return EMPTY
