import copy

# Player 1: User
# Player 2: Machine

board = [
  [' ', ' ', ' '],
  [' ', ' ', ' '],
  [' ', ' ', ' '],
]

###
# Debug
###

def debug_print_children(children):
  for child in children:
    print('child: ', child)

###
# Minimax & Tree
###

def is_terminal(node):
  board = node['board']
  return has_winner(board, 'O') or has_winner(board, 'X') or is_tied(board)

def node_value(node):
  board = node['board']
  if (has_winner(board, 'O') == True):
    return 1
  if (has_winner(board, 'X') == True):
    return -1
  if (is_tied(board) == True):
    return 0

def node_children(node, char):
  children = []
  board = node['board']
  for x in range(3):
    for y in range(3):
      if (board[x][y] == ' '):
        child = {'board': copy.deepcopy(board), 'move': [x, y]}
        child['board'][x][y] = char
        children.append(child)
  return children

def minimax(node, is_maximizing):
  if (is_terminal(node)):
    return node_value(node), node

  children = node_children(node, 'O' if is_maximizing else 'X')

  if (is_maximizing):
    biggest_node = None
    value = -1
    for child in children:
      v, n = minimax(child, False)
      if (v > value):
        value = v
        biggest_node = child
    return value, biggest_node

  else:
    smallest_node = None
    value = 1
    for child in children:
      v, n = minimax(child, True)
      if (v < value):
        value = v
        smallest_node = child
    return value, smallest_node

###
# Game core
###

def is_player_1_round(round):
  return round % 2 == 1

def print_board():
  print(board[0])
  print(board[1])
  print(board[2])

def ask_user_move():
  while (True):
    [x, y] = input('Your move: ').split()
    x = int(x)
    y = int(y)

    if (x < 0 or x > 2 or y < 0 or y > 2 or board[x][y] != ' '):
      print('Invalid move.')
    else:
      break

  return x, y

def pick_machine_move():
  node = {'board': board}
  _, node = minimax(node, True)
  [x, y] = node['move']
  return x, y

def make_move(symbol, x, y):
  board[x][y] = symbol

def has_winner(board, char):
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
    print_board()

    if (has_winner(board, 'X') == True):
      print("X Won!")
      break

    if (has_winner(board, 'O') == True):
      print("O Won!")
      break

    if (is_tied(board) == True):
      print("Tie!")
      break

    if (is_player_1_round(round)):
      x, y = ask_user_move()
      make_move('X', x, y)

    else:
      x, y = pick_machine_move()
      make_move('O', x, y)

play()