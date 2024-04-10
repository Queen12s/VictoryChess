##search and eval too slow gonna rewrite in rust but it was fun ig?
import chess
import chess.pgn
queen_tab = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]
rook_table = [  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  -3,  2,  5,  5,  2,  -3,  0]
bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10,  0,  0,  0,  0,  0,  0, -10,
                -10,  0,  5, 10, 10,  5,  0, -10,
                -10,  5,  5, 10, 10,  5,  5, -10,
                -10,  0, 10, 10, 10, 10,  0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10,  5,  0,  0,  0,  0,  5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20]

king_middle = [-30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -20, -30, -30, -40, -40, -30, -30, -20,
               -10, -20, -20, -20, -20, -20, -20, -10,
               20, 20,  0,  -7,  -7,  0, 20, 20,
               20, 30, 10,  0,  0, 10, 30, 20]

pawn_tab = [0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            -3,  -2,  0, 20, 20,  0,  -2,  -3,
            5, -5, -10,  0,  0, -10, -4,  -2,
            5, 10, 10, -20, -20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0]

knight_tab = [-50, -40, -30, -30, -30, -30, -40, -50,
              -40, -20,  0,  0,  0,  0, -20, -40,
              -30,  0, 10, 15, 15, 10,  0, -30,
              -30,  5, 15, 20, 20, 15,  5, -30,
              -30,  0, 15, 20, 20, 15,  0, -30,
              -30,  5, 10, 15, 15, 10,  5, -30,
              -40, -20,  0,  5,  5,  0, -20, -40,
              -50, -50, -30, -30, -30, -30, -50, -50]

qv, rv, nv, bv, pv = 900, 500, 300, 320, 100

ne = chess.Board()

captures = []
best_move = None

for move in ne.legal_moves:
    if ne.is_capture(move):
        captures.append(move)
zz = 0
def ng():
    if ne.turn == chess.WHITE:
        return 1, -1
    elif ne.turn == chess.BLACK:
        return -1, 1
def eye_order():
    zz= 0
    sor = []
    ##captures -> checks -> normal moves (V0.0.1) (not exactly but im lazy)
    for mov in ne.legal_moves:
        zz +=1 
        if ne.is_capture(mov):
            if zz != 0:
                sor.insert(zz,mov)
            else:
                sor.append(mov)
        else:	
            sor.append(mov)
    return sor
    zz = 0        
def evaluate(board):
    # Material score + Mobility Score (V0.0.1)
    material_score = (
        (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK))) * pv +
        (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) * nv +
        (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) * bv +
        (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) * rv +
        (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK))) * qv
    )
    
    
    positional_score = sum(pawn_tab[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    positional_score -= sum(pawn_tab[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK))
    positional_score += sum(knight_tab[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
    positional_score -= sum(knight_tab[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK))
    positional_score += sum(bishop_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    positional_score -= sum(bishop_table[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK))
    positional_score += sum(rook_table[i] for i in board.pieces(chess.ROOK, chess.WHITE))
    positional_score -= sum(rook_table[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK))
    positional_score += sum(queen_tab[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
    positional_score -= sum(queen_tab[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK))

    # Total score
    eval_score = material_score + positional_score
    return eval_score


def quis(alpha, beta):
    if ne.is_checkmate():
        return 0
    stand_pat = evaluate(ne)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    for move in captures:
        ne.push(move)
        score = evaluate(ne)
        ne.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board), None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in eye_order():
            board.push(move)
            eval_score, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in eye_order():
            board.push(move)
            eval_score, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def evaluate_after_move(board, move):
    board.push(move)
    eval_score = evaluate(board)
    board.pop()
    return eval_score
moves = []

# Loop until the game is over
while not ne.is_game_over():
    z = input()
    ne.push_san(z) ## throw error if san is not valid.
    if ne.turn == chess.WHITE:
        # White's turn to move
        score, best_move = alpha_beta(ne, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
    else:
        # Black's turn to move
        score, best_move = alpha_beta(ne, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)

    # Make the best move found by the search function
    ne.push(best_move)
    print(best_move)

    # Append the move to the moves list
    moves.append(best_move)

    # Print the board after the move
    print(ne)
    print(evaluate(ne))

# Create a new game
game = chess.pgn.Game()

# Add moves to the game
node = game.add_variation(moves[0])
for move in moves[1:]:
    node = node.add_variation(move)

# Print the PGN of the game
print("PGN of the game:")
print(game)
