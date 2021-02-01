#87671-Joao Freitas
#87693-Pedro Soares
from search import *
from utils import *

#----------------------------------------------------------------------------------
#TAI content
def c_peg():
    return "O"
def c_empty():
    return "_"
def c_blocked():
    return "X"
def is_empty(e):
    return e == c_empty()
def is_peg(e):
    return e == c_peg()
def is_blocked(e):
    return e == c_blocked()

#----------------------------------------------------------------------------------
# TAI pos
# Tuplo (l, c)
def make_pos(l, c):
    return (l, c)
def pos_l(pos):
    return pos[0]
def pos_c(pos):
    return pos[1]

#-------------------------------------------------------------------------------------
# TAI move
# Lista [p_initial, p_final]
def make_move(i, f):
    return [i, f]
def move_initial(move):
    return move[0]
def move_final(move):
    return move[1]

#----------------------------------------------------------------------------------------
# TAI board

def line_number(board):
    return len(board)

def column_number(board):
    return len(board[0])

def board_copy(board):
    return [list(row) for row in board]

def board_moves(board):
    movs = []
    lines = line_number(board)
    columns = column_number(board)
    
    for l in range(lines):
        for c in range(columns):
            if is_peg(board[l][c]):
                if 0<=c-2<columns and is_empty(board[l][c-2]) and is_peg(board[l][c-1]):#verifica se duas colunas atras existe posicao valida e se esta vazia->verifica se uma coluna atras tem peca
                    movs.append(make_move(make_pos(l,c),make_pos(l,c-2)))
                        
                if 0<=l-2<lines and is_empty(board[l-2][c]) and is_peg(board[l-1][c]):
                    movs.append(make_move(make_pos(l,c),make_pos(l-2,c)))
                        
                if 0<=c+2<columns and is_empty(board[l][c+2]) and is_peg(board[l][c+1]):
                    movs.append(make_move(make_pos(l,c),make_pos(l,c+2)))
                        
                if 0<=l+2<lines  and is_empty(board[l+2][c]) and is_peg(board[l+1][c]):
                    movs.append(make_move(make_pos(l,c),make_pos(l+2,c)))
    return movs

def non_movable_pegs(board):
    count=0
    lines = line_number(board)
    columns = column_number(board)

    for l in range(lines):
        for c in range(columns):
            if is_peg(board[l][c]):
                if 0<=c-2<columns and is_peg(board[l][c-1]) and is_empty(board[l][c-2]):
                    continue

                elif 0<=l-2<lines and is_peg(board[l-1][c]) and is_empty(board[l-2][c]):
                    continue

                elif 0<=c+2<columns and is_peg(board[l][c+1]) and is_empty(board[l][c+2]):
                    continue

                elif 0<=l+2<lines and is_peg(board[l+1][c]) and is_empty(board[l+2][c]):
                    continue
                
                else:
                    count+=1
    return count


def middle_peg_pos(first_move,final_move):
    if(pos_l(first_move)==pos_l(final_move)):
        if(pos_c(final_move)-pos_c(first_move))==2:
            return (pos_l(first_move),pos_c(final_move)-1)
        else:
            return (pos_l(first_move),pos_c(final_move)+1)
        
    elif(pos_c(first_move)==pos_c(final_move)):
        if(pos_l(final_move)-pos_l(first_move))==2:
            return (pos_l(first_move)+1,pos_c(first_move))
        else:
            return (pos_l(first_move)-1,pos_c(first_move))

def board_perform_move(board,move):
    new_board = board_copy(board)
    
    new_board[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty() #apaga peca da posicao inicial
    
    middle_pos=middle_peg_pos(move_initial(move),move_final(move)) #calcula posicao da peca a desaparecer e apaga peca dessa posicao
    new_board[pos_l(middle_pos)][pos_c(middle_pos)]=c_empty()
    
    new_board[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg() #poe peca na posicao final
    return new_board

def board_peg_count(board):
    peg_number=0
    	
    for l in board:
        peg_number += l.count(c_peg())
	
    return peg_number

#------------------------------------------------------------------------------------
# TAI sol_state
# Classe que contem configuracao de uma board
class sol_state():
    __slots__ = 'board'

    def __init__(self, board): 
        self.board = board
    
    def __lt__(self, sol_state):
        return board_peg_count(self.board) > board_peg_count(sol_state.board)

#------------------------------------------------------------------------------------
# TAI solitaire
class solitaire(Problem):
    __slots__ = 'initial'
    
    def __init__(self, board):
        self.initial=sol_state(board)
    
    def actions(self,state):
        return board_moves(state.board)
        
    def result(self,state,action):
        return sol_state(board_perform_move(state.board,action))
    
    def goal_test(self, state):
        if board_peg_count(state.board)==1:
            return True
        else:
            return False
    
    def path_cost(self, c, state1, action, state2):
        return c+1
    
    def h(self,node):
        return board_peg_count(node.state.board) + non_movable_pegs(node.state.board)