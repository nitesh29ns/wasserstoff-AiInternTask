import fitz, pymupdf
import os, pickle, requests, re
import pymongo
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
#start_time = datetime.now()

# funcation for uploading data to monogodb
def upload_to_mongodb(file_path:str,pdf:pymupdf.Document):
    try:
        # connect with the mongodb
        client = pymongo.MongoClient(secrets.MONGODB_URL)
        db = client.pdf_db
        db.client['pdf_db'] 
        coll = db['pdf_collection']

        collection = {}

        # get the size of the pdf in kb
        file_size = os.path.getsize(file_path) # Size in bytes
        file_size_kb = file_size / 1024  

        # check the varying length of the pdf
        if pdf.page_count in range(1,3):
            collection["document_length"] = "short_pdf"
        elif pdf.page_count in range(1,13):
            collection['document_length'] = "medium_pdf"
        else:
            collection['document_length'] = "long_pdf"

        collection["document_name"] = os.path.basename(file_path)
        collection['size'] = file_size_kb
        collection['path'] = file_path
        
        # insert the the collection in the db
        coll.insert_one(collection)

    except Exception as e:
        raise e

# funcation for parsing and storing extracted text into text file.
def parse_pdf_txt(file_path):
    try:
        pdf = fitz.open(file_path)
        
        # check for encrypted or password protected pdf file...
        if pdf.is_encrypted:
            print(f"Skipping password-protected PDF: {file_path}")
            pdf.close()

        upload_to_mongodb(file_path=file_path, pdf=pdf)

        # make directory for storing the extraced text in .txt
        os.makedirs("./testing", exist_ok=True)
        path = os.path.join('./testing',os.path.basename(file_path))
        with open(f"{path}.txt","w",encoding='utf-8') as f:
            for page in pdf:
                f.writelines(re.sub("[^a-zA-Z0-9.]", " ", page.get_text()))
        pdf.close()
    
    except Exception as e:
        print(f"Failed to open or process PDF '{file_path}': {e}")
        return None
    
# funcation for parsing pdf and store into pickle object(list of data dictionary)
def parse_pdf(file_path):
    try:      

        pdf = fitz.open(file_path)

        # call the funcation for data upload to db
        upload_to_mongodb(file_path=file_path, pdf=pdf)

        if pdf.page_count > 0:

            # store extracted text in the string object..
            data = {}
            text = ""
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text += page.get_text("text") + "\n"
            data[os.path.basename(file_path)] = re.sub("[^a-zA-Z0-9.]", " ", text) # text preprocessing
        else:
            print(f"pdf has no pages {file_path}")

        
        pdf.close()     
        return data
    
    except Exception as e:
        print(f"Failed to open or process PDF '{file_path}': {e}")

# funcation for thread processing for high efficiently
def ThreadProcess(pdf_files:list):
    try:
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            result = executor.map(parse_pdf, pdf_files)
        
        l = []
        for i in result:
            if type(i) == dict: # for None type object..
                l.append(i)

        with open("./parse_data.pkl", 'wb') as fp:
            pickle.dump(l, fp)

        return "./parse_data.pkl"
            
    except Exception as e:
        raise e

# funcation for initiate the parsing in a single funcation.   
def startParsing(folder:str):
    try:
        dir = os.listdir(folder) # extract the file_path
        pdf_files = [] 
        for i in dir:
            path = os.path.join(folder,i)
            pdf_files.append(path)

        # for testing purpose
        #pdf_files.append("https://openlibrary-repo.ecampusontario.ca/jspui/bitstream/123456789/1301/2/The-Book-of-Small-1645800325._print.pdf")
        
        # for scanning url links too..
        for file in pdf_files:
            if file.startswith("https://"):
                response = requests.get(file)
                file_name = os.path.basename(file)
                new_file_path = os.path.join(folder,file_name)  
                if response.status_code == 200: 
                    with open(new_file_path, 'wb') as file:
                        file.write(response.content)   

        # call the funcation
        parsed_texts = ThreadProcess(pdf_files=pdf_files)
        
        return parsed_texts
    except Exception as e:
        raise e

#startParsing(folder='./data',max_workers=5,pickle_obj='pickle_obj')

#end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))
