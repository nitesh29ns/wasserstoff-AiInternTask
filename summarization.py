import nltk
from nltk.stem import WordNetLemmatizer
import pickle, os
import pymongo
from concurrent.futures import ThreadPoolExecutor
#from datetime import datetime
#start_time = datetime.now()

client = pymongo.MongoClient(secrets.MONGODB_URL)
db = client.pdf_db
print(db)
db.client['pdf_db'] 
coll = db['pdf_collection']

# check the length of the pdf
short = []
for i in coll.find({"document_length": "short_pdf"}):
    short.append(i['document_name'])
    #print(i["document_name"])

medium = []
for i in coll.find({"document_length": "medium_pdf"}):
    medium.append(i['document_name'])
    #print(i["document_name"])


long = []
for i in coll.find({"document_length": "long_pdf"}):
    long.append(i['document_name'])
    #print(i["document_name"])

def score_sentence_legal_domian(sentence, keywords):
    try:
        words = nltk.word_tokenize(sentence.lower())
        
        return sum(1 for word in words if word in keywords)
    except Exception as e:
        raise e
    

def summerizing(sentences:str,stop_words:list,domain_keywords:list, length:int):   
    try:

        sentences = nltk.sent_tokenize(sentences)

        lemmatizer = WordNetLemmatizer()
        corpus = []
        for i in range(len(sentences)):
            words=nltk.word_tokenize(sentences[i].lower())
            words = [lemmatizer.lemmatize(word) for word in words if not word in stop_words]
            corpus.append(" ".join(words))

            #score_sentence_legal_domian(sentences,domain_keywords)
        scored_sentences = [(sentence, score_sentence_legal_domian(sentence, domain_keywords)) for sentence in corpus]
        scored_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)


        summary = " ".join([sentence for sentence, score in scored_sentences[:length]])

        return summary
    except Exception as e:
        raise e

with open("stop_word_obj.pkl","rb") as f:
    stop_words = pickle.load(f)

with open("domain_keywords_obj.pkl","rb") as f:
    domain_keywords = pickle.load(f)

#with open("parse_data.pkl","rb") as f:
#    data = pickle.load(f)

#data_list = []
#for i in data:
#    for key, value in i.items():
#        data_list.append((key,value))

def start_summarizing(data_list:list):
    try:
        l = []
        for i in range(len(data_list)):
            if data_list[i][0] in short:
                length = 2
                #print(length)
            elif data_list[i][0] in medium:
                length = 3
                #print(length)
            else :
                length = 4
                #print(length)
            
            s = summerizing(sentences=data_list[i][1],stop_words=stop_words,domain_keywords=domain_keywords,length=length)
            l.append((data_list[i][0], s))        
        
        if os.path.isfile("./summary_obj.pkl"):
            data = pickle.load(open('summary_obj.pkl','rb'))
            l = data + l
            with open("./summary_obj.pkl", 'wb') as f:
                pickle.dump(l,f)
        else:
            with open("./summary_obj.pkl", 'wb') as f:
                pickle.dump(l,f)

        return "./summary_obj.pkl"
    except Exception as e:
        raise e


# funcation for thread processing for high efficiently
def ThreadSummarizing(data_list:list):
    try:
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(start_summarizing, [data_list])

            for i in result:

                return i

    except Exception as e:
        raise e


def start_Summarizing(parse:str):
    try:
        with open(parse,"rb") as f:
            data = pickle.load(f)
        data_list = []
        for i in data:
            for key, value in i.items():
                data_list.append((key,value))

        summary = ThreadSummarizing(data_list=data_list)

        return summary
    
    except Exception as e:
        raise e


#end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))
