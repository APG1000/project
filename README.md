# Project-CS50: Chess Engine
### Video Demo URL: [https://youtu.be/yhS6Foxp9yo](https://youtu.be/yhS6Foxp9yo)

### Description:

The goal of this program is a chess engine, built on top of python-chess as the interface, calculating the best possible moves and playing against the user.

### The final project consists of four files. (main.py, evaluation.py, engine.py, utils.py)

## Main.py:

Handles the python-chess interface. After running this program the user is asked if he wants to play as white or black (W/B). This results in you starting the game as the selected color. The game is played through a changing board of chess pieces built as bitboards by python-chess. A valid move can be input either through normal documentation "SAN" (e4) or "UCI" format (e2e4). After inputting a move the program calcuates a score of the position and tries to find the best continuation for the opponent. After calculating it plays the move, prompting the user to play the next move and so for until either one of the sides has won or the game has ended in a stalemate.

## Evaluation.py:

Handles the evaluation of the chess position. To calculate the best potential move the engine needs some metric to quantify how good a move is. This is being done through a score variable. The score of a position depends on multiple factors:
Piece values (a pawn is worth 100, knight is worth 300 score etc.)
Square bonus (a knight on a more central square gives more score than one in the corners)
King safety (if there are pawns or bishops in front of the king this increases score)
Pawn structure (isolated pawns or double pawns reduce score)
Implementation of piece activity was planned, but was very difficult to implement. This would have included pieces not gaining points purely through squares but through their potential free moves. (e.g an open rook file is more important than the rook being on a specific field)  

## Engine.py:

Handles the whole move selection based on the evaluation score. Moves are selected based on score, however there are a vast amount of techniques to improve the speed of the engine. 

Moves are only considered if they are valid. Then for all possible valid moves a decision tree is being created based on a certain depth of calculations. The function is called recursively for depth - 1, until a depth of 0 has been reached. This position is then scored and noted down as the best possible case so far. This is done for all possibilities, however to improve speed, the decision tree is pruned through negamaxing, for worse results than the best other outcome. This is done through two parameters alpha and beta, which are set to +infinity and -infinity at first and then to the best case scenario afterwards. 

To illustrate this better: If depth is 2 and there are two different moves to consider for player1 (AB) and player2 (AB), there are 4 possibile solutions. The engine solves the score of the first (AA) and second choice (AB) (+2, +3), player2 would thus choose the route with +2 (minimizing our solution), if (BA) as the third option returns -2, there is no need to calculate (BB) saving us time, as player1 would choose AA regardless as BA is worse than AA. Furthermore, valid moves are ordered based on captures and silent moves, as captures tend to be better on average, improving speed through a higher chance of pruning. 

As chess engines have been around for a long time there are numerous other optimizations and possible improvements, however not all can be implemented due to limitations. Some common techniques not used for this project are opening books (for the engine to handle openings faster and more accurately) and an endgame tablebase. (improving speed for endings with less pieces than 8, as these have been solved fully)

## Utils.py:

Handles the time functions. Checks if the calculation time of the engine has already run out or if it can still calculate further before being stopped out of it. This is needed, as the engine usually has a time_limit.



