############################################################
######
######         Team Class
######
############################################################

class Team:

    # initialize
    def __init__ (self, school, conference, adjMargin, turnoversPerPossPct, oppTurnoversPerPossPct, 
                    offReboundPct, defReboundPct, fgMade, fgAtt, threeMade, threeAtt, 
                    oppTwoPct, oppThreePct, ftPct, foulsPerPossPct, scoringReturnPct):
        self._school = school
        self._conference = conference
        self._adjMargin = adjMargin
        self._TOPerPossPct = turnoversPerPossPct                           
        self._oppTOPerPossPct = oppTurnoversPerPossPct                   
        self._offRebPct = offReboundPct                 
        self._defRebPct = defReboundPct           
        self._fgMade = fgMade        
        self._fgAtt = fgAtt                 
        self._threeMade = threeMade                                       
        self._threeAtt = threeAtt   
        self._oppTwoPct = oppTwoPct
        self._oppThreePct = oppThreePct                   
        self._freeThrowPct = ftPct                   
        self._foulsPerPoss = foulsPerPossPct        
        self._scoringReturnPct = scoringReturnPct                  

    # simple gets
    def getSchool (self):
        return self._school
    def getConference (self):
        return self._conference
    def getAdjMargin (self):
        return self._adjMargin
    def getTOPerPossPct (self):
        adjustedPct = self._TOPerPossPct - self.getConfAdj()
        return adjustedPct
    def getOppTOPerPossPct (self):
        adjustedPct = self._oppTOPerPossPct + self.getConfAdj()
        return adjustedPct
    def getOffRebPct (self):
        adjustedPct = self._offRebPct + self.getConfAdj()
        return adjustedPct
    def getDefRebPct (self):
        adjustedPct = self._defRebPct + self.getConfAdj()
        return adjustedPct
    def getFgMade (self):
        return self._fgMade
    def getFgAtt (self):
        return self._fgAtt
    def getThreeMade (self):
        return self._threeMade
    def getThreeAtt (self):
        return self._threeAtt
    def getOppTwoPct (self):
        adjustedPct = self._oppTwoPct - self.getConfAdj()
        return adjustedPct
    def getOppThreePct (self):
        adjustedPct = self._oppThreePct - self.getConfAdj()
        return adjustedPct
    def getFoulsPerPoss (self):
        adjustedPct = self._foulsPerPoss - self.getConfAdj()
        return adjustedPct
    def getScoringPctReturn (self):
        return self._scoringReturnPct

    # get percentages / rates
    def getFtPct (self):
        return self._freeThrowPct

    def getTwoPct (self):
        fgMade = self.getFgMade()
        fgAttempted = self.getFgAtt()
        threesMade = self.getThreeMade()
        threesAttempted = self.getThreeAtt()
        
        twosMade = fgMade - threesMade
        twosAttempted = fgAttempted - threesAttempted
        twoPct = twosMade / twosAttempted
        twoAdj = (twoPct + self.getConfAdj()) * 100
        return twoAdj

    def getThreePct (self):
        threePct = self.getThreeMade() / self.getThreeMade()
        threeAdj = (threePct + self.getConfAdj()) * 100
        return threeAdj

    def getTwoRate (self):
        twosAtt = self.getFgAtt() - self.getThreeAtt()
        fgAtt = self.getFgAtt()
        twoRate = twosAtt / fgAtt
        return twoRate

    def getThreeRate (self):
        threesAtt = self.getThreeAtt()
        fgAtt = self.getFgAtt()
        threeRate = threesAtt / fgAtt
        return threeRate

    # dictionary of conferences and adjustments based on strength of each relative to MEC
    conferenceAdjuster = {"B12"      : 0.42, 
                          "ACC"      : 0.38, 
                          "B10"      : 0.38,
                          "SEC"      : 0.38, 
                          "Big East" : 0.37,
                          "AAC"      : 0.33,
                          "P12"      : 0.29,
                          "WCC"      : 0.29,
                          "MAC"      : 0.29,
                          "Ivy"      : 0.26,
                          "Southern" : 0.23,
                          "A10"      : 0.23,
                          "CUSA"     : 0.22,
                          "MVC"      : 0.22,
                          "WAC"      : 0.21,
                          "MWC"      : 0.21,
                          "Sun Belt" : 0.20,
                          "CAA"      : 0.20,
                          "Patriot"  : 0.19,
                          "OVC"      : 0.16,
                          "ASUN"     : 0.14,
                          "Horizon"  : 0.14,
                          "Big Sky"  : 0.13,
                          "Big West" : 0.13,
                          "AEC"      : 0.12,
                          "Big South": 0.12,
                          "Summit"   : 0.12,
                          "Northeast": 0.11,
                          "MAAC"     : 0.10,
                          "Southland": 0.08,
                          "SAC"      : 0.01,
                          "MEC"      : 0.00}

    def getConfAdj (self):
        conference = self.getConference()
        adjust = (self.conferenceAdjuster[conference]) * 2
        return adjust
    

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
        TOPctOne = self._teamOne.getTOPerPossPct()
        TOPctTwo = self._teamTwo.getTOPerPossPct()
        oppTOPctOne = self._teamOne.getOppTOPerPossPct()
        oppTOPctTwo = self._teamTwo.getOppTOPerPossPct()

        winner = ""
        canDetermine = False
        thresholdGap = 3

        turnoverOne = (TOPctOne + oppTOPctTwo) / 2 
        turnoverTwo = (TOPctTwo + oppTOPctOne) / 2   
        turnoverDiff = turnoverOne - turnoverTwo
        absDiff = abs(turnoverDiff)

        if (absDiff >= thresholdGap):
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
        offPctOne = self._teamOne.getOffRebPct()
        offPctTwo = self._teamTwo.getOffRebPct()
        defPctOne = self._teamOne.getDefRebPct()
        defPctTwo = self._teamTwo.getDefRebPct()

        offRebMargin = offPctOne - offPctTwo
        defRebMargin = defPctOne - defPctTwo
        totRebMargin = offRebMargin + defRebMargin
        absMargin = abs(totRebMargin)

        winner = ""
        canDetermine = False
        thresholdGap = 10

        if (absMargin >= thresholdGap):
            if (totRebMargin > 0 and offPctOne > 27):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (totRebMargin < 0 and offPctTwo > 27):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine

    # determine if there is a great advantage in three point shooting
    def threeDifferential (self):
        threePctOne = self._teamOne.getThreePct()
        threePctTwo = self._teamTwo.getThreePct()
        threeRateOne = self._teamOne.getThreeRate()
        threeRateTwo = self._teamTwo.getThreeRate()
        oppThreePctOne = self._teamOne.getOppThreePct()
        oppThreePctTwo = self._teamTwo.getOppThreePct()

        combinedThreePctOne = (threePctOne + oppThreePctTwo) / 2
        combinedThreePctTwo = (threePctTwo + oppThreePctOne) / 2

        threesOne = combinedThreePctOne * threeRateOne
        threesTwo = combinedThreePctTwo * threeRateTwo

        threeDiff = threesOne - threesTwo
        absDiff = abs(threeDiff)

        winner = ""
        canDetermine = False
        thresholdGap = 8

        if (absDiff >= thresholdGap):
            if (threeDiff > 0 and threeRateOne >= 0.4):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (threeDiff < 0 and threeRateTwo >= 0.4):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine     

    # determine if there is a great advantage in three point shooting
    def twoDifferential (self):  
        twoPctOne = self._teamOne.getTwoPct()
        twoPctTwo = self._teamTwo.getTwoPct()
        twoRateOne = self._teamOne.getTwoRate()
        twoRateTwo = self._teamTwo.getTwoRate()
        oppTwoPctOne = self._teamOne.getOppTwoPct()
        oppTwoPctTwo = self._teamTwo.getOppTwoPct()

        combinedThreePctOne = (twoPctOne + oppTwoPctTwo) / 2
        combinedThreePctTwo = (twoPctTwo + oppTwoPctOne) / 2

        twosOne = combinedThreePctOne * twoRateOne
        twosTwo = combinedThreePctTwo * twoRateTwo

        twoDiff = twosOne - twosTwo
        absDiff = abs(twoDiff)

        winner = ""
        canDetermine = False
        thresholdGap = 5

        if (absDiff >= thresholdGap):
            if (twoDiff > 0 and twoRateOne >= 0.6):
                canDetermine = True
                winner = self._teamOne.getSchool()
            elif (twoDiff < 0 and twoRateTwo >= 0.6):
                canDetermine = True
                winner = self._teamTwo.getSchool()

        if (canDetermine == True):
            self.setWinner(winner)

        return canDetermine     

    # finally determine free throw advantages
    def freeThrows (self):
        ftPctOne = self._teamOne.getFtPct()
        ftPctTwo = self._teamTwo.getFtPct()
        foulsOne = self._teamOne.getFoulsPerPoss()
        foulsTwo = self._teamTwo.getFoulsPerPoss()

        ftOne = ftPctOne * foulsTwo
        ftTwo = ftPctTwo * foulsOne

        ftDiff = abs(ftOne - ftTwo)

        winner = ""
        howWin = ""

        if (ftDiff <= 150):
            expOne = self._teamOne.getScoringPctReturn()
            expTwo = self._teamTwo.getScoringPctReturn()
            adjOne = ftOne * expOne
            adjTwo = ftTwo * expTwo
            howWin = "experience"

            if (adjOne > adjTwo):
                winner = self._teamOne.getSchool()
            else:
                winner = self._teamTwo.getSchool()

        else:
            howWin = "free throws"
            if (ftOne > ftTwo):
                winner = self._teamOne.getSchool()
            else:
                winner = self._teamTwo.getSchool()
        
        self.setWinner(winner)
        return howWin

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
                    howWin = "rebounds"
                else:
                    if (self.threeDifferential() == True):
                        howWin = "threes"
                    else:
                        if (self.twoDifferential() == True):
                            howWin = "twos"
                        else:
                            howWin = self.freeThrows()

        result = ("Winner -> " + self.getWinner() + " via " + howWin)
        return result


############################################################
######
######         play out games from 2018-2019 March Madness
######
############################################################

########################################
######         East Region  ->  13 / 15
########################################

# name, effMargin, TO/poss, OTO/poss, ORB%, DRB%, FGM, FGA, 3PM, 3PA, o2%, o3%, FT%, foulsPerPossPct, scoring %
Eseed01 = Team ("Duke"       , "ACC", 19.36, 17.2, 19.0, 34.9, 73.1, 1157, 2418, 278, 903, 45.0, 29.9, 68.6, 20.9, 13.8)
Eseed16 = Team ("N Dakota St", "MVC", 0.56 , 15.5, 14.2, 18.8, 76.7, 874 , 1926, 332, 910, 52.6, 37.0, 76.8, 22.2, 53.4)

Eseed08 = Team ("VCU", "A10", 13.00, 19.4, 22.7, 29.7, 73.1, 820, 1872, 235, 771, 43.8, 28.5, 70.1, 27.6, 51.9)
Eseed09 = Team ("UCF", "AAC", 7.31 , 17.2, 17.5, 27.9, 72.8, 819, 1763, 229, 628, 44.5, 31.3, 64.9, 24.2, 70.9)

Eseed05 = Team ("Mississippi St", "SEC" , 11.89, 18.8, 19.1, 33.3, 72.3, 936, 1982, 292, 774, 48.4, 35.7, 71.7, 24.5, 87.3)
Eseed12 = Team ("Liberty"       , "ASUN", 6.94 , 16.8, 20.0, 22.6, 76.7, 963, 1977, 322, 873, 48.3, 33.3, 78.2, 23.4, 78.9)

Eseed04 = Team ("Virginia Tech", "ACC", 17.80, 17.0, 21.2, 27.3, 74.1, 893, 1900, 327, 831, 49.0, 32.7, 76.1, 23.0, 67.4)
Eseed13 = Team ("Saint Louis"  , "A10", 18.13, 18.8, 18.9, 34.7, 77.3, 855, 2052, 205, 675, 46.7, 31.4, 59.8, 25.7, 58.0)

Eseed06 = Team ("Maryland", "B10", 15.76, 18.9, 13.8, 32.2, 76.9, 858 , 1909, 247, 707, 44.7, 31.9, 74.3, 22.8, 52.2)
Eseed11 = Team ("Belmont" , "OVC", 7.14 , 15.0, 15.8, 23.7, 76.4, 1042, 2094, 343, 922, 47.2, 34.4, 73.5, 20.5, 51.7)

Eseed03 = Team ("LSU" , "SEC", 19.91, 17.5, 19.7, 36.0, 71.9, 988, 2162, 236, 740, 49.4, 33.7, 75.2, 24.6, 44.3)
Eseed14 = Team ("Yale", "Ivy", 6.81 , 17.5, 14.9, 24.7, 77.4, 893, 1812, 230, 634, 47.8, 31.0, 73.5, 22.7,91.9)

Eseed07 = Team ("Louisville", "ACC", 18.18, 17.1, 15.8, 26.9, 76.4, 854, 1967, 294, 860, 46.0, 32.0, 77.7, 24.5, 39.5)
Eseed10 = Team ("Minnesota" , "B10", 19.75, 16.6, 16.4, 28.5, 74.0, 887, 2039, 191, 603, 48.7, 34.0, 68.2, 23.0, 59.3)

Eseed02 = Team ("Michigan St", "B10", 16.52, 18.0, 14.6, 32.5, 77.1, 1071, 2230, 319, 844, 41.9, 31.6, 75.3, 23.7, 59.4)
Eseed15 = Team ("Bradley"    , "MVC", 6.98 , 18.5, 18.1, 25.4, 75.2, 812 , 1874, 240, 653, 46.5, 32.8, 69.1, 26.3, 76.6)

Egame1  = Game (Eseed01, Eseed16)
Egame2  = Game (Eseed08, Eseed09)
Egame3  = Game (Eseed05, Eseed12)
Egame4  = Game (Eseed04, Eseed13)
Egame5  = Game (Eseed06, Eseed11)
Egame6  = Game (Eseed03, Eseed14)
Egame7  = Game (Eseed07, Eseed10)
Egame8  = Game (Eseed02, Eseed15)

print("East Region")
print()
print(Egame1.findWin())
print(Egame2.findWin())
print(Egame3.findWin())
print(Egame4.findWin())
print(Egame5.findWin())
print(Egame6.findWin())
print(Egame7.findWin())
print(Egame8.findWin())
print() 

Egame9  = Game (Eseed01, Eseed09)
Egame10 = Game (Eseed04, Eseed12)
Egame11 = Game (Eseed03, Eseed06)
Egame12 = Game (Eseed02, Eseed10)

print(Egame9.findWin())
print(Egame10.findWin())
print(Egame11.findWin())
print(Egame12.findWin())
print()

Egame13 = Game (Eseed01, Eseed04)
Egame14 = Game (Eseed02, Eseed03)

print(Egame13.findWin())
print(Egame14.findWin())
print()

Egame15 = Game (Eseed01, Eseed02)
print(Egame15.findWin())
print()
print()
print()

########################################
######         West Region  ->  15 / 15
########################################

# name, conf, effMargin, TO/poss, OTO/poss, ORB%, DRB%, FGM, FGA, 3PM, 3PA, o2%, o3%, FT%, foulsPerPoss, exp
Wseed01 = Team ("Gonzaga"            , "WCC"      , 32.85, 14.5, 19.8, 30.0, 77.0, 1177, 2239, 287, 790, 43.4, 30.4, 76.1, 22.3, 68.7)
Wseed16 = Team ("Fairleigh Dickinson", "Northeast", -4.22, 19.3, 18.2, 26.9, 68.7, 921 , 1939, 269, 672, 51.3, 35.3, 72.5, 23.3, 74.4)

Wseed08 = Team ("Syracuse", "ACC", 15.13, 19.2, 20.4, 28.3, 69.2, 808, 1907, 274, 824, 46.9, 32.9, 68.5, 25.0, 93.7)
Wseed09 = Team ("Baylor"  , "B12", 16.48, 17.9, 26.4, 36.4, 72.9, 869, 1966, 274, 803, 47.5, 34.5, 67.7, 27.4, 28.3)

Wseed05 = Team ("Marquette"   , "Big East", 16.52, 18.8, 15.3, 26.9, 76.7, 893, 1969, 319, 822, 45.1, 32.4, 75.7, 25.5, 71.4)
Wseed12 = Team ("Murray State", "OVC"     , 13.83, 17.0, 20.5, 30.9, 71.8, 988, 2007, 258, 731, 48.3, 28.9, 73.3, 21.9, 37.2)

Wseed04 = Team ("Florida St", "ACC", 22.39, 18.5, 20.5, 31.9, 76.9, 960, 2171, 272, 819, 45.3, 33.5, 74.4, 26.5, 70.9)
Wseed13 = Team ("Vermont"   , "AEC", 8.86 , 16.5, 20.4, 25.7, 80.0, 864, 1887, 273, 761, 46.3, 35.1, 74.8, 25.0, 41.5)

Wseed06 = Team ("Buffalo"   , "MAC", 19.85, 15.7, 16.3, 30.6, 74.8, 1083, 2344, 344, 1022, 49.3, 29.3, 68.7, 24.3, 81.3)
Wseed11 = Team ("Arizona St", "P12", 11.55, 18.2, 21.9, 29.6, 76.1, 899 , 2012, 240, 714 , 47.3, 33.4, 68.0, 26.3, 42.3)

Wseed03 = Team ("Texas Tech", "B12"    , 30.03, 17.4, 25.4, 26.3, 74.2, 990, 2110, 277, 759, 41.9, 29.8, 73.2, 25.2, 32.6)
Wseed14 = Team ("N Kentucky", "Horizon", 7.14 , 17.4, 20.7, 28.3, 76.8, 979, 2047, 306, 844, 49.9, 32.0, 66.6, 26.6, 45.0)

Wseed07 = Team ("Nevada" , "MWC", 18.18, 14.3, 17.9, 25.7, 78.4, 924, 1999, 297, 855, 46.2, 33.3, 70.8, 23.7, 60.3)
Wseed10 = Team ("Florida", "SEC", 18.30, 17.4, 20.9, 29.1, 69.9, 857, 2015, 291, 872, 48.5, 31.6, 72.1, 25.4, 64.8)

Wseed02 = Team ("Michigan", "B10"    , 28.32, 13.5, 14.7, 21.9, 77.4, 941, 2102, 287, 839, 44.3, 29.1, 70.1, 20.9, 47.1)
Wseed15 = Team ("Montana" , "Big Sky", 3.53 , 17.0, 18.3, 24.2, 76.9, 975, 1983, 287, 763, 49.3, 34.4, 68.9, 27.4, 85.2)

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


########################################
######         South Region  ->  12 / 15
########################################

# name, effMargin, TO/poss, OTO/poss, ORB%, DRB%, FGM, FGA, 3PM, 3PA, o2%, o3%, FT%, foulsPerPoss, exp
Sseed01 = Team ("Virginia"    , "ACC"      , 34.22, 14.4, 16.1, 28.6, 77.3, 974, 2056, 321, 813, 45.7, 28.9, 74.4, 22.8, 66.7)
Sseed16 = Team ("Gardner Webb", "Big South", -0.04, 16.6, 16.9, 20.0, 71.1, 955, 1962, 281, 719, 50.4, 33.7, 71.1, 22.7, 67.7)

Sseed08 = Team ("Mississippi", "SEC", 13.98, 17.7, 24.5, 27.7, 72.3, 876, 1906, 272, 760, 48.2, 37.4, 78.3, 25.6, 60.5)
Sseed09 = Team ("Oklahoma"   , "B12", 16.94, 16.6, 19.3, 23.3, 73.9, 883, 1975, 226, 654, 45.8, 33.3, 69.7, 21.7, 47.1)

Sseed05 = Team ("Wisconsin", "B10", 21.94, 14.3, 17.6, 23.1, 76.1, 874, 1945, 633, 1273, 44.1, 31.5, 64.8, 22.3, 94.0)
Sseed12 = Team ("Oregon"   , "P12", 17.86, 17.2, 21.1, 27.9, 74.8, 958, 2126, 663, 1286, 48.8, 29.0, 72.1, 25.9, 48.2)

Sseed04 = Team ("Kansas St", "B12"     , 20.06, 17.1, 19.6, 26.6, 76.1, 806, 1878, 241, 721 , 49.0, 31.4, 66.7, 24.4, 93.2)
Sseed13 = Team ("UC Irvine", "Big West", 9.16 , 17.0, 16.6, 31.6, 76.7, 987, 2159, 735, 1458, 40.7, 33.9, 70.2, 26.4, 94.3)

Sseed06 = Team ("Villanova", "Big East", 17.33, 16.1, 18.7, 29.7, 75.2, 884, 2019, 380, 1081, 49.7, 34.3, 72.8, 24.0, 29.5)
Sseed11 = Team ("St Marys" , "WCC"     , 17.31, 15.9, 16.5, 28.9, 78.7, 899, 1905, 253, 670 , 49.2, 32.1, 74.2, 25.7, 32.4)

Sseed03 = Team ("Purdue"      , "B10" , 26.81, 15.5, 16.3, 33.3, 74.9, 967, 2145, 365, 977, 47.2, 34.2, 71.9, 25.3, 39.8)
Sseed14 = Team ("Old Dominion", "CUSA", 5.45 , 17.3, 20.2, 31.3, 78.6, 823, 2026, 264, 756, 43.5, 32.4, 66.3, 24.7, 50.5)

Sseed07 = Team ("Cincinnati", "AAC", 17.50, 15.6, 18.3, 35.6, 73.1, 872, 2018, 232, 673, 45.1, 35.5, 70.4, 24.0, 49.7)
Sseed10 = Team ("Iowa"      , "B10", 16.02, 16.9, 17.9, 28.2, 71.9, 914, 2006, 285, 782, 53.5, 32.4, 73.9, 22.4, 94.9)

Sseed02 = Team ("Tennessee", "SEC"    , 26.24, 15.5, 24.8, 30.4, 72.5, 1106, 2231, 262, 714, 44.7, 35.4, 75.4, 24.6, 89.8)
Sseed15 = Team ("Colgate"  , "Patriot", 4.60 , 18.9, 17.0, 28.6, 75.4, 955 , 1995, 320, 815, 50.5, 33.9, 74.2, 22.2, 61.3)

Sgame1  = Game (Sseed01, Sseed16)
Sgame2  = Game (Sseed08, Sseed09)
Sgame3  = Game (Sseed05, Sseed12)
Sgame4  = Game (Sseed04, Sseed13)
Sgame5  = Game (Sseed06, Sseed11)
Sgame6  = Game (Sseed03, Sseed14)
Sgame7  = Game (Sseed07, Sseed10)
Sgame8  = Game (Sseed02, Sseed15)

print("South Region")
print()
print(Sgame1.findWin())
print(Sgame2.findWin())
print(Sgame3.findWin())
print(Sgame4.findWin())
print(Sgame5.findWin())
print(Sgame6.findWin())
print(Sgame7.findWin())
print(Sgame8.findWin())
print() 

Sgame9  = Game (Sseed01, Sseed09)
Sgame10 = Game (Sseed12, Sseed13)
Sgame11 = Game (Sseed03, Sseed06)
Sgame12 = Game (Sseed02, Sseed10)

print(Sgame9.findWin())
print(Sgame10.findWin())
print(Sgame11.findWin())
print(Sgame12.findWin())
print()

Sgame13 = Game (Sseed01, Sseed12)
Sgame14 = Game (Sseed02, Sseed03)

print(Sgame13.findWin())
print(Sgame14.findWin())
print()

Sgame15 = Game (Sseed01, Sseed03)
print(Sgame15.findWin())
print()
print()
print()

########################################
######         North Region  ->  9 / 15
########################################

# name, effMargin, TO/poss, OTO/poss, ORB%, DRB%, FGM, FGA, 3PM, 3PA, o2%, o3%, FT%, foulsPerPoss, exp
Nseed01 = Team ("UNC" , "ACC" , 27.69, 16.9, 17.9, 33.6, 78.9, 1118, 2410, 312, 862, 47.9, 33.5, 74.3, 21.9, 64.6)
Nseed16 = Team ("Iona", "MAAC", -2.88, 16.9, 18.2, 22.8, 71.1, 857 , 1897, 297, 845, 50.3, 36.6, 74.5, 23.5, 32.3)

Nseed08 = Team ("Utah St"   , "MWC", 15.41, 17.8, 16.8, 29.7, 81.4, 959, 2038, 274, 772, 42.2, 35.4, 75.0, 25.8, 54.6)
Nseed09 = Team ("Washington", "P12", 14.28, 19.2, 23.6, 26.3, 67.1, 883, 1956, 273, 780, 46.0, 33.4, 69.5, 26.2, 95.9)

Nseed05 = Team ("Auburn"       , "SEC", 25.00, 16.5, 24.0, 30.2, 69.5, 1097, 2439, 454, 1204, 51.4, 34.8, 71.3, 25.9, 64.1)
Nseed12 = Team ("New Mexico St", "WAC", 13.62, 17.6, 18.8, 36.9, 79.3, 962 , 2092, 326, 977 , 48.1, 33.4, 67.6, 26.0, 36.9)

Nseed04 = Team ("Kansas"      , "B12", 21.57, 18.2, 17.5, 28.8, 73.6, 989, 2128, 260, 743, 46.1, 33.5, 70.5, 23.4, 39.5)
Nseed13 = Team ("Northeastern", "CAA", 7.59 , 16.4, 16.5, 21.1, 77.0, 880, 1848, 328, 858, 53.0, 33.7, 75.1, 23.2, 82.0)

Nseed06 = Team ("Iowa St", "B12", 22.09, 15.5, 18.0, 26.5, 72.5, 974, 2047, 294, 811, 47.1, 33.6, 73.2, 21.2, 70.2)
Nseed11 = Team ("Ohio St", "B10", 14.66, 18.3, 17.8, 25.7, 75.8, 839, 1931, 264, 774, 47.9, 32.7, 73.5, 26.1, 38.6)

Nseed03 = Team ("Houston"   , "AAC"     , 24.13, 16.1, 17.7, 33.3, 76.7, 982, 2203, 333, 939, 43.1, 27.8, 70.3, 27.6, 48.9)
Nseed14 = Team ("Georgia St", "Sun Belt", 4.85 , 16.0, 20.5, 21.7, 68.5, 903, 1968, 330, 859, 51.2, 32.8, 65.9, 23.8, 80.2)

Nseed07 = Team ("Wofford"   , "Southern", 20.69, 15.9, 18.9, 31.4, 76.8, 1044, 2132, 385, 929, 50.6, 32.6, 71.0, 25.0, 95.0)
Nseed10 = Team ("Seton Hall", "Big East", 11.50, 17.1, 19.3, 27.8, 73.7, 888 , 2021, 240, 741, 48.7, 34.0, 70.6, 25.8, 33.3)

Nseed02 = Team ("Kentucky"         , "SEC"      , 27.57, 18.3, 17.6, 35.0, 76.4, 978, 2050, 215, 607, 43.6, 34.3, 73.9, 23.5, 31.9)
Nseed15 = Team ("Abilene Christian", "Southland", 1.35 , 17.0, 22.9, 26.0, 73.4, 897, 1911, 251, 660, 49.8, 33.3, 71.9, 27.9, 69.3)

Ngame1  = Game (Nseed01, Nseed16)
Ngame2  = Game (Nseed08, Nseed09)
Ngame3  = Game (Nseed05, Nseed12)
Ngame4  = Game (Nseed04, Nseed13)
Ngame5  = Game (Nseed06, Nseed11)
Ngame6  = Game (Nseed03, Nseed14)
Ngame7  = Game (Nseed07, Nseed10)
Ngame8  = Game (Nseed02, Nseed15)

print("North Region")
print()
print(Ngame1.findWin())
print(Ngame2.findWin())
print(Ngame3.findWin())
print(Ngame4.findWin())
print(Ngame5.findWin())
print(Ngame6.findWin())
print(Ngame7.findWin())
print(Ngame8.findWin())
print() 

Ngame9  = Game (Nseed01, Nseed09)
Ngame10 = Game (Nseed04, Nseed05)
Ngame11 = Game (Nseed03, Nseed11)
Ngame12 = Game (Nseed02, Nseed07)

print(Ngame9.findWin())
print(Ngame10.findWin())
print(Ngame11.findWin())
print(Ngame12.findWin())
print()

Ngame13 = Game (Nseed01, Nseed05)
Ngame14 = Game (Nseed02, Nseed03)

print(Ngame13.findWin())
print(Ngame14.findWin())
print()

Ngame15 = Game (Nseed02, Nseed05)
print(Ngame15.findWin())
print()
