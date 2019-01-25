# class Game implements: 
# taking 2 players and letting them play the PD game for a specified 
# number of iterations. 
#
# A typical use is: 
# 1) construct an instance of the Game class
# 2) invoke the run() method 
# 3) invoke the get_players_payoffs() method.

class Game:
    def __init__(self, playerA, playerB, payoff_matrix, number_of_iterations):
        # INPUTS:
        # playerA, playerB: 
        #      the players (objects)
        #
        # payoff_matrix:
        #      payoff matrix which tells me each player's payoff, based on 
        #      what the players moves were. 
        #
        #      The matrix has the following indexing:
        #      payoff_matrix[playerA_move] [playerB_move] [player_payoff_index]
        #         where player_payoff_index=0 for playerA and =1 for playerB
        #         and both playerA_move and playerB_move are either 0 or 1:
        #         COOPERATE (=0)/DEFECT (=1)
        #
        # number_of_iterations: 
        #      number of iterations to be played in a game.
        # 
        # OUTPUTS:
        # (none)
        
        # store the input variables:
        self.players = playerA, playerB
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations=number_of_iterations

        # initialize the players payoffs to None:
        self.playerA_payoff = None
        self.playerB_payoff = None
        # we do this because if the user invokes the 
        # get_players_payoffs() method (see below) before the game
        # was run, we need to return the undefined state.

    def run(self):
        # INPUTS, OUTPUTS: none

        # initiate players' scores to 0
        self.playerA_payoff = 0
        self.playerB_payoff = 0

        playerA, playerB = self.players

        for iteration in range(1,self.number_of_iterations+1):
            print(iteration)
            playerA_move=playerA.move()
            playerB_move=playerB.move()

            # let the players know their opponent's move
            playerA.record_opponents_move(playerB_move)
            playerB.record_opponents_move(playerA_move)

            # update their scores:
            self.playerA_payoff = self.playerA_payoff + \
                self.payoff_matrix[playerA_move][playerB_move][0]
            self.playerB_payoff = self.playerB_payoff + \
                self.payoff_matrix[playerA_move][playerB_move][1]


    def get_players_payoffs(self):
        # INPUTS: none 
        # OUTPUTS: 
        #     a 2-element list with playerA's payoff and playerB's payoff
        return([self.playerA_payoff, self.playerB_payoff])
        # note that this would be [None, None] if the game has not been run.
