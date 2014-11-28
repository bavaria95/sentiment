import pandas as pd
import sys, os
import math, nltk, re
 
file_to_read = r"train.tsv"
train_data = pd.read_table(file_to_read)
 
features = []

size = train_data.count()[0]

#? lower case phrases


train_data['Unigrams'] = train_data['Phrase'].str.split() 

bigrams = [] 												
for i in range(size):
    t = list(nltk.bigrams(train_data['Phrase'][i].split()))	
    t = list(map(lambda x: x[0] + ' ' + x[1], t))
    bigrams.append(t)

train_data['Bigrams'] = bigrams

# print train_data


for index, number, phraseid, phrase, sentiment, unigrams, bigrams in train_data[0:117].itertuples():
	V = 0

	V_uni = 0
	V_bi = 0

	N_t = 0
	P_t = 0

	P = train_data[train_data['Sentiment'] == 0].count()[0]

	N = train_data[train_data['Sentiment'] == 2].count()[0]


	for uni in unigrams:
		uni = re.escape(uni)

		N_t_t = train_data[(train_data['Sentiment'] == 0) & (train_data['Phrase'].str.contains('\W' + uni + '\W'))].count()[0]
		P_t_t = train_data[(train_data['Sentiment'] == 2) & (train_data['Phrase'].str.contains('\W' + uni + '\W'))].count()[0]

		C_uni = len(re.findall('\W?' + uni + '\W?', phrase))


		if P * N_t_t != 0 and N * P_t_t != 0:
			V_uni = C_uni * math.log((N * P_t_t) / (P * N_t_t), 2)
			print (uni, C_uni, P, N, P_t_t, N_t_t, V_uni)
		else:
			print (uni, C_uni, P, N, P_t_t, N_t_t)			


	# for bi in bigrams:
	# 	N_t_bi += train_data[(train_data['Sentiment'] == 0) & (train_data['Phrase'].str.contains(bi))].count()[0]



# jak nie wiemy co to bedzie pozytywny i negatywny to moim zdaniem bedzie sensownie zgenerowac takie features()
		# 0 2
		# 0 3
		# 0 4
		# 1 2
		# 1 3
		# 1 4
		# 2 3
		# 2 4