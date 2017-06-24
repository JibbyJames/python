import re
import pandas as pd
import numpy as np

MsgTable = pd.read_csv('data/whatsapp_nidaa_data.csv', header=None, encoding='utf-8')

JamesMsgTable = MsgTable[MsgTable[2] == 'James Buckley']
NidaaMsgTable = MsgTable[MsgTable[2] == 'Nidaa Ali']

# James Variables
JamesMsgList = JamesMsgTable[3].tolist()
JamesWordList = ' '.join(JamesMsgList).lower().split()
JamesWordList = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in JamesWordList]

from collections import Counter
JamesWordCount = pd.DataFrame.from_dict(dict(Counter(JamesWordList)), orient='index').reset_index()
JamesWordCount.columns =['Word','JamesCount']

JamesWordCount['Word'].replace(regex=True,inplace=True,to_replace=r'\d|\W|\?|http*',value=r'')
DropWords = ['','a','and','u','to','for','with','of','in','x','am','pm','omitted','image']
JamesWordCount['Word'].replace(DropWords, np.nan, inplace=True)
JamesWordCount.dropna(subset=['Word'], inplace=True)
JamesWordCount.sort_values(by=['JamesCount'],axis=0, ascending=False, inplace=True)

# Nidaa Variables
NidaaMsgList = NidaaMsgTable[3].tolist()
NidaaWordList = ' '.join(NidaaMsgList).lower().split()
NidaaWordList = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in NidaaWordList]

NidaaWordCount = pd.DataFrame.from_dict(dict(Counter(NidaaWordList)), orient='index').reset_index()
NidaaWordCount.columns =['Word','NidaaCount']

NidaaWordCount['Word'].replace(regex=True,inplace=True,to_replace=r'\d|\W|\?|http*',value=r'')
DropWords = ['','a','and','u','to','for','with','of','in','omitted','image']
NidaaWordCount['Word'].replace(DropWords, np.nan, inplace=True)
NidaaWordCount.dropna(subset=['Word'], inplace=True)
NidaaWordCount.sort_values(by=['NidaaCount'],axis=0, ascending=False, inplace=True)

MergedWordCount = pd.merge(JamesWordCount, NidaaWordCount, on='Word')
MergedWordCount.to_csv('data/MergedWordCount.csv', index=False)