class MyPlayer:
 
    """Simple Tit-for-tat-like player adjusted i.a. for noise and abnormal payoff order"""
 
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.past_moves = []
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.CC = payoff_matrix[0][0][0]
        self.CD = payoff_matrix[0][1][0]
        self.DC = payoff_matrix[1][0][0]
        self.DD = payoff_matrix[1][1][0]
 
        # Defining shortcuts for conditions of my 4 possible strategies to add clarity
 
        if self.DC > self.CC > self.DD > self.CD:
            self.tit_conditions = True
        if self.CD > self.CC > self.DD > self.DC:
            self.cooperator_conditions = True
        if self.DC > self.DD > self.CC > self.CD:
            self.defector_conditions = True
        if self.CD > self.DD > self.CC > self.DC:
            self.tat_conditions = True
 
    # Strategies
 
    def tit_for_tat(self):  # My main strategy - simple tit-for-tat
        if len(self.past_moves) > 0:
            if self.past_moves[-1] == 1:
                return False
            elif self.past_moves[-1] == 0:
                return True
        else:
            return False
 
    def tat_for_tit(self):  # New strategy in case of an abnormal payoff matrix specified below
        if len(self.past_moves) > 0:
            if self.past_moves[-1] == 1:
                return True
            elif self.past_moves[-1] == 0:
                return False
        else:
            return True
 
    # Checking the payoff matrix to adjust for non-standard, yet symmetric, matrices
 
    def matrix_check(self):
        if self.tit_conditions == 1:
            return self.tit_for_tat()
        elif self.cooperator_conditions == 1:
            return False
        elif self.defector_conditions == 1:
            return True
        else:
            return self.tat_for_tit()
 
    # Move - adjusted for knowledge of no. of iterations and noise
 
    def move(self):
        if self.number_of_iterations is None:  # In an infinite game, I cannot change last move, hence standard strategy
            return self.matrix_check()
        else:  # If I know the exact number of iterations, I can play the subgame perfect equilibrium through betrayal
            while len(self.past_moves) < self.number_of_iterations - 1:
                if len(self.past_moves) < 2:
                    return self.matrix_check()
                else: # Due to potential noise, my player forgives one defection after three cooperations
                    if self.tit_conditions == 1:
                        if self.past_moves[-4:] == 3*[1]+[0]:
                            return False
                        else:
                            return self.matrix_check()
                    elif self.tat_conditions == 1:
                        if self.past_moves[-4:] == 3*[0]+[1]:
                            return True
                        else:
                            return self.matrix_check()
                    else:
                        return self.matrix_check()
            if len(self.past_moves) >= self.number_of_iterations - 1:  # In last round cooperation has to stop
                if self.tit_conditions == 1:
                    return True
                elif self.tat_conditions == 1:
                    return False
                else:
                    return self.matrix_check()
 
    # History
 
    def record_opponents_move(self, opponent_move):
        self.past_moves.append(opponent_move)
