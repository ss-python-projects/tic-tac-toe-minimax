import math
import copy
import os

###
# Hard depth: 9 (max)
# Medium depth: 5
# Easy depth: 1
###

# X: User
# O: Machine

board = [
  [' ', ' ', ' '],
  [' ', ' ', ' '],
  [' ', ' ', ' '],
]

###
# Minimax & Tree
###

"""
Check if a given node is a terminal one. This logic
varies from game to game.
"""
def is_node_terminal(node):
  board = node['board']
  return is_winner(board, 'O') or is_winner(board, 'X') or is_tied(board)

def are_middles_empty(board):
  mid1 = board[0][1]
  mid2 = board[1][0]
  mid3 = board[1][2]
  mid4 = board[2][1]
  return (mid1 == ' ' and mid2 == ' ' and mid3 == ' ' and mid4 == ' ')

def is_trap(board):
  # 0,0 - 0,2 - 2,0 - 2,2
  # 1,1
  quina1 = board[0][0]
  quina2 = board[0][2]
  quina3 = board[2][0]
  quina4 = board[2][2]
  meio = board[1][1]
  return (
    (quina1 == 'O' and quina2 == 'O' and quina3 == 'O' and quina4 == 'X' and meio == 'X' and are_middles_empty(board)) or
    (quina2 == 'O' and quina3 == 'O' and quina4 == 'O' and quina1 == 'X' and meio == 'X' and are_middles_empty(board)) or
    (quina3 == 'O' and quina4 == 'O' and quina1 == 'O' and quina2 == 'X' and meio == 'X' and are_middles_empty(board)) or
    (quina4 == 'O' and quina1 == 'O' and quina2 == 'O' and quina3 == 'X' and meio == 'X' and are_middles_empty(board))
  )

"""
Calculate the node value. This logic varies from game
to game.
"""
def get_node_value(node):
  board = node['board']
  if (is_winner(board, 'O') == True and is_trap(board)):
    return 2
  elif (is_winner(board, 'O') == True):
    return 1
  elif (is_winner(board, 'X') == True):
    return -1
  else:
    return 0

"""
Generate the children for that node. Returns an array
of nodes (children).
"""
def get_node_children(node, char):
  children = []
  board = node['board']
  for x in range(3):
    for y in range(3):
      if (board[x][y] == ' '):
        child = {'board': copy.deepcopy(board), 'move': [x, y]}
        child['board'][x][y] = char
        children.append(child)
  return children

"""
Given a list of nodes, return the max one.
"""
def get_max_node(nodes, depth):
  max_node = nodes[0]
  max_value = -1
  for node in nodes:
    v, n = minimax(node, False, depth-1)
    if (v > max_value):
      max_value = v
      max_node = node
  return max_value, max_node

"""
Given a list of nodes, return the min one.
"""
def get_min_node(nodes, depth):
  min_node = nodes[0]
  min_value = 2
  for node in nodes:
    v, n = minimax(node, True, depth-1)
    if (v < min_value):
      min_value = v
      min_node = node
  return min_value, min_node

"""
Minimax implementation.
"""
def minimax(node, is_maximizing, depth):
  if (depth == 0 or is_node_terminal(node)):
    return get_node_value(node), node

  children = get_node_children(node, 'O' if is_maximizing else 'X')

  if (is_maximizing):
    value, node = get_max_node(children, depth)
    if (value == 2):
      print('max', value, node)
    return value, node

  else:
    value, node = get_min_node(children, depth)
    return value, node

###
# Game core
###

"""
Clear the terminal screen.
"""
def clear():
  os.system('clear')

"""
Check if current round refers to the player 1's turn.
"""
def is_player_1_turn(round):
  return round % 2 == 1

"""
Print the board on the screen in an human readable format.
"""
def print_board():
  for x in range(3):
    print('[ ', end='')
    for y in range(3):
      if (board[x][y] == ' '):
        print(x * 3 + y + 1, ' ', end='')
      else:
        print(board[x][y], ' ', end='')
    print(']')

"""
Ask the human for a move and convert it into a 2D
coordinate (x, y).
"""
def ask_user_move():
  while (True):
    pos = int(input('Your move: '))
    x = int((pos - 1) / 3)
    y = int((pos - 1) % 3)
    if (pos < 1 or pos > 9 or board[x][y] != ' '):
      print('Invalid move.')
    else:
      break
  return x, y

"""
Pick a move for the machine (AI) and then convert it
into a 2D coordinate (x, y).
"""
def pick_machine_move(depth):
  node = {'board': board}
  _, node = minimax(node, True, depth)
  [x, y] = node['move']
  return x, y

"""
Make a move - which means putting a char into a specific
position on the board.
"""
def make_move(symbol, x, y):
  board[x][y] = symbol

"""
Check if given char won the match.
"""
def is_winner(board, char):
  return (
    board[0][0] == char and board[0][1] == char and board[0][2] == char or # line 1
    board[1][0] == char and board[1][1] == char and board[1][2] == char or # line 2
    board[2][0] == char and board[2][1] == char and board[2][2] == char or # line 3

    board[0][0] == char and board[1][0] == char and board[2][0] == char or # col 1
    board[0][1] == char and board[1][1] == char and board[2][1] == char or # col 2
    board[0][2] == char and board[1][2] == char and board[2][2] == char or # col 3

    board[0][0] == char and board[1][1] == char and board[2][2] == char or # main diag
    board[2][0] == char and board[1][1] == char and board[0][2] == char # sec diag
  )

"""
Check if current state is a draw by checking if any cell
is empty.
"""
def is_tied(board):
  return (
    board[0][0] != ' ' and board[0][1] != ' ' and board[0][2] != ' ' and
    board[1][0] != ' ' and board[1][1] != ' ' and board[1][2] != ' ' and
    board[2][0] != ' ' and board[2][1] != ' ' and board[2][2] != ' '
  )

"""
Ask the user for the difficulty level.
"""
def ask_difficulty_level():
  option = 0
  while (True):
    print("[1] Fácil")
    print("[2] Médio")
    print("[3] Difícil")
    option = int(input('Qual a dificuldade? '))
    if (option > 0 and option < 4):
      break

  if (option == 1):
    return 1
  if (option == 2):
    return 5
  if (option == 3):
    return 9

def play():
  round = 0

  depth = ask_difficulty_level()
  clear()

  while (True):
    round = round + 1

    # clear()
    print_board()

    if (is_winner(board, 'X') == True):
      print("X Won!")
      break

    if (is_winner(board, 'O') == True):
      print("O Won!")
      break

    if (is_tied(board) == True):
      print("Tie!")
      break

    if (is_player_1_turn(round)):
      x, y = pick_machine_move(depth)
      make_move('O', x, y)

    else:
      x, y = ask_user_move()
      make_move('X', x, y)

play()