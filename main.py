import chess

from engine import ChessEngine
from evaluation import evaluate_position
from utils import format_move


def main() -> None:
    board = chess.Board()
    engine = ChessEngine(max_depth=3)

    print("Chess engine ready. Enter moves in SAN or UCI format, or type 'quit'.")
    print(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move_input = input("Your move: ").strip()
            if move_input.lower() in {"quit", "exit"}:
                break
            try:
                move = board.push_san(move_input)
            except ValueError:
                try:
                    move = chess.Move.from_uci(move_input)
                    if move not in board.legal_moves:
                        raise ValueError
                    board.push(move)
                except ValueError:
                    print("Illegal move. Try again.")
                    continue
        else:
            move = engine.select_move(board)
            if move is None:
                break
            board.push(move)
            print(f"Engine plays {move.uci()}")

        print(board)
        print(f"Evaluation: {evaluate_position(board)}")

    if board.is_checkmate():
        print(f"Checkmate! Winner: {'White' if board.turn == chess.BLACK else 'Black'}")
    elif board.is_stalemate():
        print("Stalemate!")


if __name__ == "__main__":
    main()