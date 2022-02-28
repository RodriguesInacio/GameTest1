try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector


class Score:
    # Make an initialiser with a score for player 1 and player 2
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.score = ("Blue: " + str(self.score1) +
                      " Green: " + str(self.score2))

    def incrementScore1(self):
        self.score1 += 1

    def incrementScore2(self):
        self.score2 += 1

    def resetScores(self):
        self.score1 = 0
        self.score2 = 0

    def printScore(self):
        self.checkScore()
        self.score = ("Blue: " + str(self.score1) +
                      " Green: " + str(self.score2))

    def checkScore(self):
        if self.score1 >= 10:
            print("Blue has won")
            self.resetScores()
            return True
        elif self.score2 >= 10:
            print("Green has won")
            self.resetScores()
            return True
        else:
            print("The game continues")
            return False
