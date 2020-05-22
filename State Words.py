
# coding: utf-8

# In[40]:


import urllib.request

#Read in the list of words.  Fortunately, this list of words is just straight up text, so easy to parse!
url="https://norvig.com/ngrams/word.list"
file = urllib.request.urlopen(url)

#Initialize the wordlist
wordlist = []

#Read in each line of the file
for line in file:
    word = line.decode("utf-8").rstrip()
    wordlist.append(word)
    


# In[41]:


from lxml import html
import requests

#Read in a list of states.  This page is a little more complex to parse, so need some html parsing.
url_state = "https://www.plaintextlist.com/geography/list_of_us_states/"
#Read in the page
page = requests.get(url_state)

#Translate the page html to tree nodes so we can parse it
tree = html.fromstring(page.content)

#This reads in only the text from the p elements with the content_item class
states = tree.xpath('//p[@class="content_item"]/span/text()')

#Lowcase the state names so they match the word list
states = [str.lower() for str in states]
    


# In[9]:


#Cribbed this from https://www.geeksforgeeks.org/check-two-strings-common-substring/ with some changes- thanks, ChitraNayal!

def twoStrings(s1, s2) : 
  
    # vector for storing character 
    # occurrences 
    v = [0] * (26) 
      
    # increment vector index for every 
    # character of str1 
    for i in range(len(s1)): 
        v[ord(s1[i]) - ord('a')] = True
      
    # checking common substring  
    # of str2 in str1 
    for i in range(len(s2)) : 
        if (ord(s2[i]) - ord('a') <= 26) and  (ord(s2[i]) - ord('a') >= 0):            
            if (v[ord(s2[i]) - ord('a')]) : 
                return True
        
    return False


# In[10]:


#Using twoStrings above, compare a word to a list of words.
#If one matches, return that one
#If none match, return NONE
#If two or more match, return MULTIPLE
def checkWord(word,wordlist):
    count=0
    match=''
    for worditem in wordlist:       
        if twoStrings(word,worditem) == False:
            count = count + 1
            match = worditem
            ##print(worditem,':',word)
            if count > 1:
                return 'MULTIPLE'
    if count == 1:
        return match
    return 'NONE'


# In[11]:


#Run checkWord on each element in wordlist, then grab the lengths and zip to a final result list

resultList = [checkWord(worditem,states) for worditem in wordlist]
lenList   = [len(word) for word in wordlist]
final_list=list(zip(wordlist,resultList,lenList))


# In[12]:


#Determine the max length by iteration

maxLen=0
for (word,result,len) in final_list:
    if (result != 'MULTIPLE' and result != 'NONE'):
        if len > maxLen:
            maxLen = len
            
            
#Print out those records with the max length
for (word,result,len) in final_list:
    if (result != 'MULTIPLE' and result != 'NONE' and len == maxLen):
        print(word,':',result)


# In[52]:


#Extra Credit!  Finding the count per state

import pandas as pd
import numpy as np

#Using pandas, creating a dataframe from the list of only the unique words
uniqueWordList = pd.DataFrame(list(filter(lambda w: w[1] != 'NONE' and  w[1] !='MULTIPLE',final_list))
                             , columns=['word','state','length'])

#using numpy, count the unique values of state, and return them
vals,counts = np.unique(uniqueWordList.state, return_counts=True)

#Zip the results into a dict and print to screen
table = dict(zip(vals,counts))
table

