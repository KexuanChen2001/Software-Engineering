"""
# 2022.5.1 - class: DivisionWinnerPoster
"""
from ProgrammeWinnerPoster import ProgrammeWinnerPoster


class DivisionWinnerPoster(ProgrammeWinnerPoster):

    def __init__(self, author, email, abstract, programmeName):
        super(DivisionWinnerPoster, self)
        # no new attributes

    def displayDivisionWinnerPoster(self, posterID):
        # get information from the database according to the posterID
        # we ignore this in this week
        pass
        print('posterID: ' + str(self.__posterID) + ' author: ' + self.__author \
              + ' email: ' + self.__email + ' abstract: ' + self.__abstract + \
              ' programmeName: ' + self.__programmeName)
