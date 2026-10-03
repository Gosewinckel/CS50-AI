"""
Tic Tac Toe Player
"""

import math
import copy
from collections import deque

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    for row in board:
        for val in row:
            if  val== X:
                x += 1
            elif val == O:
                o += 1
    if x <= o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    valid_actions = set()
    for x, _ in enumerate(board):
        for y, value in enumerate(board[x]):
            if value == EMPTY:
                valid_actions.add((x,y))
    return valid_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2:
        raise ValueError
    if action[1] < 0 or action[1] > 2:
        raise ValueError
    x = action[0]
    y = action[1]
    if len(action) != 2:
        raise ValueError
    if board[x][y] != EMPTY:
        raise ValueError
    board_copy = copy.deepcopy(board)
    current_player = player(board_copy)
    board_copy[x][y] = current_player
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[2][0]
    for x in range(0, 3):
        if board[x][0] != EMPTY:
            if board[x][0] == board[x][1] and board[x][1] == board[x][2]:
                return board[x][1]
    for y in range(0, 3):
        if board[0][y] != EMPTY:
            if board[0][y] == board[1][y] and board[1][y] == board[2][y]:
                return board[0][y]
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for x, _ in enumerate(board):
        for _, value in enumerate(board[x]):
            if value == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    if victor == X:
        return 1
    if victor == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    current_player = player(board)
    winning_score = 0
    possible_moves = actions(board)
    winning_position = (0, 0)
    for move in possible_moves:
        new_board = result(board, move)
        board_score = score_search(new_board)
        if current_player == X:
            if board_score == 1:
                return move
            if board_score >= winning_score:
                winning_score = board_score
                winning_position = move
        if current_player == O:
            if board_score == -1:
                return move
            if board_score <= winning_score:
                winning_score = board_score
                winning_position = move
    return winning_position

def score_search(board):
    if terminal(board):
        return utility(board)
    possible_moves = actions(board)
    current_player = player(board)
    best_score = 0
    if current_player == X:
        best_score = -2
    else:
        best_score = 2
    for move in possible_moves:
        new_board = result(board, move)
        path_result = score_search(new_board)
        if current_player == X:
            if path_result > best_score:
                if path_result == 1:
                    return 1
                best_score = path_result
        if current_player == O:
            if path_result < best_score:
                if path_result == -1:
                    return -1
                best_score = path_result
    return best_score
