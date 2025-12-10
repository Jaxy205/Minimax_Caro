"""
ai.py - AIEngine sử dụng Minimax với Alpha-Beta Pruning.
"""

from typing import Optional
from consts import (
    BOARD_SIZE, WIN_CONDITION, EMPTY, HUMAN, AI,
    AI_DEPTH, NEIGHBOR_RADIUS, DIRECTIONS,
    SCORE_FIVE, SCORE_OPEN_FOUR, SCORE_CLOSED_FOUR,
    SCORE_OPEN_THREE, SCORE_CLOSED_THREE,
    SCORE_OPEN_TWO, SCORE_CLOSED_TWO, SCORE_ONE,
    DEFENSE_MULTIPLIER
)
from board import Board


class AIEngine:
    __slots__ = ('_depth', '_board')
    
    def __init__(self, depth: int = AI_DEPTH) -> None:
        self._depth: int = depth
        self._board: Optional[Board] = None
    
    def get_best_move(self, board: Board) -> Optional[tuple[int, int]]:
        self._board = board
        if board.move_count == 0:
            center = BOARD_SIZE // 2
            return (center, center)
        if board.move_count == 1:
            return self._get_adjacent_to_opponent()
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        candidate_moves = self._get_candidate_moves()
        
        for row, col in candidate_moves:
            board.make_move(row, col, AI)
            
            if board.check_winner(row, col) == AI:
                board.undo_move(row, col)
                return (row, col)
            
            score = self._minimax(self._depth - 1, False, alpha, beta, (row, col))
            board.undo_move(row, col)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
            
            alpha = max(alpha, score)
        
        return best_move
    
    def _minimax(self, depth: int, is_maximizing: bool, alpha: float, beta: float, last_move: tuple[int, int]) -> float:
        winner = self._board.check_winner(last_move[0], last_move[1])
        if winner == AI:
            return SCORE_FIVE + depth
        if winner == HUMAN:
            return -SCORE_FIVE - depth
        if self._board.is_full():
            return 0
        if depth == 0:
            return self._evaluate_board()
        
        candidate_moves = self._get_candidate_moves()
        
        if is_maximizing:
            max_score = float('-inf')
            for row, col in candidate_moves:
                self._board.make_move(row, col, AI)
                score = self._minimax(depth - 1, False, alpha, beta, (row, col))
                self._board.undo_move(row, col)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha: break
            return max_score
        else:
            min_score = float('inf')
            for row, col in candidate_moves:
                self._board.make_move(row, col, HUMAN)
                score = self._minimax(depth - 1, True, alpha, beta, (row, col))
                self._board.undo_move(row, col)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha: break
            return min_score
    
    def _get_candidate_moves(self) -> list[tuple[int, int]]:
        candidates: set[tuple[int, int]] = set()
        center = BOARD_SIZE // 2
        
        for played_row, played_col in self._board.played_cells:
            for dr in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                for dc in range(-NEIGHBOR_RADIUS, NEIGHBOR_RADIUS + 1):
                    if dr == 0 and dc == 0: continue
                    nr, nc = played_row + dr, played_col + dc
                    if self._board.is_valid_move(nr, nc):
                        candidates.add((nr, nc))
        
        return sorted(candidates, key=lambda p: abs(p[0] - center) + abs(p[1] - center))

    def _get_adjacent_to_opponent(self) -> tuple[int, int]:
        for row, col in self._board.played_cells:
            for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (1,0)]:
                nr, nc = row + dr, col + dc
                if self._board.is_valid_move(nr, nc): return (nr, nc)
        return (BOARD_SIZE//2, BOARD_SIZE//2)

    def _evaluate_board(self) -> float:
        return self._evaluate_player(AI) - self._evaluate_player(HUMAN) * DEFENSE_MULTIPLIER

    def _evaluate_player(self, player: str) -> float:
        total_score: float = 0
        evaluated = set()
        for row, col in self._board.played_cells:
            if self._board.get_cell(row, col) != player: continue
            for dr, dc in DIRECTIONS:
                if (row, col, dr, dc) in evaluated: continue
                score, cells = self._evaluate_line(row, col, dr, dc, player)
                total_score += score
                for c in cells: evaluated.add((c[0], c[1], dr, dc))
        return total_score

    def _evaluate_line(self, row, col, dr, dc, player):
        cells = [(row, col)]
        count = 1
        
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self._board.get_cell(r, c) == player:
            cells.append((r, c))
            count += 1
            r += dr
            c += dc
        open_f = (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self._board.get_cell(r, c) == EMPTY)
        
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self._board.get_cell(r, c) == player:
            cells.append((r, c))
            count += 1
            r -= dr
            c -= dc
        open_b = (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self._board.get_cell(r, c) == EMPTY)
        
        return self._get_pattern_score(count, int(open_f) + int(open_b)), cells

    def _get_pattern_score(self, count, open_ends):
        if count >= WIN_CONDITION: return SCORE_FIVE
        if open_ends == 0: return 0
        if count == 4: return SCORE_OPEN_FOUR if open_ends == 2 else SCORE_CLOSED_FOUR
        if count == 3: return SCORE_OPEN_THREE if open_ends == 2 else SCORE_CLOSED_THREE
        if count == 2: return SCORE_OPEN_TWO if open_ends == 2 else SCORE_CLOSED_TWO
        if count == 1: return SCORE_ONE if open_ends == 2 else SCORE_ONE // 2
        return 0
