# -*- coding: utf-8 -*-
"""TPSMedia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RS-4P3uJ9zeRLbdKsBNT4D1gaFTpBjRF

# Imports, downloads, etc.
"""

import requests
import nltk
from bs4 import BeautifulSoup

"""# Creating the dataframe from csv"""

import pandas as pd
#pd.set_option('display.max_colwidth', none)
url_file = 'https://raw.githubusercontent.com/MarissaFosse/ryersoncapstone/master/DailyNewsArticlesCSV.csv'

tstar_articles = pd.read_csv(url_file, header=0, usecols=["Date", "Category", "Publisher", "Heading", "URL"]) 

#tstar_articles.describe()
tstar_articles.head(90)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

plt.figure(figsize=(10,4))
tstar_articles.Category.value_counts().plot(kind='bar')

"""The categories are not well balanced. Thus, my classification algorithm will be designed to only predict Violent Crime and Community Policing & Demographics. Perhaps Traffic if I normalize the data.

# Creating a list of the tokenized/lemmatized words from each artile and appending it to the dataframe
"""

url_to_sents = {}

for url in tstar_articles['URL']:
    response = requests.get(url)
    bsoup = BeautifulSoup(response.content.decode('utf8'))
    if bsoup.find(class_='c-article-body__content'):
      article_sents = ' '.join([p.text for p in bsoup.find(class_='c-article-body__content').find_all('p')])
    url_to_sents[url] = article_sents

#url_to_sents

"""Append the extracted text to the tstar_articles dataframe."""

urls, texts = zip(*url_to_sents.items())
data = {'urls':urls, 'text':texts}
df1 = pd.DataFrame.from_dict(data)

tstar_articles['raw text'] = df1['text']
tstar_articles.head()

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
import random
from string import punctuation

"""For stop words, I used both the NLTK English stopwords, the stopwords-json from https://github.com/6/stopwords-json, and I created my own list specific to law enforcement."""

stopwords_nltk = set(stopwords.words('english')) | set(punctuation)
stopwords_json = {"en":["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]}
stopwords_police = ["a.m.","p.m.","near","“","”","’","police","officer","toronto","say","also","year"]
stoplist_combined = set.union(stopwords_nltk, stopwords_json, stopwords_police)

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')

wnl = WordNetLemmatizer()

def penn2morphy(penntag):
  morphy_tag = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'}
  try:
    return morphy_tag[penntag[:2]]
  except:
    return 'n'

def lemmatize_sent(text):
  return [wnl.lemmatize(word.lower(), pos=penn2morphy(tag)) for word, tag in pos_tag(word_tokenize(text))]

def preprocess_text(text):
  return [word for word in lemmatize_sent(text) if word not in stoplist_combined and not word.isdigit()]

tstar_articles['Cleaned_Tokens'] = tstar_articles['raw text'].apply(preprocess_text)

tstar_articles.head(20)

tstar_articles['raw text'].apply(lambda x: len(x.split(' '))).sum()

tstar_articles['Cleaned_Tokens'].apply(lambda x: len(x.split(' '))).sum()

"""Testing various sets of cleaned_tokens to see which words should be stopped, and see what the data looks like."""

freq = nltk.FreqDist(tstar_articles.iloc[6,6])
for key,val in freq.items():
  print(str(key) + ':' + str(val))

freq.plot(20, cumulative=False)

"""# Vectorization"""

from collections import Counter

sent1 = tstar_articles.iloc[0,6]
sent2 = tstar_articles.iloc[1,6]

print(Counter(sent1))
print(Counter(sent2))

from io import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

vectorizer = CountVectorizer()
vectorizer.fit(sent1)
print(vectorizer.vocabulary_)
vector = vectorizer.transform(sent1)
#print(vector)
print(vector.shape)
print(type(vector))
print(vector.toarray())

"""# TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
tfidf.fit(sent1)
print(tfidf.vocabulary_)
print(tfidf.idf_)
vector = tfidf.transform([sent1[0]])
print(vector.shape)
print(vector.toarray())

"""# Word2Vec

# Trying Naive Bayes Classifier
"""

mf_categories = ['Violent Crime','Community Policing & Demographics','Traffic','Other']

x = tstar_articles.Cleaned_Tokens
y = tstar_articles.Category

x_train, x_test, y_train, y_test = train_test_split(x, y, testsize=0.2)

# Commented out IPython magic to ensure Python compatibility.
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfTransformer
# 
# nb = Pipeline(['vect', CountVectorizer(),
#                'tfidf', TfidfTransformer(),
#                'clf', MultinomialNB()])
# nb.fit(x_train, y_train)
# 
# %%time
# 
# from sklearn.metrics import classification_report
# 
# y_pred = nb.predict(x_text)
# 
# print('accuracy %s' % accuracy_score(y_pred, y_test))
# print(classification_report(y_test, y_pred, target_names=mf_categories))

train, valid = train_test_split(tstar_articles, test_size=0.2)

count_vect = CountVectorizer(analyzer=preprocess_text)

train_set = count_vect.fit_transform(train['raw text'])
train_tags = train['Category']

valid_set = count_vect.transform(valid['raw text'])
valid_tags = valid['Category']

#test_set = count_vect.transform(df_test['request_text_edit_aware'])

training_set = featuresets[:1900] #up to but not including 1900'th review
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)