from Dice import *

class Configuration:
    configs = ["Category", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Upper Scores", "Upper Bonus(35)", "Three of a kind", "Four of a kind",
            "Full House(25)", "Small Straight(30)", "Large Straight(40)",
            "Yahtzee(50)", "Chance", "Lower Scores", "Total"]

    def getConfigs(void):   # 정적 메소드: 객체생성 없이 사용 가능
        return Configuration.configs

    def score(row, d):      # 정적 메소드: 객체생성 없이 사용 가능
        # row에 따라 주사위 점수를 계산 반환. 예를 들어, row가 0이면 "Ones"가 채점되어야 함을
        # 의미합니다. row가 2이면, "Threes"가 득점되어야 함을 의미합니다. row가 득점 (scored)하지
        # 않아야 하는 버튼 (즉, UpperScore, UpperBonus, LowerScore, Total 등)을 나타내는 경우
        # -1을 반환합니다.

        if row >= 0 and row <= 5:
            return Configuration.scoreUpper(d, row+1)
        elif row == 8:
            return Configuration.scoreThreeOfAKind(d)
        elif row == 9:
            return Configuration.scoreFourOfAKind(d)
        elif row == 10:
            return Configuration.scoreFullHouse(d)
        elif row == 11:
            return Configuration.scoreSmallStraight(d)
        elif row == 12:
            return Configuration.scoreLargeStraight(d)
        elif row == 13:
            return Configuration.scoreYahtzee(d)
        elif row == 14:
            return Configuration.scoreChance(d)

    def scoreUpper(d, num):  # 정적 메소드: 객체생성 없이 사용 가능 (Ones에서 ~ Sixes까지 점수)
        numList = [i.getRoll() for i in d]
        return numList.count(num)*num

    def scoreThreeOfAKind(d):
        numList = [i.getRoll() for i in d]
        numList.sort()
        if numList.count(numList[0]) == 3 or numList.count(numList[2]) == 3 or numList.count(numList[-1]) == 3:
            return sum(numList)
        return 0

    def scoreFourOfAKind(d):
        numList = [i.getRoll() for i in d]
        numList.sort()
        if numList.count(numList[0]) == 4 or numList.count(numList[-1]) == 4:
            return sum(numList)
        return 0

    def scoreFullHouse(d):
        numList = [i.getRoll() for i in d]
        numList.sort()      # 정렬한 후 개수가 3개, 2개라면
        if (numList.count(numList[0]) == 3 and numList.count(numList[-1]) == 2) or \
                (numList.count(numList[0]) == 2 and numList.count(numList[-1]) == 3):
            return 25
        return 0

    def scoreSmallStraight(d):
        numList = [i.getRoll() for i in d]
        if 1 in numList and 2 in numList and 3 in numList and 4 in numList:
            return 30
        if 2 in numList and 3 in numList and 4 in numList and 5 in numList:
            return 30
        if 3 in numList and 4 in numList and 5 in numList and 6 in numList:
            return 30
        return 0

    def scoreLargeStraight(d):
        numList = [i.getRoll() for i in d]
        if 1 in numList and 2 in numList and 3 in numList and 4 in numList and 5 in numList:
            return 40
        if 2 in numList and 3 in numList and 4 in numList and 5 in numList and 6 in numList:
            return 40
        return 0

    def scoreYahtzee(d):
        numList = [i.getRoll() for i in d]
        numList.sort()
        if numList[0] == numList[-1]:
            return 50
        return 0

    def scoreChance(d):
        numList = [i.getRoll() for i in d]
        return sum(numList)

    def sumDie(d):
        pass