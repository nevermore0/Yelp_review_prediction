import re
import os
import sys
from Porterstemmer import PorterStemmer
from math import log

def readFile(path):
    s = []
    files = os.listdir(path)
    for filepath in files:
        fullname = path + filepath
        f = open(fullname, 'r')
        s.append(f.read())
        f.close()
    return s

def removeSGML(raw_text):
    SGML = re.compile('<.*?>')
    ret_text = re.sub(SGML, '', raw_text)
    return ret_text

def tokenizeText(raw_text):
    raw_tokens = raw_text.split()

    result = []

    period_list = [
            'I.O.U.',
            'M.D.',
            'N.B.',
            'P.O.',
            'U.K.',
            'U.S.',
            'U.S.A.',
            'P.S.',
            '.c',
            'mr.',
            'mrs.',
            '.com',
            'dr.',
            '.sh',
            '.java',
            'st.',
            'j.',
            'ae.',
            'scs.'
    ]

    #contracton list:https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
    contraction_list = {
                'amn\'t': 'am not',
                'aren\'t': 'are not',
                'can\'t': 'can not',
                'could\'ve': 'could have',
                'couldn\'t': 'could not',
                'didn\'t': 'did not',
                'doesn\'t': 'does not',
                'don\'t': 'do not',
                'gotta': 'got to',
                'gonna': 'going to',
                'hadn\'t': 'had not',
                'hasn\'t': 'has not',
                'haven\'t': 'have not',
                'he\'d': 'he had',
                'he\'ll': 'he will',
                'he\'s': 'he is',
                'she\'d': 'she had',
                'she\'ll': 'she will',
                'she\'s': 'she is',
                'you\'d': 'you had',
                'you\'ll': 'you will',
                'you\'re': 'you are',
                'you\'ve': 'you have',
                'they\'d': 'they had',
                'they\'ll': 'they will',
                'they\'re': 'they are',
                'they\'ve': 'they have',
                'we\'d': 'we had',
                'we\'ll': 'we will',
                'we\'re': 'we are',
                'we\'ve': 'we have',
                'who\'d': 'who had',
                'who\'ll': 'who will',
                'who\'re': 'who are',
                'who\'ve': 'who have',
                'that\'d': 'that had',
                'that\'ll': 'that will',
                'that\'re': 'that are',
                'that\'s': 'that is',
                'what\'d': 'what did',
                'what\'ll': 'what will',
                'what\'re': 'what are',
                'what\'s': 'what is',
                'what\'ve': 'what have',
                'where\'d': 'where did',
                'where\'re': 'where are',
                'where\'s': 'where is',
                'where\'ve': 'where have',
                'when\'s': 'when is',
                'there\'d': 'there had',
                'these\'re': 'these are',
                'there\'re': 'there are',
                'there\'s': 'there is',
                'I\'d': 'I had',
                'I\'ll': 'I will',
                'I\'m': 'I am',
                'I\'ve': 'I have',
                'how\'ll': 'how will',
                'isn\'t': 'is not',
                'it\'d': 'it would',
                'it\'ll': 'it will',
                'it\'s': 'it is',
                'let\'s': 'let us',
                'mayn\'t': 'may not',
                'may\'ve': 'may have',
                'mightn\'t': 'might not',
                'might\'ve': 'might have',
                'mustn\'t': 'must not',
                'must\'ve': 'must have',
                'needn\'t': 'need not',
                'oughtn\'t': 'ought not',
                'shan\'t': 'shall not',
                'shouldn\'t': 'should not',
                'should\'ve': 'should have',
                'weren\'t': 'were not',
                'wasn\'t': 'was not',
                'won\'t': 'will not',
                'would\'ve': 'would have',
                'wouldn\'t': 'would not',
                'why\'re': 'why are',
                'why\'s': 'why is',
                'why\'d': 'why did',
    }

    for token in raw_tokens:
        length = len(token)
        if token.find('.') != -1:
            #do not tokenize acronyms,abbreviations,numbers
            if token in period_list:
                result.append(token)
                continue
            pos = token.find('.')
            if pos < length - 1 and token[pos + 1].isdigit():
                result.append(token)
                continue
            if pos == length - 1 and len(token) < 4 and len(token) > 1:
                result.append(token)
                continue
        if token.find('\'') != -1:
            if token in contraction_list:
                split_token = contraction_list[token]
                split_token.split(' ')
                for word in split_token:
                    result.append(word)
                continue
            pos = token.find('\'')
            if pos == length - 2 and token[length - 1] == 's':
                result.append(token[:pos])
                result.append(token[pos:])
                continue
            else:
                split_token = token.split('\'')
                for word in split_token:
                    result.append(word)
                continue
        if token.find(',') != -1:
            if token.find(',') < length - 1 and token[token.find(',') + 1].isdigit():
                result.append(token)
                continue

        #regex of date https://www.regular-expressions.info/dates.html
        date = re.match('^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$',token)
        if date:
            result.append(token)
            continue
        split_token = re.split('[!;:"\'\[\]()<>,/.]',token)
        for word in split_token:
            if len(word) > 0:
                result.append(word)

    return result

def removeStopwords(raw_text_list):
    restext = []
    stopwords_path = "stopwords"
    stopwords = [line.strip() for line in open(stopwords_path).readlines()]
    for word in raw_text_list:
        if word not in stopwords:
            restext.append(word)
    return restext

def stemWords(raw_text_list):
    p = PorterStemmer()
    ret_text = []
    for token in raw_text_list:
        flag = True
        for c in str(token):
            if not c.isalpha():
                flag = False
        if flag:
            ret_text.append(p.stem(str(token),0,len(str(token))-1))
        else:
            ret_text.append(str(token))
    return ret_text

if __name__ == '__main__':
    numofwords = 0
    Vocabulary = {}
    path = sys.argv[1]
    s = readFile(path)
    for i in range(len(s)):
        doc = s[i].lower()
        doc = removeSGML(doc)
        doc = tokenizeText(doc)
        doc = removeStopwords(doc)
        doc = stemWords(doc)
        for word in doc:
            numofwords += 1
            if word not in Vocabulary:
                Vocabulary[word] = 0
            Vocabulary[word] += 1

    numofvocabulary = len(Vocabulary)

    #Vocabulary = sorted(Vocabulary.iteritems(), key=lambda (k,v): (v,k),reverse=True)

    #beta = log((4716.0/5785),(40776.0/64443))
    #K = 5785/pow(64443,beta)
    #print(beta)
    #print(K)
    #print(K * pow(100000000,beta))
    #i = 0
    #num = 0
    #subsetvoc = {}
    #while i < 600:
    #    doc = s[i].lower()
    #    doc = removeSGML(doc)
    #    doc = tokenizeText(doc)
    #    doc = removeStopwords(doc)
    #    doc = stemWords(doc)
    #    for word in doc:
    #        num += 1
    #        if word not in subsetvoc:
    #            subsetvoc[word] = 0
    #        subsetvoc[word] += 1
    #    i += 1
    #print("num of words:" + str(num))
    #print("num of vocabulary:" + str(len(subsetvoc)))

    #point = numofwords * 0.25
    #i = 0
    #sum = 0
    #while sum < point:
    #    sum += Vocabulary[i][1]
    #   i += 1
    #print(i)
    f = open("preprocess.output", "w")
    f.write("Words " + str(numofwords) + "\n")
    f.write("Vocabulary " + str(numofvocabulary) + "\n")
    f.write("Top 50 Words" + "\n")
    index = 0
    while index < 50:
        f.write(Vocabulary[index][0] + ' ' + str(Vocabulary[index][1]) + "\n")
        index += 1