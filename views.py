from levels import Levels
import uuid
import json

UsersList = {}
levels = Levels()

class LoginView(object):

    def __init__(self, userId, params):
        self.userId = userId
        self.params = params

    def get(self):
        if  self.userId not in UsersList:
            username = str(uuid.uuid4())[0:7]
            UsersList[username] = self.userId
        else:
            print('This user is on DB', flush=True)

        return 'username: ' + username

class ScoreView(object):

    def __init__(self, levelId, params):
        self.level = int(levelId)
        self.params = params

    def post(self, data):
        username = self.params.get('sessionkey')[0]

        if data:
            self.score = data['score']

        if UsersList[username]:
            userResult = {
                'score' : self.score,
                'userId': UsersList[username]
            }
            levels.saveResult(self.level, userResult)
        else:
            print('Such username is not exist',  flush=True)

class HighscorelView(object):

    def __init__(self, levelId, params):
        self.level = int(levelId)
        self.params = params

    def get(self):
        if levels.LevelsTable[self.level - 1]:
            return json.dumps(levels.LevelsTable[self.level - 1])
        else:
           print('There are no results for this level...',  flush=True)  
