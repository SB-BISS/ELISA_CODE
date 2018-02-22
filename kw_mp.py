import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
stop_words = stopwords.words('english') + list(string.punctuation)

def removeStopwords(wordlist, stopwords):
  return [w for w in wordlist if w not in stopwords]

def kw_mp_helper(sentence, kw):
    tmp1 = list( set(sentence) & set(kw) )
    tmp2 = len(tmp1)
    return {'key_words': tmp1, 'length': tmp2}

def kw_mp(x, kw):
    tmpp2 = {}
    for i in range(len(x["fragments"])):
       tmpp = removeStopwords( word_tokenize(x["fragments"][i]["lines"].__str__().lower()), stop_words )
       tmpp= kw_mp_helper(tmpp, kw)
       tmpp2[i]= tmpp
    return tmpp2

filee= json.load(open('btq112.json'))
key_words= ["finance", "year"]
tmpp= kw_mp(filee, key_words)
print(tmpp)