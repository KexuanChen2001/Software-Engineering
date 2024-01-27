
from flask import Flask, request, jsonify
from Poster import Poster


class Poster_InternalUse(Poster):
    # create a Flask instance
    app = Flask(__name__)

    def __init__(self, author, email, abstract, programmeName):
        super(Poster_InternalUse, self)
        # the array
        self.__judgesScore = []

    def setScore(self, judgesScore):
        self.__judgesScore.append(judgesScore)
        # update into the database
        # we ignore this in this week
        pass

    def calcAvg(self, judgesScore_array):
        # calculation
        m = 0
        sumScore = 0
        for n in judgesScore_array:
            m = m + 1
            sumScore = sumScore + n
        avgScore = sumScore / m
        return avgScore

    if __name__ == '__main__':
        app.run(debug=True)