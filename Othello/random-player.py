import random
  
class MyPlayer:
  '''Hrac hraje nahodne'''
  def __init__(self, my_color, opponent_color):
    self.my_color = my_color
    self.opponent_color = opponent_color
    self.name = "zanzajen"
  
    
  def move(self, board):
    self.board = board
    self.smery = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)] 
    self.valid_moves = []
    for i in range(len(self.board)):
      for j in range(len(self.board)):
        if self.board[i][j] == -1 :
          for u, v in self.smery:
            x = u
            y = v
            if 0 <= i+x < 8 and 0 <= y+j <8 and self.board[i+u][j+v]==self.opponent_color:
              while 0 <= i+x < 8 and 0 <= y+j <8:
                if self.board[i+x][j+y] == -1:
                  break
                if self.board[i+x][j+y] == self.my_color:
                  self.valid_moves.append((i, j))
                  break
                x += u
                y += v
    if len(self.valid_moves) == 0:
      return (-1,-1)
    else:
      return random.choice(self.valid_moves)
