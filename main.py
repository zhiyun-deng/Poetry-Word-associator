"""
import matplotlib.pyplot as plt
from sklearn  import datasets, svm, neural_network, metrics
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from collections import Counter
def simple_get(url):
    
    #Attempts to get the content at `url` by making an HTTP GET request.
    #If the content-type of response is some kind of HTML/XML, return the
    #text content, otherwise return None.
    
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    
    #Returns True if the response seems to be HTML, False otherwise.
    
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    
    #It is always a good idea to log errors. 
    #This function just prints them, but you can
    #make it do anything.
    
    print(e)
def getrhyme(word):
    resp = get('https://api.datamuse.com/words?rel_rhy='+word)
    data = resp.json()
    return data
def getsynonym(word):
    resp = get('https://api.datamuse.com/words?rel_syn='+word)
    data = resp.json()
    return data
#print(getsynonym("help"))

#word  counted once in a poem
def count(poems):
    count = [None]*len(poems)
    for i in range(len(poems)):
        count[i]=one_poem_counter(poems[i])
    #adding counters together
    overall_count = Counter();
    for counter in count:
        overall_count = overall_count + counter
    return count
#associate words to others. Create a counter for each common word and return a dictionary of these counters
def word_to_others(wordList, poemsCounter):
    counterList = {}
    for word in wordList:
        counter = Counter()
        for poemCounter in poemsCounter:
            if(poemCounter[word])>1:#what do you think about this
                for word, occurrence in poemCounter.most_common(10):
                    counter[word]+=occurrence
        counterList[word] = counter
    return counterList

def parsePoem(raw_poem):
  global stopWords
  poem = str(raw_poem[1]).split('<br/>')
  poem_words = []
  for line in poem:
    for word in line.split(' '):
      lWord = removePunc(word.lower())
      if lWord != '' and lWord not in stopWords and lWord != "--":
        poem_words.append(lWord)
  return poem_words[1:-2]
stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",                  "like", "no", "not", "one", "can", "may", "shall", "us", "let", "yet", "make", "though", "made", "every", "oh", "just", "know", "go"]

punctuation = [",", ".", "/", "\\", "(", ")", "!", "?", ":", ";", "[", "]", "{", "}"]

def parsePoem2(poem):
    poem_words = []
    for word in poem.split(' '):
        lWord = removePunc(word.lower())
        if lWord != '' and lWord not in stopWords and lWord != "--":
            poem_words.append(lWord)
    return poem_words
def removePunc(word):
  global punctuation
  if word == "":
    return ""
  
  x = 0
  while x < len(word):
    if word[x] in punctuation:
      word = word[:x] + word[x+1:]
    else:
      x+=1
  return word
def user_start(poemsList, common_words):
    result_counter = Counter()
    user_input = input("Enter:")
    #we load the poem list. Then, we create ccount(poem list). we load common_words. Then, we call "word_to_others(common_words, )
    #poemsList
    poemsCounter = count(poemsList)
    #common_words
    wordDiction = word_to_others(common_words, poemsCounter)
    wordList = parsePoem2(user_input)
    for word in wordList:
        if(wordDiction.get(word)!=None):
            for suggestion, occurrence in wordDiction.get(word).most_common(5):
                result_counter[suggestion] += occurrence
    return result_counter.most_common()[0]

def get_associated_word(word):
    resp = get('https://similarwords.p.mashape.com/moar?query='+word, headers = {"X-Mashape-Key": "r63BPcKtDHmsho4tWg8EpyDaFtWCp1mRt55jsnD5ZpLdLfNhXS","Accept": "application/json"})
    data = resp.json()
    return data['result']


print(get_associated_word("cat"))
"""
#print(getsynonym('beautiful'))
#user_start()  

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import  csv
import pandas as pd
from tqdm import tqdm
from numba import jit
from collections import Counter

def getrhyme(word):
    resp = get('https://api.datamuse.com/words?rel_rhy='+word)
    data = resp.json()
    return data
def getsynonym(word):
    resp = get('https://api.datamuse.com/words?rel_syn='+word)
    data = resp.json()
    return data
#with more stopWords
stopWords = ["world", "old", "man", "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",                  "like", "no", "not", "one", "can", "may", "shall", "us", "let", "yet", "make", "though", "made", "every", "oh", "just", "know", "go"]

#stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]
poemSource = "https://www.poemhunter.com/p/m/l.asp?a=0&l=top500&order=title&p="
poetSource = "https://www.poemhunter.com/p/t/l.asp?a=0&l=Top500&cinsiyet=&Populer_mi=&Classicmi=&Dogum_Tarihi_yil=&Dogum_Yeri=&p="
punctuation = ["│", "‘", "’", "’", "â", "€", "™", "€", "¦", "©", "«", "»", "…", "\"", "\t", "–", "—", ",", "<", ">", ".", "/", "?", ":", ";", "\\", "|", "[", "]", "{", "}", "+", "=", "-", "_", "(", ")", "*", "&", "^", "%", "$", "#", "@", "!", "~", "`"]

@jit
def removePunc(word):
  global punctuation
  if len(word) <= 2:
    return ""
  
  while "\xa0" in word:
    word = word.replace("\xa0", "")
  while "\t" in word:
    word = word.replace("\t", "")
    
  x = 0
  while x < len(word):
    
    if word[x] in punctuation:
      word = word[:x] + word[x+1:]
    else:
      x+=1
  return word

def getPoems():
  global poemSource
  htmlLinks = []
  for i in tqdm(range(19, 21)):
    website = requestHTML(poemSource + str(i))
    if website is not None:
      links = BeautifulSoup(website, 'html.parser').find_all('td', { 'class' : 'title'})
      links = ['https://www.poemhunter.com' + links[j].find('a', recursive=False)['href'] for j in range(1, len(links))]
      htmlLinks += links
  return htmlLinks
    
def getPoets():
  global poetSource
  htmlLinks = []
  for i in range(11):
    website = requestHTML(poetSource + str(i))
    if website is not None:
      poets = BeautifulSoup(website, 'html.parser').findAll('a', { 'class' : 'photo' })
      poets = ['https://www.poemhunter.com' + poet['href'] + 'poems/' for poet in poets]
      htmlLinks += poets
  return htmlLinks

def getPoemsFromPoets():
  htmlLinks = getPoets()
  poemList = []
  for link in htmlLinks:
    website = requestHTML(link)
    if website is not None:
      poems = BeautifulSoup(website, 'html.parser').findAll('td', { 'class' : 'title' })
      try:
          poems = ['https://www.poemhunter.com' + poem.find('a', recursve=False)['href'] for poem in poems][:25]
          poemList += poems
      except:
          print("NullType while dealing with poet pages!")
  return poemList

def requestHTML(url):
  try:
    with closing(get(url, stream=True)) as resp:
      if resp.status_code == 200 and \
          resp.headers['Content-Type'].lower() is not None and \
          resp.headers['Content-Type'].lower().find('html') > -1:
            return resp.content
      else:
        return None
  except RequestException as e:
    print(e)
    return None

@jit  
def parsePoem(htmlLink):
  global stopWords
  html = requestHTML(htmlLink)
  if html is None:
    return None
  raw_poem = BeautifulSoup(html, 'html.parser').select('p')
  poem = str(raw_poem[1])
  if poem.find('<font color=') != -1:
    return None
  poem = poem.split('<br/>')
  poem_words = []
  for line in poem:
    for word in line.split(' '):
      lWord = removePunc(word.lower())
      if lWord != '' and lWord not in stopWords and lWord.find("&") == -1:
        poem_words.append(lWord)
  return poem_words[1:-2]

  
def parsePoem2(poem): #for user input and csv input
    poem_words = []
    for word in poem.split(' '):
        lWord = removePunc(word.lower())
        if lWord != '' and lWord not in stopWords and lWord != "--":
            poem_words.append(lWord)
    return poem_words
def to_csv2(poem):
  try:
      with open("out3.csv","a") as f:
          wr = csv.writer(f,delimiter=",")    
          wr.writerow(poem)
  except:
      print("could not save poem to csv!")
      
        
@jit
def run():
    links = getPoemsFromPoets()
    #print(links)
    poems = ["derp"]
    print("starting parsing poems")
    for i in tqdm(range(len(links))):
      poem = parsePoem(links[i])
      if poem is not None:
        #poems.append(poem)
        to_csv2(poem)
    
    for i, poem in enumerate(poems):
      print(str(i), poem)
      
    return poems
  

#poems = run()


def to_csv(poems):
  with open("out.csv","w") as f:
      wr = csv.writer(f,delimiter=",")    
      for poem in poems:
        wr.writerow(poem)
def from_csv(file):
    p = []
    with open(file) as f:
      reader = csv.reader(f)
      tmp = list(reader)
      for t in tmp:
          t = parsePoem2(" ".join(list(filter(None, t))))
          if t != []:
              p.append(t)
    return p


def one_poem_counter(poem):
  cnt = Counter()
  for word in poem:
    if cnt[word] != 2:
      cnt[word] += 1
  return cnt

#word  counted once in a poem
def overall_count(poems):
    print("overall_count")
    count = [None]*len(poems)
    global p_len
    for i in tqdm(range(p_len)):
        count[i]=one_poem_counter(poems[i])
    #adding counters together
    overall_count = Counter();
    print("getting to overall_count calculation")
    for counter in tqdm(range(len(count))):
        overall_count = overall_count + count[counter]
    print("done")
    return overall_count, count

def count(poems):
  print("count")
  count = [None]*len(poems)
  for i in tqdm(range(len(poems))):
      count[i]=one_poem_counter(poems[i])
  #print(count)
  return count

def word_to_others(wordList, poemsCounter):
    counterList = {}
    for word in wordList:
        counter = Counter()
        
        for poemCounter in poemsCounter:
            if poemCounter[word]>=1:#what do you think about this
                for innerword, occurrence in poemCounter.most_common(10):
                    #print("yes")
                    #print(innerword)
                    #print(occurence)
                    counter[innerword]+=occurrence
        counterList[word] = counter
        #print(counter.most_common())
    return counterList


def getKeys(co):
  temp = []
  for x in co.most_common():
    temp.append(x[0])
  return temp

def doTheThing(co):
  temp = []
  temp2 = []
  for x in co.most_common():
    temp.append(x[0])
    temp2. append(x[1])
  return temp, temp2

def get_associated_word(word):
    resp = get('https://similarwords.p.mashape.com/moar?query='+word, headers = {"X-Mashape-Key": "r63BPcKtDHmsho4tWg8EpyDaFtWCp1mRt55jsnD5ZpLdLfNhXS","Accept": "application/json"})
    data = resp.json()
    return data['result']


def from_csv(file):
    p = []
    with open(file) as f:
      reader = csv.reader(f)
      tmp = list(reader)
      for t in tmp:
          t = parsePoem2(" ".join(list(filter(None, t))))
          if t != []:
              p.append(t)
    return p
poems = from_csv("out2.csv") 
p_len = len(poems)

#regularizes keywords (horizontal thing)(variable c)
c, count_notOverall = overall_count(poems)  
total = p_len
#print(len(c))
max_threshold = 1/3
for x in c.most_common():
  #print(x)
  #print(str(x[1]/total) + " " + str(max_threshold))
  if x[1]/total > max_threshold:
    del c[x[0]]
    for cou in count_notOverall:
        del cou[x[0]]
  elif x[1] < 3:
    del c[x[0]]
    for cou in count_notOverall:
        del cou[x[0]]
                
    
                    
#print("making wordDiction")
poemsCounter = count_notOverall
#print("commonWords")
common_word = list(getKeys(c))
#print("done")
wordDiction = word_to_others(common_word, poemsCounter)
#print("done")

while True:
    #print(c)
    #lost = ["love", "lobe"]
    #print(lost)
    result_counter = Counter()
    user_input = input("enter a line of your own poetry (use  forward slash to separate lines)\nEnter:")

    
    #print(common_word)
    
    wordList = parsePoem2(user_input)
    #print((wordDiction['love'].most_common()))
    
    for word in tqdm(wordList):
        if(wordDiction.get(word)!=None):
            #print(word)
            for suggestion, occurrence in wordDiction.get(word).most_common(5):
                result_counter[suggestion] += occurrence
                #print(suggestion)
        else:
            associated_list = get_associated_word(word)
            t = 0
            while t < len(associated_list):
                if wordDiction.get(associated_list[t])!=None :
                    for suggestion, occurrence in wordDiction.get(associated_list[t]).most_common(5):
                        result_counter[suggestion] += occurrence
                    break
                t+=1
    """
    if(result_counter.most_common()==[] and wordList!=[]):
        rhymeDict = getrhyme(wordList[len(wordList)-1])
        rhymeList = rhymeDict['word']
        print("We cannot find any suggestion for given input. However, here is a list that rhymes with the last word")
        print(rhymeList)
    """
        
    print(result_counter.most_common(10))
    
        
        

    

digits = datasets.load_digits
#images_and_labels = list(zip(digits.images, digits.target))
