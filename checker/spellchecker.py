from . import logger
import nltk
import re
import time
import json
import operator

'''
class spellcheck
String dictionary
Dictionary unigramDict
Dictionary bigramDict
Dictionary lengthDict
'''


class SpellChecker:

    # dictionary path
    __path = 'checker/dictionary.json'

    # unigram dictionary attribute
    __unigramDict = {}

    # bigram dictionary attribute
    __bigramDict = {}

    # dictionary length attribute
    __lengthDict = {}

    # init class and load dictionaries
    def __init__(self):
        logger.info('app intialized')
        self.loadDictionaries()

    '''
    Load dictionary
    # unigram
    # bigram
    # frequency
    '''
    @classmethod
    def loadDictionaries(cls):
        if any(cls.__unigramDict) == False:
            with open(cls.__path, 'r') as f:
                data = json.load(f)
                # assing data to dictionaries
                cls.__unigramDict = data['unigram']
                cls.__bigramDict = data['bigram']
                # json return string key therefore cast key as int()
                for length, words in data['length'].items():
                    cls.__lengthDict[int(length)] = words

            logger.info('dictionary imported with %s words' % len(cls.__unigramDict))

    '''
    Normalize words
    # remove special characters from start and end of word (Come? == come)
    '''

    def normalize(self, word):
        # remove special characters from start and end of word
        return re.sub(r'^\W+|\W+$', '', word.lower())

    '''
    Select candidates
    # select candidates from length dict.
    '''

    def candidates(self, scale):
        candidates = []
        for length in scale:
            if length in self.__lengthDict.keys():
                candidates.extend(self.__lengthDict[length])

        return candidates

    '''
    Calculate candidates search range
    # most of the spelling mistakes are between +- 2 edit distance therefore
    # select search range (word +- 2)
    '''

    def searchRange(self, word):
        return list(range((len(word) - 2), (len(word) + 3)))

    '''
    Return final result
    '''

    def result(self, suggestions):
        result = {}
        for key, value in suggestions.items():
            result[key] = []
            for i, x in enumerate(value):
                if i > 4:  # pick top five results
                    continue
                result[key].append(x['word'])

        return result

    '''
    Apply edit distance and conditional probability
    '''

    def process(self, candidates, word, preWord):
        selected = []
        tmpEd = []  # assign empty array to hold distance calculated words
        logger.info('apply edit distance & apply probability')
        for candidate in candidates:
            ed = SpellChecker.editDistance(word, candidate)
            # accept only edit distance <= 3
            if ed <= 2:
                tmpEd.append({
                    'word': candidate,
                    'ed': ed
                })
                selected = sorted(tmpEd, key=lambda x: x['ed'])
        # apply probability check if suggestions > 1
        if len(selected) > 1 and preWord != "":
            tmpPro = []  # assign empty array to hold probability calculated words
            for item in selected:
                if preWord in self.__bigramDict.keys() and item['word'] in self.__bigramDict[preWord].keys():
                    # count(Wi-1, Wi), count(Wi-1)
                    item['probability'] = SpellChecker.probability(self.__bigramDict[preWord][item['word']], self.__unigramDict[preWord])
                    tmpPro.append(item)

            selected = sorted(tmpPro, key=lambda x: x['probability'], reverse=True)

        return selected

    '''
    Main function
    # loop through text
    '''

    def check(self, text):
        startTime = time.time()
        words = text.split()  # split text into words
        suggestions = {}
        preWord = ''

        # loop through text
        for iteration, phrase in enumerate(words):
            word = self.normalize(phrase)
            # check word present in dictionary - real word
            if word in self.__unigramDict.keys():
                logger.info('checking real word error')

                if (iteration == 0):
                    preWord = word
                    continue  # ignore 1st word no word to compare
                else:
                    # check word exist in bigram
                    if preWord in self.__bigramDict.keys() and word in self.__bigramDict[preWord].keys():
                        preWord = word
                        continue  # word exists in bigram therefore ignore suggestions
                    else:
                        logger.info('word not in bigram %s ' % word)
                        # get candidate search range -+2 length
                        searchRange = self.searchRange(word)
                        print(searchRange)
                        logger.info('looking for candidates in range %s ' % searchRange)

                        candidates = self.candidates(searchRange)
                        if bool(candidates) == False:
                            logger.info('no candidates')
                            preWord = word
                            continue
                        else:
                            suggestions[word] = self.process(candidates, word, preWord)
                            preWord = word
            else:
                logger.info('checking non word error')
                # get candidate search range -+2 length
                searchRange = self.searchRange(word)
                logger.info('looking for candidates in range %s ' % searchRange)
                # pick candidates
                candidates = self.candidates(searchRange)
                if bool(candidates) == False:
                    logger.info('no candidates')
                    preWord = word
                    continue
                else:
                    suggestions[word] = self.process(candidates, word, preWord)
                    preWord = word

        logger.info('executed in %s' % (time.time() - startTime))
        return self.result(suggestions)

    '''
    Levenshtein edit distance implementation by Ben Langmead
    # credit goes to: (Ben Langmead) http://www.cs.jhu.edu/~langmea/resources/lecture_notes/dp_and_edit_dist.pdf
    # delete/insert = 1
    # subsitution = 2
    '''
    @staticmethod
    def editDistance(x, y, cache=None):
        if cache is None:
            cache = {}
        if len(x) == 0:
            return len(y)
        if len(y) == 0:
            return len(x)
        if (len(x), len(y)) in cache:
            return cache[(len(x), len(y))]

        delt = 2 if x[-1] != y[-1] else 0
        diag = SpellChecker.editDistance(x[:-1], y[:-1], cache) + delt
        vert = SpellChecker.editDistance(x[:-1], y, cache) + 1
        horz = SpellChecker.editDistance(x, y[:-1], cache) + 1

        distance = min(diag, vert, horz)
        cache[(len(x), len(y))] = distance

        return distance

    '''
    Calculate conditional probability to find maximum likelihood
    # P(Wi|Wi-1) = count(Wi-1, Wi)/count(Wi-1)
    '''
    @staticmethod
    def probability(x, y):
        return x / y
