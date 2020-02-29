import numpy as np 
import pandas as pd 
import sys
import os

import time
import random
import warnings
warnings.simplefilter('ignore')

import PyPDF2
import textract
import re

from nltk.corpus import stopwords


def mapper(text):

	return True if len(text)>4 else False

def preprocess(filename = 'B.E. Project Synopis-converted.pdf'):

	pdfFileObj = open(filename,'rb')               
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   
	num_pages = pdfReader.numPages

	count = 0
	text = ""
	                                                            
	while count < num_pages:                       
	    pageObj = pdfReader.getPage(count)
	    count +=1
	    text += pageObj.extractText()
	    
	if text != "":
	    text = text
	 
	else:
	    text = textract.process('http://bit.ly/epo_keyword_extraction_document', method='tesseract', language='eng')


	text = text.encode('ascii','ignore').lower()
	text = str(text)
	delimited = re.split(r'(\\\n|\.)\s*', text)
	keywords = re.findall(r'[a-zA-Z]\w+',text)

	return text, delimited, keywords, filename

text, delimited, keywords, filename = preprocess()

stop_ = set(stopwords.words('english'))
stop_keys = [word for word in keywords if word not in stop_]
filtered_keys = filter(mapper, stop_keys)


df = pd.DataFrame(list(set(filtered_keys)),columns=['keywords'])


def weightage(word,text,number_of_documents=1):

    word_list = re.findall(word,text)

    number_of_times_word_appeared =len(word_list)
    tf = number_of_times_word_appeared/float(len(text))
    idf = np.log((number_of_documents)/float(number_of_times_word_appeared))

    tf_idf = tf*idf

    return number_of_times_word_appeared,tf,idf ,tf_idf 

df['number_of_times_word_appeared'] = df['keywords'].apply(lambda x: weightage(x,text)[0])
df['tf'] = df['keywords'].apply(lambda x: weightage(x,text)[1])
df['idf'] = df['keywords'].apply(lambda x: weightage(x,text)[2])
df['tf_idf'] = df['keywords'].apply(lambda x: weightage(x,text)[3])

df = df.sort_values('tf_idf',ascending=True)
df.to_csv('Keywords_tf_idf_{}.csv'.format(filename), index=False)
# df.head(25)

def keywords_with_gensim(text):

	from gensim.summarization import keywords

	values = keywords(text=text, split='\n', scores=True)

	data = pd.DataFrame(values,columns=['keyword','score'])

	data = data.sort_values('score',ascending=False)
	# data.head(10)

	return data

gensim_df = keywords_with_gensim(text)
gensim_df.to_csv('Keywords_gensim_{}.csv'.format(filename), index=False)

def keywords_with_rake(text):

	from rake_nltk import Rake 

	r = Rake()
	r.extract_keywords_from_text(text)

	phrases = r.get_ranked_phrases_with_scores()

	table = pd.DataFrame(phrases,columns=['score','Phrase'])
	table = table.sort_values('score',ascending=False)

	return table

rake_df = keywords_with_rake(text)
rake_df.to_csv('Keywords_rake_{}.csv'.format(filename), index=False)

def helper(df, col):

	array = []

	for idx,row in df.iterrows():
		array.append(row[col])

	return array

def find_best_suited_words(filename=filename):

	term_file, gensim_file, rake_file = 'Keywords_tf_idf_{}.csv'.format(filename), 'Keywords_gensim_{}.csv'.format(filename), 'Keywords_rake_{}.csv'.format(filename)

	# print(term_file, gensim_file, rake_file)

	term_df = pd.read_csv(term_file)
	gensim_df = pd.read_csv(gensim_file)
	rake_df = pd.read_csv(rake_file)

	# print(term_df.head(5),gensim_df.head(5),rake_df.head(5))

	lowest = min(len(rake_df), len(term_df), len(gensim_df))

	term_df, gensim_df, rake_df = term_df[:lowest], gensim_df[:lowest], rake_df[:lowest]

	selected,k = {},0

	term_df_keys = helper(term_df,'keywords')
	gensim_df_keys = helper(gensim_df,'keyword')
	rake_df_keys = helper(rake_df,'Phrase')

	while k < len(term_df_keys):

		selected[term_df_keys[k]] = 0 #set value to 0 first

		try:

			if term_df_keys[k] in gensim_df_keys:
				selected[term_df_keys[k]] +=1

			for item in rake_df_keys:

				if term_df_keys[k] in item:
					selected[term_df_keys[k]] += 1

			k+=1

		except Exception as e:

			k+=1 #if an exception occurs, k has not been reached
			print('{} occurred, passing. '.format(e))

			pass

	# print("\nKeywords : \n")
	# for key,val in selected.items():
	# 	print("" if val==0 else "{} : {}".format(key,val))

	return sorted(selected.items(), reverse=True, key=lambda x:x[1])

sample = find_best_suited_words()
print('\nTop 5 keywords : \n')
for k,v in sample[:5]:
	print('{} : {}'.format(k,v))