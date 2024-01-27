from Poster_InternalUse import Poster_InternalUse


class ProgrammeWinnerPoster(Poster_InternalUse):

    def __init__(self, author, email, abstract, programmeName):
        super(ProgrammeWinnerPoster, self)
        # the array of headJudge score
        self.__headJudgesScore = []

    # score By Head Judge
    def scoreByHeadJudge(self, headJudgesScore):
        self.__headJudgesScore.append(headJudgesScore)
        """database"""
        pass

    def calcHeadJudgeAverage(self, judgesScore_array):
        """get from database"""
        # calculation
        m = 0
        sumScore = 0
        for n in judgesScore_array:
            m = m + 1
            sumScore = sumScore + n
        avgScore = sumScore / m
        return avgScore

