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
        5, 5, 10, 30, 30, 10, 5, 5,
        0, 0, 0, 30, 30, 0, 0, 0,
        5, 5, 5, 5, 5, 5, 5, 5,
        10, 10, 10, -20, -20, 10, 10, 10,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],

    # advantage if more to center, punish near the edges
    chess.KNIGHT: [
        -50, -10, -30, -30, -30, -30, -10, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 0, 5, 10, 10, 5, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 5, 10, 10, 5, 0, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -10, -30, -30, -30, -30, -10, -50,
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
        -20, -10, -10, 0, 0, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 5, 5, 5, 0, 0,
        0, 0, 5, 5, 5, 5, 0, 0,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, 0, 0, -10, -10, -20,
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
    index = (63 - square) if piece.color == chess.WHITE else square
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

    return score if board.turn == chess.WHITE else -score


def _king_safety(board: chess.Board) -> int:
    wscore = 0
    bscore = 0
    piece_map = board.piece_map()

    for color in (chess.WHITE, chess.BLACK):
        king_square = board.king(color)
        if king_square is None:
            continue

        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        home_rank = 0 if color == chess.WHITE else 7
        if king_rank == home_rank:
            if color == chess.WHITE:
                wscore += 10
            else:
                bscore -= 10

        forward_rank = king_rank + (1 if color == chess.WHITE else -1)

        if 0 <= forward_rank <= 7:
            # check front_square for pawn or bishop
            front_square = chess.square(king_file, forward_rank)
            front_piece = piece_map.get(front_square)
            if front_piece is not None and front_piece.color == color and (front_piece.piece_type == chess.PAWN or front_piece.piece_type == chess.BISHOP):
                if color == chess.WHITE:
                    wscore += 30
                else:
                    bscore -= 30

        for neighbor_file in (king_file - 1, king_file + 1):
            if not 0 <= neighbor_file <= 7:
                continue
            if not 0 <= forward_rank <= 7:
                continue
            # check neighbor_square for pawn
            neighbor_square = chess.square(neighbor_file, forward_rank)
            neighbor_piece = piece_map.get(neighbor_square)
            if neighbor_piece is not None and neighbor_piece.color == color and neighbor_piece.piece_type == chess.PAWN:
                if color == chess.WHITE:
                    wscore += 20
                else:
                    bscore -= 20

    return wscore + bscore


def _pawn_structure(board: chess.Board) -> int:
    score = 0
    piece_map = board.piece_map()
    for color in (chess.WHITE, chess.BLACK):
        pawns = [square for square, piece in piece_map.items() if piece.color == color and piece.piece_type == chess.PAWN]
        for square in pawns:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            is_isolated = True

            for neighbor_file in (file - 1, file + 1):
                if 0 <= neighbor_file <= 7:
                    for s in pawns:
                        if chess.square_file(s) == neighbor_file:
                            is_isolated = False
                            break
            if is_isolated:
                if color == chess.WHITE:
                    score -= 20
                else:
                    score += 20

            same_file_pawns = [s for s in pawns if chess.square_file(s) == file]
            if len(same_file_pawns) > 1:
                if color == chess.WHITE:
                    score -= 30 * (len(same_file_pawns) - 1)
                else:
                    score += 30 * (len(same_file_pawns) - 1)
    return score
