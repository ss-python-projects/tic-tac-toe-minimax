import copy
import os

# Player 1: User
# Player 2: Machine

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

"""
Calculate the node value. This logic varies from game
to game.
"""
def get_node_value(node):
  board = node['board']
  if (is_winner(board, 'O') == True):
    return 1
  if (is_winner(board, 'X') == True):
    return -1
  if (is_tied(board) == True):
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
Given a list of nodes, return the biggest one (max).
"""
def get_max_node(nodes):
  max_node = None
  max_value = -1
  for node in nodes:
    v, n = minimax(node, False)
    if (v > max_value):
      max_value = v
      max_node = node
  return max_value, max_node

"""
Given a list of nodes, return the smallest one (min).
"""
def get_min_node(nodes):
  min_node = None
  min_value = 1
  for node in nodes:
    v, n = minimax(node, True)
    if (v < min_value):
      min_value = v
      min_node = node
  return min_value, min_node

"""
Minimax implementation.
"""
def minimax(node, is_maximizing):
  if (is_node_terminal(node)):
    return get_node_value(node), node

  children = get_node_children(node, 'O' if is_maximizing else 'X')

  if (is_maximizing):
    value, node = get_max_node(children)
    return value, node

  else:
    value, node = get_min_node(children)
    return value, node

###
# Game core
###

def clear():
  os.system('clear')

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
def pick_machine_move():
  node = {'board': board}
  _, node = minimax(node, True)
  [x, y] = node['move']
  return x, y

"""
Make a move - which means putting a char into a specific
position on the board.
"""
def make_move(symbol, x, y):
  board[x][y] = symbol

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

def is_tied(board):
  return (
      board[0][0] != ' ' and board[0][1] != ' ' and board[0][2] != ' ' and
      board[1][0] != ' ' and board[1][1] != ' ' and board[1][2] != ' ' and
      board[2][0] != ' ' and board[2][1] != ' ' and board[2][2] != ' '
  )

def play():
  round = 0

  while (True):
    round = round + 1

    clear()
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
      x, y = ask_user_move()
      make_move('X', x, y)

    else:
      x, y = pick_machine_move()
      make_move('O', x, y)

play()