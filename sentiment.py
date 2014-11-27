import pandas as pd
import sys, os
import math

file_to_read = r"train.tsv"
train_data_pandas = pd.read_table(file_to_read)

tmp_storrage = []
for i in train_data_pandas:
    tmp_storrage.append(zip(train_data_pandas['Phrase'], train_data_pandas['Sentiment']))
train_data = tmp_storrage

# print (train_data[0][0])
features = []

for phrase, sentiment in train_data[0]:
	print(phrase)
	V = 0
	d = {}
	words = phrase.split()
	print 'list = ', words

	for word in words:
		d[word] = d.setdefault(word, 0) + 1

	print d
	for word in d:
		C = d[word]
		P = train_data_pandas[train_data_pandas['Sentiment'] == 0].count()[0]
		N = train_data_pandas[train_data_pandas['Sentiment'] == 2].count()[0]
		Pt = 0
		Nt = 0
		for phrase_in, sentiment_in in train_data[0]:
			if word in phrase_in.split() and sentiment_in == 0:
				Pt += 1
			elif word in phrase_in.split() and sentiment_in == 2:
				Nt += 1

		print (word, C, P, N, Pt, Nt)

		V_l = C * math.log((N * Pt)/(P * Nt), 2) 		#nie wiem dlaczego nie rachuje poprawnie, chociaz jak policzyc to osobno z 
		print V_l										#wyzej wypisanymi wynikami - ma byc dobrze...
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