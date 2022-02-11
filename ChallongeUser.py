class ChallongeUser:

    def __init__(self, display_name, opponents, rds, outcomes):

        self.display_name = display_name
        self.opponents = opponents
        self.rds = rds
        self.outcomes = outcomes

    def setOpponents(self, opponents):

        self.opponents = opponents

    def setOutcomes(self, outcomes):

        self.outcomes = outcomes

    def setRDs(self, rds):

        self.rds = rds

    def printAll(self):

        print(self.display_name)
        print(self.opponents)
        print(self.rds)
        print(self.outcomes)