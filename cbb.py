############################################################
######
######         Team Class
######
############################################################

class Team:

    # initialize
    def __init__ (self, school, adjMargin, steals, turnovers, offRebounds, reboundMargin, 
                    fgMade, fgAtt, threeMade, threeAtt, ftPct, fouls, gamesPlayed):
        self._school = school
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
    def getAdjMargin (self):
        return self._adjMargin
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
        turnoversPerGame = self._turnovers / self.getGamesPlayed()
        return turnoversPerGame
    def getReboundMarginPerGame (self):
        reboundMarginPerGame = self._reboundMargin / self.getGamesPlayed()
        return reboundMarginPerGame
    def getTwosPerGame (self):
        twosMade = self.getFgMade() - self.getThreeMade()
        twosPG = twosMade / self.getGamesPlayed()
        return twosPG
    def getThreesPerGame (self):
        threePG = self.getThreeMade() / self.getGamesPlayed()
        return threePG
    def getFoulsPerGame (self):
        foulsPerGame = self._fouls / self.getGamesPlayed()
        return foulsPerGame

    # get percentages
    def getFtPct (self):
        return self._freeThrowPct

    def getOffReboundPct (self):
        fgAttempts = self.getFgAtt()
        fgMade = self.getFgMade()
        missedShots = (fgAttempts - fgMade)
        offPct = (self.getOffRebounds() / missedShots) * 100
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

        if (absDiff >= 2.5):
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

        if (absMarginDiff >= 5):
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

        winner = ""
        canDetermine = False

        if (absDiff >= 3.5):
            if (threeDiff > 0 and threePctOne >= 33):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (threeDiff < 0 and threePctTwo >= 33):
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
        
        winner = ""
        canDetermine = False

        if (absDiff >= 5):
            if (twoDiff > 0 and twoPctOne >= 50):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (twoDiff < 0 and twoPctTwo >= 50):
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
