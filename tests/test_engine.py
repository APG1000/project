import chess

from engine import ChessEngine
from evaluation import evaluate_position


def test_material_evaluation_is_white_perspective():
    board = chess.Board()
    assert evaluate_position(board) > 0


def test_engine_returns_legal_move():
    engine = ChessEngine(max_depth=2)
    board = chess.Board()
    move = engine.select_move(board)
    assert move in board.legal_moves
