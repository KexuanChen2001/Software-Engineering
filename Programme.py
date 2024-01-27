from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# import os, cv2
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from werkzeug.datastructures import FileStorage
import string
import random


class Programme:

    def __init__(self, name):
        Programme.__name = name

    def showProgramme(self):
        print('Programme: ' + Programme.name)

    def calAverage(self):
        pass
        # we use a better method in poster class when programming
