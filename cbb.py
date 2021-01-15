############################################################
######
######         Team Class
######
############################################################

class Team:

# -> add conference to adjust rebounding values
    # initialize
    def __init__ (self, school, conference, adjMargin, steals, turnovers, offRebounds, 
                    reboundMargin, fgMade, fgAtt, threeMade, threeAtt, ftPct, 
                    fouls, gamesPlayed):
        self._school = school
        self._conference = conference
        self._adjMargin = adjMargin
        self._steals = steals                           
        self._turnovers = turnovers                   
        self._offRebounds = offRebounds                 # all season totals
        self._reboundMargin = reboundMargin           
        self._fgMade = fgMade                    
        self._threeMade = threeMade                 
        self._fgAtt = fgAtt                           
        self._threeAtt = threeAtt                      
        self._freeThrowPct = ftPct                   
        self._fouls = fouls                          
        self._gamesPlayed = gamesPlayed

    # simple gets
    def getSchool (self):
        return self._school
    def getConference (self):
        return self._conference
    def getAdjMargin (self):
        return self._adjMargin
    def getSteals (self):
        return self._steals
    def getOffRebounds (self):
        return self._offRebounds
    def getFgMade (self):
        return self._fgMade
    def getFgAtt (self):
        return self._fgAtt
    def getThreeMade (self):
        return self._threeMade
    def getThreeAtt (self):
        return self._threeAtt
    def getGamesPlayed (self):
        return self._gamesPlayed

    # get per games
    def getStealsPerGame (self):
        stealsPerGame = self._steals / self.getGamesPlayed()
        return stealsPerGame
    def getTurnoversPerGame (self):
        turnoversPerGame = self.adjustTurnovers() / self.getGamesPlayed()
        return turnoversPerGame
    def getReboundMarginPerGame (self):
        reboundMarginPerGame = self.adjustReboundMargin() / self.getGamesPlayed()
        return reboundMarginPerGame
    def getTwosPerGame (self):
        twosMade = self.adjustFgMade() - self.adjustThreeMade()
        twosPG = twosMade / self.getGamesPlayed()
        return twosPG
    def getThreesPerGame (self):
        threePG = self.adjustThreeMade() / self.getGamesPlayed()
        return threePG
    def getFoulsPerGame (self):
        foulsPerGame = self.adjustFouls() / self.getGamesPlayed()
        return foulsPerGame

    # get percentages
    def getFtPct (self):
        return self._freeThrowPct

    def getOffReboundPct (self):
        fgAttempts = self.getFgAtt()
        fgMade = self.getFgMade()
        missedShots = (fgAttempts - fgMade)
        offPct = (self.adjustOffRebounds() / missedShots) * 100
        return offPct

    def getFgPct (self):
        fgPct = (self.getFgMade() / self.getFgAtt()) * 100
        return fgPct

    def getTwoPct (self):
        fgMade = self.getFgMade()
        fgAttempted = self.getFgAtt()
        threesMade = self.getThreeMade()
        threesAttempted = self.getThreeAtt()
        
        twosMade = fgMade - threesMade
        twosAttempted = fgAttempted - threesAttempted
        twoPct = (twosMade / twosAttempted) * 100
        return twoPct

    def getThreePct (self):
        threePct = (self.getThreeMade() / self.getThreeMade()) * 100
        return threePct

    # dictionary of major conferences and assigned multiplier
    conferenceAdjuster = {"B10"      : 5, 
                          "ACC"      : 4, 
                          "B12"      : 4,
                          "SEC"      : 3, 
                          "Big East" : 3,
                          "AAC"      : 2,
                          "P12"      : 2,
                          "WCC"      : 1,
                          "A10"      : 1,
                          "MWC"      : 1,
                          "OVC"      : 1,

                          "America East": 0, "Atlantic Sun": 0, "Big Sky": 0, 
                          "Big South": 0, "Big West": 0, "Colonial": 0, 
                          "USA": 0, "Horizon": 0, "Ivy": 0, 
                          "Metro Atlantic": 0, "Mid American": 0, "MEAC": 0, 
                          "Missouri Valley": 0, "Northeast": 0, "Patriot": 0, 
                          "Southern": 0, "Southland": 0, "SWAC": 0, 
                          "Summit": 0, "Sun Belt": 0, "WAC": 0}

    # stat adjustments
    def getMultiplier (self):
        multiplier = self.conferenceAdjuster[self.getConference()]
        return multiplier
    def adjustTurnovers (self):
        self._turnovers = self._turnovers - int (15 * self.getMultiplier())
        return self._turnovers
    def adjustOffRebounds (self):
        self._offRebounds = self._offRebounds + int (15 * self.getMultiplier())
        return self._offRebounds
    def adjustReboundMargin (self):
        self._reboundMargin = self._reboundMargin + int (40 * self.getMultiplier())
        return self._reboundMargin
    def adjustFgMade (self):
        self._fgMade = self._fgMade + int (100 * self.getMultiplier())   
        return self._fgMade
    def adjustThreeMade (self):
        self._threeMade = self._threeMade + int (27.5 * self.getMultiplier())  
        return self._threeMade
    def adjustFouls (self):
        self._fouls = self._fouls - int (35 * self.getMultiplier())
        return self._fouls


############################################################
######
######         Game Class
######
############################################################

class Game:

    # initialize
    def __init__ (self, teamOne, teamTwo):
        self._teamOne = teamOne
        self._teamTwo = teamTwo
        self._winner = None

    def getWinner (self):
        return self._winner
    def setWinner (self, winner):
        self._winner = winner

    # determine if there is a great efficiency mismatch
    def efficiencyDifferential (self):
        effOne = self._teamOne.getAdjMargin()
        effTwo = self._teamTwo.getAdjMargin()
        effDiff = effOne - effTwo
        absDiff = abs(effDiff)

        winner = ""
        canDetermine = False

        if (absDiff >= 15):
            canDetermine = True
            if effDiff > 0:
                winner = self._teamOne.getSchool()
            else:
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine

    # determine if there is a great turnover difference 
    def turnoverDifferential (self):
        spgOne = self._teamOne.getStealsPerGame()
        spgTwo = self._teamTwo.getStealsPerGame()
        tpgOne = self._teamOne.getTurnoversPerGame()
        tpgTwo = self._teamTwo.getTurnoversPerGame()

        winner = ""
        canDetermine = False

        turnoverOne = (tpgOne + spgTwo) / 2
        turnoverTwo = (tpgTwo + spgOne) / 2
        turnoverDiff = turnoverOne - turnoverTwo
        absDiff = abs(turnoverDiff)

        # team rebounds per game - opponents rpg
        avgTODifferentialPerGame = 13.0 - 12.8
        avgStealsPerGame = 6.8 - 6.5
        avgGamesPlayed = int ((self._teamOne.getGamesPlayed() + self._teamTwo.getGamesPlayed()) / 2)

        avgDiff = avgTODifferentialPerGame * avgStealsPerGame

        if (absDiff >= avgDiff * avgGamesPlayed):
            canDetermine = True
            if (turnoverDiff > 0):
                winner = self._teamTwo.getSchool()
            else:
                winner = self._teamOne.getSchool()
        
        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine

    # determine if there is a great advantage in rebounding
    def reboundDifferential (self):
        offPctOne = self._teamOne.getOffReboundPct()
        offPctTwo = self._teamTwo.getOffReboundPct()

        rebMarginOne = self._teamOne.getReboundMarginPerGame()
        rebMarginTwo = self._teamTwo.getReboundMarginPerGame()
        rebMarginDiff = rebMarginOne - rebMarginTwo
        absMarginDiff = abs(rebMarginDiff)

        winner = ""
        canDetermine = False

        # team rebounds per game - opponents rpg
        avgReboundMarginPerGame = 35.05 - 34.9
        avgGamesPlayed = int ((self._teamOne.getGamesPlayed() + self._teamTwo.getGamesPlayed()) / 2)

        if (absMarginDiff >= avgReboundMarginPerGame * avgGamesPlayed):
            if (rebMarginDiff > 0 and offPctOne > 27):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (rebMarginDiff < 0 and offPctTwo > 27):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine

    # determine if there is a great advantage in three point shooting
    def threeDifferential (self):
        threesOne = self._teamOne.getThreesPerGame()
        threesTwo = self._teamTwo.getThreesPerGame()
        threePctOne = self._teamOne.getThreePct()
        threePctTwo = self._teamTwo.getThreePct()

        threeDiff = threesOne - threesTwo
        absDiff = abs(threeDiff)
        avgThreePct = 33

        winner = ""
        canDetermine = False

        # (ppg from 3 - opponent ppg from 3) / 3
        avgThreesMadePerGame = (24.05 - 22.9) / 3
        avgGamesPlayed = int ((self._teamOne.getGamesPlayed() + self._teamTwo.getGamesPlayed()) / 2)

        if (absDiff >= (avgThreesMadePerGame * avgGamesPlayed)):
            if (threeDiff > 0 and threePctOne >= avgThreePct):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (threeDiff < 0 and threePctTwo >= avgThreePct):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine     

    # determine if there is a great advantage in three point shooting
    def twoDifferential (self):  
        twosOne = self._teamOne.getTwosPerGame()
        twosTwo = self._teamTwo.getTwosPerGame() 
        twoPctOne = self._teamOne.getTwoPct()
        twoPctTwo = self._teamTwo.getTwoPct()

        twoDiff = twosOne - twosTwo
        absDiff = abs(twoDiff)
        avgTwoPct = 50
        
        winner = ""
        canDetermine = False

        # (ppg from 2 - opponent ppg from 2) / 2
        avgTwosMadePerGame = (35.55 - 34.95) / 2
        avgGamesPlayed = int ((self._teamOne.getGamesPlayed() + self._teamTwo.getGamesPlayed()) / 2)

        if (absDiff >= (avgTwosMadePerGame * avgGamesPlayed)):
            if (twoDiff > 0 and twoPctOne >= avgTwoPct):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (twoDiff < 0 and twoPctTwo >= avgTwoPct):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine     

    # finally determine free throw advantages
    def freeThrows (self):
        ftPctOne = self._teamOne.getFtPct()
        ftPctTwo = self._teamTwo.getFtPct()
        foulsOne = self._teamOne.getFoulsPerGame()
        foulsTwo = self._teamTwo.getFoulsPerGame()

        totalFtOne = ftPctOne * foulsTwo
        totalFtTwo = ftPctTwo * foulsOne

        winner = ""

        if (totalFtOne > totalFtTwo):
            winner = self._teamOne.getSchool()
        else:
            winner = self._teamTwo.getSchool()
        
        self.setWinner(winner)

    # figure out the winning team of the game
    def findWin (self):
        howWin = ""
        if (self.efficiencyDifferential() == True):
            howWin =  "efficiency"
        else:
            if (self.turnoverDifferential() == True):
                howWin = "turnovers"
            else:
                if (self.reboundDifferential() == True):
                    howWin = "rebounding"
                else:
                    if (self.threeDifferential() == True):
                        howWin = "threes"
                    else:
                        if (self.twoDifferential() == True):
                            howWin = "twos"
                        else:
                            self.freeThrows()
                            howWin = "free throws"

        result = ("Winner -> " + self.getWinner() + " via " + howWin)
        return result


############################################################
######
######         play out games from 2018-2019 March Madness
######
############################################################

########################################
######         West Region  ->  12 / 15
########################################

# name, effMargin, steals, TO, OR, rebMarg, FGM, FGA, 3PM, 3PA, FT%, PF, GP
Wseed01 = Team ("Gonzaga"            , "WCC"      , 32.85, 278, 394, 354, 277, 1177, 2239, 287, 790, 76.1, 603, 37)
Wseed16 = Team ("Fairleigh Dickinson", "Northeast", -4.22, 261, 477, 323, 35 , 921 , 1939, 269, 672, 72.5, 578, 35)

Wseed08 = Team ("Syracuse", "ACC", 15.13, 278, 423, 363, -79, 808, 1907, 274, 824, 68.5, 588, 34)
Wseed09 = Team ("Baylor"  , "B12", 16.48, 209, 446, 450, 195, 869, 1966, 274, 803, 67.7, 636, 34)

Wseed05 = Team ("Marquette"   , "Big East", 16.52, 168, 467, 331, 146, 893, 1969, 319, 822, 75.7, 635, 34)
Wseed12 = Team ("Murray State", "OVC"     , 13.83, 249, 401, 351, 102, 988, 2007, 258, 731, 73.3, 527, 33)

Wseed04 = Team ("Florida St", "ACC"         , 22.39, 266, 492, 418, 168, 960, 2171, 272, 819, 74.4, 705, 37)
Wseed13 = Team ("Vermont"   , "America East", 8.86 , 188, 377, 304, 144, 864, 1887, 273, 761, 74.8, 568, 34)

Wseed06 = Team ("Buffalo"   , "Mid American", 19.85, 263, 433, 452, 48 , 1083, 2344, 344, 1022, 68.7, 659, 36)
Wseed11 = Team ("Arizona St", "P12", 11.55, 213, 466, 399, 133, 899, 2012, 240, 714, 68.0, 675, 34)

Wseed03 = Team ("Texas Tech", "B12"    , 30.03, 278, 457, 315, 43 , 990, 2110, 277, 759, 73.2, 663, 38)
Wseed14 = Team ("N Kentucky", "Horizon", 7.14 , 218, 441, 364, 157, 979, 2047, 306, 844, 66.6, 664, 35)

Wseed07 = Team ("Nevada" , "MWC", 18.18, 211, 352, 325, 88 , 924, 1999, 297, 855, 70.8, 584, 34)
Wseed10 = Team ("Florida", "SEC", 18.30, 257, 420, 375, -41, 857, 2015, 291, 872, 72.1, 614, 36)

Wseed02 = Team ("Michigan", "B10"    , 28.32, 225, 334, 299, 34, 941, 2102, 287, 839, 70.1, 514, 37)
Wseed15 = Team ("Montana" , "Big Sky", 3.53 , 229, 416, 293, 82, 975, 1983, 287, 763, 68.9, 655, 35)

Wgame1  = Game (Wseed01, Wseed16)
Wgame2  = Game (Wseed08, Wseed09)
Wgame3  = Game (Wseed05, Wseed12)
Wgame4  = Game (Wseed04, Wseed13)

Wgame5  = Game (Wseed06, Wseed11)
Wgame6  = Game (Wseed03, Wseed14)
Wgame7  = Game (Wseed07, Wseed10)
Wgame8  = Game (Wseed02, Wseed15)

print("West Region")
print()
print(Wgame1.findWin())
print(Wgame2.findWin())
print(Wgame3.findWin())
print(Wgame4.findWin())
print(Wgame5.findWin())
print(Wgame6.findWin())
print(Wgame7.findWin())
print(Wgame8.findWin())
print() 

Wgame9  = Game (Wseed01, Wseed09)
Wgame10 = Game (Wseed04, Wseed12)
Wgame11 = Game (Wseed03, Wseed06)
Wgame12 = Game (Wseed02, Wseed10)

print(Wgame9.findWin())
print(Wgame10.findWin())
print(Wgame11.findWin())
print(Wgame12.findWin())
print()

Wgame13 = Game (Wseed01, Wseed04)
Wgame14 = Game (Wseed02, Wseed03)

print(Wgame13.findWin())
print(Wgame14.findWin())
print()

Wgame15 = Game (Wseed01, Wseed03)
print(Wgame15.findWin())
print()
print()
print()
