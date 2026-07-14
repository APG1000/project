import time
from typing import Optional, Tuple

import chess

from evaluation import evaluate_position
from utils import format_move, is_time_up

INF = 10**9
MATE_SCORE = 10**6


class ChessEngine:
    def __init__(self, max_depth: int = 4, time_limit: Optional[float] = None) -> None:
        self.max_depth = max_depth
        self.time_limit = time_limit

    def select_move(
        self,
        board: chess.Board,
        max_depth: Optional[int] = None,
        time_limit: Optional[float] = None,
    ) -> Optional[chess.Move]:
        if board.is_game_over():
            return None

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        search_depth = self.max_depth if max_depth is None else max_depth
        search_depth = max(1, search_depth)
        time_limit = self.time_limit if time_limit is None else time_limit
        start_time = time.perf_counter() if time_limit is not None else None

        best_move = legal_moves[0]
        best_score = -INF

        for depth in range(1, search_depth + 1):
            if time_limit is not None and is_time_up(start_time, time_limit):
                break

            try:
                score, move = self._search_root(board, depth, start_time, time_limit)
            except TimeoutError:
                break

            if move is not None:
                best_move = move
                best_score = score

            if abs(best_score) >= MATE_SCORE - depth:
                break

        return best_move

    def _search_root(
        self,
        board: chess.Board,
        depth: int,
        start_time: Optional[float],
        time_limit: Optional[float],
    ) -> Tuple[int, Optional[chess.Move]]:
        alpha = -INF
        beta = INF
        ordered_moves = self._order_moves(board, list(board.legal_moves))
        if not ordered_moves:
            return 0, None

        best_score = -INF
        best_move = ordered_moves[0]

        for move in ordered_moves:
            if time_limit is not None and is_time_up(start_time, time_limit):
                raise TimeoutError

            board.push(move)
            score = -self._negamax(board, depth - 1, -beta, -alpha, 1, start_time, time_limit)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best_score, best_move

    def _negamax(
        self,
        board: chess.Board,
        depth: int,
        alpha: int,
        beta: int,
        ply: int,
        start_time: Optional[float],
        time_limit: Optional[float],
    ) -> int:
        if time_limit is not None and is_time_up(start_time, time_limit):
            raise TimeoutError

        if board.is_checkmate():
            return -MATE_SCORE + ply
        if board.is_stalemate():
            return 0
        if depth == 0:
            return evaluate_position(board)

        best_value = -INF
        for move in self._order_moves(board, list(board.legal_moves)):
            board.push(move)
            value = -self._negamax(board, depth - 1, -beta, -alpha, ply + 1, start_time, time_limit)
            board.pop()

            best_value = max(best_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_value

    def _order_moves(self, board: chess.Board, moves: list[chess.Move]) -> list[chess.Move]:
        def move_sort_key(move: chess.Move) -> tuple[int, int, int]:
            captured_piece = board.piece_at(move.to_square)
            if captured_piece is not None:
                return (0, -captured_piece.piece_type, move.to_square)
            return (1, 0, move.to_square)

        return sorted(moves, key=move_sort_key)


if __name__ == "__main__":
    engine = ChessEngine(max_depth=2)
    board = chess.Board()
    print(format_move(engine.select_move(board)))
