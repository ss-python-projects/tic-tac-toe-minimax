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
  board = node
  return has_winner(board, 'O') or has_winner(board, 'X') or is_tied(board)
  # return has_winner(board, 'O')

def node_value(node):
  board = node
  if (has_winner(board, 'O') == True):
    return 1
  if (has_winner(board, 'X') == True):
    return -1
  if (is_tied(board) == True):
    return 0

def node_children(node, char):
  # print('node: ', node) #debug
  children = []
  board = node
  for line in range(3):
    for col in range(3):
      if (board[line][col] == ' '):
        new_board = copy.deepcopy(board)
        # print('board', board) #debug
        # print('new board', new_board) #debug
        new_board[line][col] = char
        children.append(new_board)
  return children

def minimax(node, is_maximizing):
  # todo: implement
  # return 2, 2
  if (is_terminal(node)):
    # print('=== terminal') #debug
    # print('node: ', node) #debug
    # print('value: ', node_value(node)) #debug
    return node_value(node)

  children = node_children(node, 'O' if is_maximizing else 'X')

  if (is_maximizing):
    value = -1
    # print('=== max') #debug
    # print('node: ', node) #debug
    # debug_print_children(children) #debug
    for child in children:
      value = max(value, minimax(child, False))
    return value

  else:
    value = 1
    # print('=== min') #debug
    # print('node: ', node) #debug
    # debug_print_children(children) #debug
    for child in children:
      value = min(value, minimax(child, True))
    return value

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
  # todo: implement
  minimax(board, True)
  return 0, 0

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