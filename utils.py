import time
from typing import Optional

import chess


def is_time_up(start_time: Optional[float], time_limit: Optional[float]) -> bool:
    if start_time is None or time_limit is None:
        return False
    return (time.perf_counter() - start_time) >= time_limit


def format_move(move: Optional[chess.Move]) -> str:
    return move.uci() if move is not None else "None"

