import pymongo
import pickle
from pathlib import Path
from pymongo.server_api import ServerApi

#summaries = pickle.load(open("summary_obj.pkl", "rb"))

#keywords = pickle.load(open("extracted_keywords.pkl", "rb"))

def updateMongodb(summary:str):
    try:
        summaries = pickle.load(open(summary, "rb"))

        keywords = pickle.load(open(Path("./extracted_keywords.pkl"), "rb"))


        # connect with the mongodb
        url = "mongodb+srv://nitesh8527:Nitesh8527@cluster0.bxxtr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = pymongo.MongoClient(url, server_api=ServerApi('1'), tls=True) #  secrets.MONODB_URL
        db = client.pdf_db
        db.client['pdf_db'] 
        coll = db['pdf_collection']

        for summary, keyword in zip(summaries,keywords):
            coll.update_one({'document_name': f'{summary[0]}'}, {"$set":{"summary": f"{summary[1]}","keywords":f"{keyword[0][1]}"}})

    except Exception as e:
        raise e
