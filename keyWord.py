import nltk
from collections import Counter
import pickle

with open("stop_word_obj.pkl","rb") as f:
    stop_words = pickle.load(f)

with open("domain_keywords_obj.pkl","rb") as f:
    domain_keywords = pickle.load(f)

#with open("pickle_obj","rb") as f:
#    data = pickle.load(f)


"""data_list = []
for i in data:
    for key, value in i.items():
        data_list.append((key,value))"""

def keyword_Extraction(data_list:list):
    try:
        extracted_Keywords = []
        for sentances in data_list:
            
            words = nltk.word_tokenize(sentances[1])
            common = []
            for word in words:
                if word in domain_keywords:
                    common.append(word)
                    #print(word)
            freq_word = Counter(common)
            extracted_Keywords.append([(sentances[0] ,[i[0] for i in freq_word.most_common(10)])])
            
        pickle.dump(extracted_Keywords, open("./extracted_keywords.pkl",'wb'))
        
        return "./extracted_keywords.pk"
    except Exception as e:
        raise e
    

def start_Keyword_extraction(parse:str):
    try:
        with open(parse,"rb") as f:
            data = pickle.load(f)

        data_list = []
        for i in data:
            for key, value in i.items():
                data_list.append((key,value))

        keyword = keyword_Extraction(data_list=data_list)

        return keyword
    except Exception as e:
        raise e