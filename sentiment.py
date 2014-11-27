import pandas as pd
import sys, os
import math
import nltk
 
file_to_read = r"train.tsv"
train_data_pandas = pd.read_table(file_to_read)
 
features = []

size = train_data_pandas.count()[0]

train_data_pandas['Unigrams'] = train_data_pandas['Phrase'].str.split() 

bigrams = [] 												
for i in range(size):
    t = list(nltk.bigrams(train_data_pandas['Phrase'][i].split()))	
    t = list(map(lambda x: x[0] + ' ' + x[1], t))
    bigrams.append(t)

train_data_pandas['Bigrams'] = bigrams

print train_data_pandas

 
# # ---------------------------------------------------------------V to ograniczenie pozniej nalezy usunac [H]
for index,number,phraseid,phrase,sentiment in train_data_pandas[0:1].itertuples():
# iterujemy poszczegolne linie z danych jako tuple, index = number -1, nie ma potrzeby przeksztalcania tabeli danych [H]
    V = 0
    d = {}
    words = phrase.split()
    print 'list = ', words
 
    for word in words:
        d[word] = d.setdefault(word, 0) + 1
 
    for word in d:
        C = d[word]
        P = train_data_pandas[train_data_pandas['Sentiment'] == 0].count()[0]
        N = train_data_pandas[train_data_pandas['Sentiment'] == 2].count()[0]
        Pt = 0
        Nt = 0   
        #wybieramy tylko columny frazy i sentymentu, tworzoymy nowy 'dataframe' [H]
        phrase_and_sentiment_columns = train_data_pandas[['Phrase','Sentiment']]
        print phrase_and_sentiment_columns # odkomentuj sobie i zobacz jak teraz to wyglada [H]
        #wybieramy tylko pierwszy wpis (mozna usunac, zalezy co chcesz zrobic) [H]
        phrase_and_sentiment_columns = phrase_and_sentiment_columns[0:1]
        # --V numer linii, V fraza, V wartosc saentymentu----------------V iterujemy po liniach jako tuple [H]
        for col_id,phrase_in, sentiment_in in phrase_and_sentiment_columns.itertuples():
            print ("diff info", phrase_in.split(), sentiment_in)
            if word in phrase_in.split() and sentiment_in == 0:
            	print ('THERE IS PHRASE to Pt!')
                Pt += 1
            elif word in phrase_in.split() and sentiment_in == 2:
            	print ('THERE IS PHRASE to Nt!')
                Nt += 1
 
        print 'for formula: ', word, C, P, N, Pt, Nt
 
        #dzielisz tutaj przez zero, dlatego jest blad [H]
        V_l = C * math.log((N * Pt)/(P * Nt), 2) #nie wiem dlaczego nie rachuje poprawnie, chociaz jak policzyc to osobno z 
        print V_l      #wyzej wypisanymi wynikami - ma byc dobrze...
        V += V_l
 
        features.append(V)
 
 
print(features)
# jak nie wiemy co to bedzie pozytywny i negatywny to moim zdaniem bedzie sensownie zgenerowac takie features()
		# 0 2
		# 0 3
		# 0 4
		# 1 2
		# 1 3
		# 1 4
		# 2 3
		# 2 4