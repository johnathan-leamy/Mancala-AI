#todo
# add the take rest rule
numHoles = 7
startNum = 4

def validate_move(move, player):
  
  # check if move is a valid pit on the board
  if not (0 <= move < numHoles-1):
    return False
  
  # check if pit contains any stones
  if board[player][move] == 0:
    return False
  
  return True

def make_move(position,move, player, go_again=False, captured=False):
  new_position = [row[:] for row in position]
  # take all stones from selected pit
  stones = new_position[player][move]
  new_position[player][move] = 0
  startplayer = player
  # distribute stones in other pits
  while stones > 0:
    move += 1
    if (move > numHoles-1) or (move > numHoles-2 and startplayer != player):
      # switch players
      player = 1 - player
      move = 0
      
      # if last stone was placed in own mancala, player gets to go again
    if stones == 1:
        go_again = (player == current_player and move == numHoles-1)
       
  
    # capture opponent's pieces if final stone is placed in empty pit on player's side
    if stones == 1 and new_position[player][move] == 0 and player == current_player and move != 5:
      captured = True
      # add captured pieces to player's mancala
      new_position[player][numHoles-1] += new_position[1-player][numHoles-2-move] + 1
      new_position[1-player][numHoles-2-move] = 0
      new_position[player][move] -= 1
      
    new_position[player][move] += 1
    stones -= 1
    
  return new_position, go_again, captured

MAX = 0
      
def minimax(position, player, depth):
  # base case: game is over or maximum search depth is reached
  if game_over(position,player) or depth == 0:
    return evaluate(position)
  #if depth == 0:
  #     return evaluate()
  # initialize best score and best move
  best_score = -float("inf") if player == MAX else float("inf")
  best_move = None
  
  # generate list of possible moves
  moves = generate_moves(position,player)
  
  # explore each possible move
  for move in moves:
    # make move and switch players
    new_position = make_move(position, move, player)
    new_player = 1 - player
    
    # evaluate move using minimax function recursively
    score = minimax(new_position[0], new_player, depth - 1)
    #print("score:")
    #print(score)
    if(type(score) == tuple):
        score = score[0]
    
    
    # update best score and move if necessary
    if player == MAX:#change 1 to MAX
      if score > best_score:
        best_score = score
        best_move = move
    else:
      if score < best_score:
        best_score = score
        best_move = move
  
  return best_score, best_move

def game_over(position,player):
  # check if either player has no more pieces
  #print("position: ")
  #print(position[0][0])
  #print("that was position")
  #return sum(position[0]) == 0 or sum(position[1]) == 0
  return len(generate_moves(position, player)) == 0
    

def evaluate(position):
  # use simple heuristic to evaluate position
  # (higher score is better for player)
  return position[0][numHoles-1] - position[1][numHoles-1]
#for the minimax but prob better to just loop through each pit
def generate_moves(position, player):
  # return a list of non-empty pits on the player's side of the board

  return [i for i in range(numHoles-1) if position[player][i] > 0]

if __name__ == '__main__':
    # initialize game board
    board = [[startNum, startNum, startNum, startNum, startNum, startNum, 0], [startNum, startNum, startNum, startNum, startNum, startNum, 0]]
    #board = [[1, 0, 1, 2, 2, 2, 28], [1, 1, 1, 1, 1, 0, 8]]
    # initialize current player
    current_player = 0

    while True:
        # display game board
        print(board)
        print(minimax(board, current_player, 6))
        # allow current player to make a move
        move = input("Player " + str(current_player) + ", select a pit: ")
        move = int(move)
        # validate move and make it
        if validate_move(move, current_player):
            board, go_again, captured = make_move(board,move, current_player)
            if captured:
                print("Player " + str(current_player) + " has captured pieces!")
        else:
            print("Invalid move, please try again")
            continue
  
        # check for end of game
        print(len(generate_moves(board, current_player)))
        if game_over(board,current_player):
            print("Game over!")
            break
  
         # switch players if necessary
        if not go_again:
            current_player = 1 - current_player
        else:
            print("go again")

#todo add neural network