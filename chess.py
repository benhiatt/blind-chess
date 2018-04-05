# -*- coding: utf-8 -*-
from copy import deepcopy
from os import system

def coords(pos):
    return ord(pos[0]) - 97, int(pos[1]) - 1

def pos(x, y):
    return chr(x + 97) + str(y + 1)

DIM = 8

def displayBoard(board, symbols):
    print '　'.join([chr(x) for x in xrange(ord('a'), ord('i'))])
    for i in xrange(DIM - 1, -1, -1):
        print ' '.join([symbols[square] for square in board[i]]), i + 1

# relative primes
symbols = {
    -11: '♔',
    -35: '♕',
    -7: '♖',
    -5: '♗',
    -3: '♘',
    -2: '♙',
    0: '▢',
    2: '♟',
    3: '♞',
    5: '♝',
    7: '♜',
    35: '♛',
    11: '♚'
}

alt_symbols = {
    -11: 'k',
    -35: 'q',
    -7: 'r',
    -5: 'b',
    -3: 'n',
    -2: 'p',
    0: '+',
    2: 'P',
    3: 'N',
    5: 'B',
    7: 'R',
    35: 'Q',
    11: 'K'
}

def getMoves(board, X, Y):
    moves = []
    piece = board[Y][X]
    if not piece:
        return moves
    turn = 1 if piece > 0 else -1
    if not piece % 2: # pawn
        # moving
        if not board[Y + turn][X]: # square directly in front is empty
            moves.append(pos(X, Y + turn))
            if Y == turn or Y == 7 + turn: # pawn hasn't moved yet
                if not board[Y + turn + turn][X]: # square two spaces in front is empty
                    moves.append(pos(X, Y + turn + turn))
        # capturing
        for deltaX in (-1, 1):
            try: # target square on board
                if turn * board[Y + turn][X + deltaX] < 0: # enemy piece on the diagonal
                    moves.append(pos(X + deltaX, Y + turn))
            except: # target square not on board
                pass
    if not piece % 3: # knight
        for deltaY in (-2, -1, 1, 2):
            for deltaX in (-2, -1, 1, 2):
                if abs(deltaY) != abs(deltaX): # knight moves in an "L" shape
                    try: # target square on board
                        if turn * board[Y + deltaY][X + deltaX] <= 0: # enemy piece or empty space at target square
                            moves.append(pos(X + deltaX, Y + deltaY))
                    except: # target square not on board
                        pass
    if not piece % 5: # bishop or 1/2 queen
        for deltaY in (-1, 1):
            for deltaX in (-1, 1):
                n = 1
                try: # target square on board
                    while not board[Y + (n * deltaY)][X + (n * deltaX)]: # empty space at target square
                        moves.append(pos(X + (n * deltaX), Y + (n * deltaY)))
                        n += 1
                    if turn * board[Y + (n * deltaY)][X + (n * deltaX)] < 0: # enemy piece at target square
                        moves.append(pos(X + (n * deltaX), Y + (n * deltaY)))
                except: # target square not on board
                    pass
    if not piece % 7: # rook or 1/2 queen
        for deltaY in (-1, 1): # constant X, vary Y
            n = 1
            try: # target square on board
                while not board[Y + (n * deltaY)][X]: # empty space at target square
                    moves.append(pos(X, Y + (n * deltaY)))
                    n += 1
                if turn * board[Y + (n * deltaY)][X] < 0: # enemy piece at target square
                    moves.append(pos(X, Y + (n * deltaY)))
            except: # target square not on board
                pass
        for deltaX in (-1, 1): # constant Y, vary X
            n = 1
            try: # target square on board
                while not board[Y][X + (n * deltaX)]: # empty space at target square
                    moves.append(pos(X + (n * deltaX), Y))
                    n += 1
                if turn * board[Y][X + (n * deltaX)] < 0: # enemy piece at target square
                    moves.append(pos(X + (n * deltaX), Y))
            except: # target square not on board
                pass
    if not piece % 11: # king
        for deltaY in xrange(-1, 2): # zero or one space down or up
            for deltaX in xrange(-1, 2): # zero or one space left or right
                try: # target square on board
                    if turn * board[Y + deltaY][X + deltaX] <= 0: # enemy piece or empty space at target square
                        moves.append(pos(X + deltaX, Y + deltaY))
                except: # target square not on board
                    pass
    return moves

def makeMove(board, symbols, turn, move): # todo: en passante and castling
    fromPos = move[0: 2]
    fromX, fromY = coords(fromPos)
    piece = board[fromY][fromX]
    if turn * piece <= 0:
        if turn * piece:
            print "Invalid move: You can't move your opponent's " + symbols[piece] + ' on '  + fromPos + '.'
        else:
            print "Invalid move: You don't have a piece on the " + fromPos + ' square to move.'
        return False
    toPos = move[2: ]
    toX, toY = coords(toPos)
    destination = board[toY][toX]
    if turn * destination > 0:
        print 'Invalid move: Your ' + symbols[destination] + ' is already occupying the ' + toPos + ' square.'
        return False
    moves = getMoves(board, fromX, fromY)
    if toPos not in moves:
        print'Illegal move: Your ' + symbol[piece] + ' on ' + fromPos + " can't move to " + toPos + '.'
        return False
    next_board = deepcopy(board)
    next_board[toY][toX] = piece
    next_board[fromY][fromX] = 0
    moves = []
    for X in xrange(DIM):
        for Y in xrange(DIM):
            moves += getMoves(next_board, X, Y)
            if next_board[Y][X] and not next_board[Y][X] % 11:
                if turn * next_board[Y][X] > 0:
                    ownKing = pos(X, Y)
                else:
                    otherKing = pos(X, Y)
    if ownKing in moves:
        print 'Illegal move: Your move caused your ' + symbols[turn * 11] + ' to go under check.'
        return False
    if otherKing in moves:
        print 'Check!'
    return next_board

home = [7, 3, 5, 35, 11, 5, 3, 7]

board = [home if not row else [2] * DIM if row == 1 else [-2] * DIM if row == 6 else [-piece for piece in home] if row == 7 else [0] * DIM for row in xrange(DIM)]

displayBoard(board, symbols)

players = ('White', 'Black')

moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'd2d3', 'd7d5', 'e4d5', 'f6d5', 'f3g5']

for i in xrange(len(moves)):
    print
    print players[i % 2] + ': ' + moves[i]
    system('say ' + players[i % 2] + ': ' + moves[i])
    board = makeMove(board, symbols, (-1) ** i, moves[i])
    displayBoard(board, symbols)
