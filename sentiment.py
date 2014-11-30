import pandas as pd
import sys, os
import math, nltk, re, pickle
 
file_to_read = r"train.tsv"
train_data = pd.read_table(file_to_read)
 

size = train_data.count()[0]

#? lower case phrases


train_data['Unigrams'] = train_data['Phrase'].str.split() 

bigrams = [] 												
for i in range(size):
    t = list(nltk.bigrams(train_data['Phrase'][i].split()))	
    t = list(map(lambda x: x[0] + ' ' + x[1], t))
    bigrams.append(t)

train_data['Bigrams'] = bigrams


A = []

combs = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3), (2, 4)]
for i in range(5):
	A.append(train_data[train_data['Sentiment'] == i].count()[0])

matrix = []

for index, number, phraseid, phrase, sentiment, unigrams, bigrams in train_data[0:1].itertuples(): 		#forAll
	
	V = 0
	V_uni = 0
	V_bi = 0

	features = [0] * len(combs)

	for uni in unigrams:
		uni = re.escape(uni)
		C_uni = len(re.findall('\W?' + uni + '\W?', phrase))

		features_tmp = []
		for pair in combs:
			N_t = train_data[(train_data['Sentiment'] == pair[0]) & (train_data['Phrase'].str.contains('\W' + uni + '\W'))].count()[0]
			P_t = train_data[(train_data['Sentiment'] == pair[1]) & (train_data['Phrase'].str.contains('\W' + uni + '\W'))].count()[0]


			if N_t != 0 and P_t != 0:
				V_uni = C_uni * math.log((A[pair[0]] * P_t) / float((A[pair[1]] * N_t)), 2)
			elif N_t != 0:
				V_uni = C_uni * math.log(A[pair[0]] / float((A[pair[1]] * N_t)), 2)
			elif P_t != 0:
				V_uni = C_uni * math.log((A[pair[0]] * P_t) / float(A[pair[1]]), 2)
			else:
				V_uni = 0

			print ('unigram = ' + uni + ', pair = ' + str(pair), ', C = ' + str(C_uni) + ', N = ' + str(A[pair[0]]) + ', P = ' + str(A[pair[1]]) + ', Pt = ' + str(P_t) + ', Nt = ' + str(N_t) + ', V = ' + str(V_uni))
			features_tmp.append(V_uni)
			print ('features_tmp = ' + str(features_tmp))
			print ('features = ' + str(features))
			print ('\n')

		features_tmp = map(lambda x: 1.0 * x / len(unigrams), features_tmp)
		features = [(x + y) for (x, y) in zip(features, features_tmp)]

	matrix.append(features)
	# print number

	###for bigrams

with open('unigrams.dat', 'wb') as f:
    pickle.dump(matrix, f)