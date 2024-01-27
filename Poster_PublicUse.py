from Poster import Poster


class Poster_PublicUse(Poster):

    def __init__(self, author, email, abstract, programmeName):
        super(Poster_PublicUse, self)
        # vote value
        self.__vote = 0

    def increaseVoteCount(self):
        # increase the vote by 1
        self.__vote = self.__vote + 1

    def displayVote(self):
        return self.__vote