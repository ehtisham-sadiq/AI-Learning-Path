import re
import string
import contractions
from cleantext import clean
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
wn = WordNetLemmatizer()

def text_preprocessing(mystr):
    mystr = mystr.lower()                                               # case folding
    mystr = re.sub('\w*\d\w*', '', mystr)                               # remove digits
    mystr = re.sub('\n', ' ', mystr)                                    # replace new line characters with space
    mystr = re.sub('[‘’“”…]', '', mystr)                                # removing double quotes and single quotes
    mystr = re.sub('<.*?>', '', mystr)                                  # removing html tags 
    mystr = re.sub(r'\[.*?\]', '', mystr)                               # remove text in square brackets
    mystr = re.sub('https?://\S+|www.\.\S+', '', mystr)                 # removing URLs
    mystr = re.sub('\n', ' ', mystr)                                    # replace new line characters with space
    mystr = clean(mystr, no_emoji=True)                                 # remove emojis
    mystr = ''.join([c for c in mystr if c not in string.punctuation])  # remove punctuations
    mystr = ' '.join([contractions.fix(word) for word in mystr.split()])# expand contractions
    
    tokens = word_tokenize(mystr)                                       # tokenize the string
    mystr = ''.join([c for c in mystr if c not in string.punctuation])  # remove punctuations
    tokens = [token for token in tokens if token not in stop_words]     # remove stopwords
#   tokens = [ps.stem(token) for token in tokens]                       # stemming
    tokens = [wn.lemmatize(token) for token in tokens]                   # lemmatization
    new_str = ' '.join(tokens)
    return new_str