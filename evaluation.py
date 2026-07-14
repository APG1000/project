import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# Piece-square tables.
PSQT = {

    # advantage if further ahead
    chess.PAWN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 5, -10, -10, 5, 5, 5,
        10, 10, 10, -20, -20, 10, 10, 10,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],

    # advantage if more to center, punish near the edges
    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],
    chess.BISHOP: [
        # no punish, more if blocked not sure how to implement that
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 10, 0, 0, 0, 0, 10, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 10, 15, 15, 10, 0, -10,
        -10, 0, 10, 15, 15, 10, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 10, 0, 0, 0, 0, 10, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],
    chess.ROOK: [
        # no punish, more if blocked by pawns not sure how to implement that
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],
    chess.QUEEN: [

        # advantage if near the enemy king?, otherwise small punish in the corners
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20,
    ],
    chess.KING: [
        # advantage if near castle position
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20,
    ],
}


def _piece_square_score(piece: chess.Piece, square: int) -> int:
    table = PSQT[piece.piece_type]
    # flip the table for black pieces since the tables are defined from white's perspective
    index = square if piece.color == chess.WHITE else 63 - square
    return table[index]


def evaluate_position(board: chess.Board) -> int:
    score = 20
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        square_bonus = _piece_square_score(piece, square)
        if piece.color == chess.WHITE:
            score += value + square_bonus
        else:
            score -= value + square_bonus

    score += _king_safety(board)
    score += _pawn_structure(board)

    return score


def _king_safety(board: chess.Board) -> int:
    score = 0
    for color in (chess.WHITE, chess.BLACK):
        king_square = board.king(color)
        if king_square is None:
            continue
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        if color == chess.WHITE:
            score += 8 - abs(king_file - 3)
            score += 2 if king_rank > 4 else 0
        else:
            score -= 8 - abs(king_file - 3)
            score -= 2 if king_rank < 4 else 0
    return score


def _pawn_structure(board: chess.Board) -> int:
    score = 0
    piece_map = board.piece_map()
    for color in (chess.WHITE, chess.BLACK):
        pawns = [square for square, piece in piece_map.items() if piece.color == color and piece.piece_type == chess.PAWN]
        for square in pawns:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            if color == chess.WHITE:
                score += 2
            else:
                score -= 2

            is_isolated = True
            for neighbor_file in (file - 1, file + 1):
                if 0 <= neighbor_file <= 7:
                    neighbor_square = chess.square(neighbor_file, rank)
                    if neighbor_square in piece_map:
                        neighbor_piece = piece_map[neighbor_square]
                        if neighbor_piece.color == color and neighbor_piece.piece_type == chess.PAWN:
                            is_isolated = False
                            break
            if is_isolated:
                if color == chess.WHITE:
                    score -= 12
                else:
                    score += 12

            same_file_pawns = [s for s in pawns if chess.square_file(s) == file]
            if len(same_file_pawns) > 1:
                if color == chess.WHITE:
                    score -= 8 * (len(same_file_pawns) - 1)
                else:
                    score += 8 * (len(same_file_pawns) - 1)
    return score


def evaluate_material(board: chess.Board) -> int:
    return sum((PIECE_VALUES[piece.piece_type] if piece.color == chess.WHITE else -PIECE_VALUES[piece.piece_type]) for piece in board.piece_map().values())
