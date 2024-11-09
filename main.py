import argparse
from parsing import startParsing
from summarization import start_Summarizing
from keyWord import start_Keyword_extraction
from docUpdation import updateMongodb
from datetime import datetime
start_time = datetime.now()

def parse_arguments():
    parser = argparse.ArgumentParser(description ='give folder path.')
    parser.add_argument('-folder',
                    type = str,
                    help ='folder containing pdf files.')
    return parser.parse_args()


def startPipeline(args):
    try:

        parse = startParsing(folder=args.folder)
        summary = start_Summarizing(parse)
        keyword = start_Keyword_extraction(parse)
        updateMongodb(summary)

        return "done successfully.."
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    args = parse_arguments()
    startPipeline(args)
    
#end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))
