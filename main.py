import json
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from preprocess import tokenizeText
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

def balance_classes(xs, ys):
    freqs = Counter(ys)

    # the least common class is the maximum number we want for all classes
    max_allowable = freqs.most_common()[-1][1]
    num_added = {clss: 0 for clss in freqs.keys()}
    new_ys = []
    new_xs = []
    for i, y in enumerate(ys):
        if num_added[y] < max_allowable:
            new_ys.append(y)
            new_xs.append(xs[i])
            num_added[y] += 1
    return new_xs, new_ys

if __name__ == '__main__':
    print(datetime.datetime.now())
    # read the data from disk and split into lines
    # we use .strip() to remove the final (empty) line
    reviews = []
    with open("review.json") as f:
        for line in f:
            reviews.append(line.strip())

    # each line of the file is a separate JSON object
    reviews = [json.loads(review) for review in reviews]

    # we're interested in the text of each review
    # and the stars rating, so we load these into
    # separate lists
    print(len(reviews))
    texts = []
    stars = []
    stemmer = PorterStemmer()
    for i in range(0,1000000):
        original_text = reviews[i]['text']
        #print(original_text)
        s = tokenizeText(original_text)
        new_s = []
        for word in s:
            if word not in stopwords.words('english'):
                new_s.append(word)
        s = new_s
        new_s = []
        for word in s:
            new_s.append(stemmer.stem(word))
        new_text = ' '.join(new_s)
        #print(new_text)
        texts.append(new_text)
        stars.append(reviews[i]['stars'])
    #texts = [review['text'] for review in reviews]
    #stars = [review['stars'] for review in reviews]
    print(len(texts))
    balanced_x, balanced_y = balance_classes(texts, stars)
    print(len(balanced_x))
    # This vectorizer breaks text into single words and bi-grams
    # and then calculates the TF-IDF representation
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    t1 = datetime.datetime.now()

    # the 'fit' builds up the vocabulary from all the reviews
    # while the 'transform' step turns each indivdual text into
    # a matrix of numbers.
    vectors = vectorizer.fit_transform(texts)
    print(vectors.shape)
    print(datetime.datetime.now() - t1)

    X_train, X_test, y_train, y_test = train_test_split(vectors, stars, test_size=0.33, random_state=42)


    # initialise the SVM classifier
    classifier = LinearSVC()

    # train the classifier
    t1 = datetime.datetime.now()
    classifier.fit(X_train, y_train)
    print(datetime.datetime.now() - t1)

    preds = classifier.predict(X_test)
    print(list(preds[:10]))
    print(y_test[:10])

    preds = classifier.predict(X_test)

    print(accuracy_score(y_test, preds))

