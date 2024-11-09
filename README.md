# nitesh-sharma-wasserstoff-AiInternTask

## Web application link
## https://wasserstoff-aiinterntask-production.up.railway.app/

## Task Details
---
## 1. PDF Ingestion & Parsing
My `approach for Pdf Parsing` is simple extract the text data from the pdf and create a dictionary object containing keys as pdf name and values as extracted text, and save as pickle object for further tasks.

parsing pdf from the desktop folder extract text from the pdf perform neccessary text preprocessing and insert into MongoDB contain meta data(pdf_name, path, size in kb, length of the document) like shot, medium, or long.
Exception Handeling done in a way that it doesn't affect the database, and not any corrupt pdf or passward protected pdf crash the pipeline.

for best performance using `ThreadPoolExecutor`.


## 2. summarization & Keyword Extraction
As i choose the `Legal Domain`, so `MY Approach for Summarizing` is i gether the list of terms which are used most of the time in legal documnents, around 500 words are there in the list.

Not using any framework like langchain or huggingface. done all the text processing neccessary for summarization and key word extraction. Take the text data and convert them into sentences using `sent_tokenize`. for geting the word having meaning using `lemmatization method`.

Reducing the size of the text by removing the stop_words from the sentance, which is not neccessary for summarizing. build a `Custom Function` which `Calculate the relevance in the sentance based on the Specific Domain` which is in my case is `Legal Domain`, and give them the score. based on that score Summary is generated, `Length of the Summary` is based on the `Length of the Pdf`. create a pickle object containing summary for using in DB.

`KeyWord Extraction` `My Approach` is i create a `Custom Funcation` that checks the each words of the extracted text are in there in legal domain list and what is the count of it. create an pickle object containing list of keywords for using in DB.

## 3. MongoDB Updates
Update the existing collection of each pdf containing meta data with summary and keywords. use the existing pickle objects that we generate from summarization.py and keyword.py .

## `Main.py`
main.py Containing and calling all the other functions here and it takes an input which is folder having pdfs. It `initiate the entire Pipeline` in a single command.

main.py can be called directly through command line
```sh
python main.py -folder ./folder_name or path
```
## Installation

create the python virtual environment
```sh
conda create -p ./env python==3.12.0
```
Activate the virtual environment
```sh
conda activate ./env
```

Install the dependencies
```sh
pip install -r requirements.txt
```

## Performance

| PYTHON SCRIPT | EXECUTION TIME (sec)|
| ------ | ------ |
| Parsing.py | 06.494 |
| summarization.py | 10.78 |
|keyword.py |03.41 |
| docUpdation.py | 01.95 |
| main.py | 19.22 |
