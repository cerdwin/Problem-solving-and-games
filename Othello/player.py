class MyPlayer:
    """Trivial player looking into near future and adjusting his heuristics"""
 
    # valid directions of movement along the board
    directions = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]
 
    # a map of "heat" of each possible move on the board
    heat_map = [[120, -200, 20, 5, 5, 20, -200, 120], [-200, -100, -5, -5, -5, -5, -100, -200],
                [20, -5, 15, 3, 3, 15, -5, 20],
                [5, -5, 3, 3, 3, 3, -5, 5], [5, -5, 3, 3, 3, 3, -5, 5], [20, -5, 15, 3, 3, 15, -5, 20],
                [-200, -100, -5, -5, -5, -5, -100, -200], [120, -200, 20, 5, 5, 20, -200, 120]]
 
    def __init__(self, my_color, opponent_color):
        """Creates an instance of the class """
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.name = "zanzajen"
 
    def board_duplicate(self, board):
        """Copy of current board"""
        new_board = [row[:] for row in board]       # list comprehension notation for all fields in the board
        return new_board
 
    def valid_moves(self, board, my_color, opponent_color):
        """Finds all valid moves for my player"""
        available_moves = []        # we start of without any
        for i in range(len(board)):
            for j in range(len(board)):     # searching the entire grid
                if board[i][j] == -1:       # if we find an empty slot, we check:
                    for u, v in self.directions:
                        x = u   # x and y correspond to coordinates in the board 2D matrix
                        y = v
                        if 0 <= i + x < 8 and 0 <= y + j < 8 and board[i + u][j + v] == opponent_color:
                            while 0 <= i + x < 8 and 0 <= y + j < 8:    # we check placement and color of a field
                                if board[i + x][j + y] == -1:  # if we do not find our color, we search elsewhere
                                    break
                                if board[i + x][j + y] == my_color:  # if we do find it, we know its a valid move
                                    available_moves.append((i, j))
                                    break
                                x += u
                                y += v
        return available_moves  # the function returns all the possible moves given current board status
 
    def opponents_valid_moves(self, board, my_color, opponent_color):
        """Finds all possible moves opponent may make"""
        opponent_available_moves = []       # analogous to previous one, added to preserve clarity in the distinction
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == -1:
                    for u, v in self.directions:
                        x = u
                        y = v
                        if 0 <= i + x < 8 and 0 <= y + j < 8 and board[i + u][j + v] == my_color:
                            while 0 <= i + x < 8 and 0 <= y + j < 8:
                                if board[i + x][j + y] == -1:
                                    break
                                if board[i + x][j + y] == opponent_color:
                                    opponent_available_moves.append((i, j))
                                    break
                                x += u
                                y += v
        return opponent_available_moves         # function returns all opponents possible moves given board status
 
    def move_consequence(self, some_board, color_a, color_b, v, w):     # v, w are mere indexes of possible moves
        """Simulates effects of a move on board"""
        for i, j in self.directions:        # the function enacts changes to the board in every direction
            a = v
            b = w       # the body of the function is similar to that of previous two functions
            if 0 <= a + i < 8 and 0 <= b + j < 8 and some_board[a + i][b + j] == color_b:
                while 0 <= a + i < 8 and 0 <= b + j < 8 and some_board[a + i][b + j] != -1:
                    if some_board[a + i][b + j] == color_a:
                        a = a - i
                        b = b - j
                        while 0 <= a + i < 8 and 0 <= b + j < 8 and some_board[a + i][b + j] != color_a:
                            some_board[a + i][b + j] = color_a
                            a = a - i
                            b = b - j
                        break
                    a = a + i
                    b = b + j
        return some_board
 
    def optimal_move(self, board, my_color, opponent_color):    # function looks one move forward to assess moves
        """Adjusts move as per opponents possible choices"""
        possible_moves = self.valid_moves(board, self.my_color, self.opponent_color)        # all possible moves
        if len(possible_moves) == 0:
            return None         # If there are no possible moves available, returns None
        else:
            best_score = -999999999999
            my_worst_score = 999999999999
            my_move = ()
            for v,w in possible_moves:
                mock_board = self.board_duplicate(board)        # the simulates different states of the game
                mock_board[v][w] = self.my_color        # changes board by placing a potential stone
                mock_board = self.move_consequence(mock_board, my_color, opponent_color, v, w)  # evaluates
                # now, analyzing first layer- opponents possible response
                opponents_view = self.opponents_valid_moves(mock_board, self.my_color, self.opponent_color)
                for o, p in opponents_view:     # finds opponents all possible moves given ours
                    second_mock_board = self.board_duplicate(mock_board)        # repeats process above deeper
                    second_mock_board[o][p] = self.opponent_color
                    second_mock_board = self.move_consequence(mock_board, opponent_color, my_color, o, p)  # beware
                    opponent_minimized_potential_score = self.evaluate(second_mock_board, my_color, opponent_color)
                    if opponent_minimized_potential_score < my_worst_score:     # opponent tries to minimize our score
                        my_worst_score = opponent_minimized_potential_score
                if my_worst_score > best_score:     # given zero-sum nature, we want the best scenario for us
                    best_score = my_worst_score
                    my_move = (v, w)
            return my_move      # finally, we have our ideal move as per algorithm
 
    def evaluate(self, board, my_color, opponent_color):    # We evaluate the given state of board
        """Ranks the current board by attractiveness in heatmap"""
        my_score = 0
        opponent_score = 0
        for i in range(len(board)):
            for y in range(len(board)):
                if board[i][y] == my_color:     # each time we see our stone, we add its respective value
                    my_score = my_score + self.heat_map[i][y]
                elif board[i][y] == opponent_color:     # same applies for opponents stones
                    opponent_score = opponent_score + self.heat_map[i][y]
        return my_score - opponent_score        # function returns sort-of score, based on the heatmap
 
    def move(self, board):
        """Deciding on final move based on future and my heuristics"""
        my_decision = self.optimal_move(board, self.my_color, self.opponent_color)      # algorithm result
        final_call = my_decision
        all_moves = self.valid_moves(board, self.my_color, self.opponent_color)     # checking all moves again
        x = final_call[0]       # mere coordinates of result on the heatmap
        y = final_call[1]
        if self.heat_map[x][y] < -90:  # I added some heuristics I follow when I play against computer
            if len(all_moves) > 1:
                for i, v in all_moves:
                    if self.heat_map[i][v] > -100:  # just making sure we choose a corner when we can
                        final_call = (i, v)
                        if self.heat_map[i][v] > 50:
                            final_call = (i, v)
        return final_call       # alea iacta est
        
