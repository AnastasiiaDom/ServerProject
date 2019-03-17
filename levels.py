MAX_RESULT_COUNT = 15

class Levels(object):

    LevelsTable = [[] for i in range(10)]

    def sortResults(self, arr):
        return sorted(arr, key=lambda k: k['score'], reverse=True) 

    def saveResult(self, level, result):
        key = level - 1
        resultsCount = len(self.LevelsTable[key])

        if resultsCount < MAX_RESULT_COUNT:
            self.LevelsTable[key].append(result)
        elif resultsCount >= MAX_RESULT_COUNT and self.LevelsTable[key][resultsCount - 1]['score'] < result['score']:
            self.LevelsTable[key][resultsCount - 1] = result
        else:
            print('Your result is too low' , flush=True)

        self.LevelsTable[key] = self.sortResults(self.LevelsTable[key])

