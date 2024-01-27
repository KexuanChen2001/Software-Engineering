"""
# 2022.5.1 - class: PopularPoster
"""
from Poster import Poster


class PopularPoster(Poster):

    def __init__(self, author, email, abstract, programmeName):
        super(PopularPoster, self)
        # no more attributes

    def displayPopularPoster(self, posterID):
        pass
        print('posterID: ' + str(self.__posterID) + ' author: ' + self.__author \
              + ' email: ' + self.__email + ' abstract: ' + self.__abstract + \
              ' programmeName: ' + self.__programmeName)
