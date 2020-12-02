import Classes.Path as Path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import RegexTokenizer
import pandas as pd
import pathlib
import pickle

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    writer=[]

    def __init__(self):
        rootPath = pathlib.Path(__file__).parent.parent.__str__()
        self.inputFilePath = rootPath + Path.InputPickleFile

        schema = Schema(doc_no=ID(stored=True),
                        doc_content=TEXT(analyzer=RegexTokenizer(), stored=True),
                        doc_title=TEXT(stored=True))
        indexing = index.create_in(rootPath + Path.IndexPath, schema)
        self.writer = indexing.writer()
        return

    # This method build index for each document.
    def index(self, docNo, content, title):
        self.writer.add_document(doc_no=docNo, doc_content=content, doc_title=title)
        return
    
    # This method build index for entire corpus.
    def indexCorpus(self):
        count = 0
    
        # Initiate pre-processed collection file reader.
        pickle_in = open(self.inputFilePath,"rb")
        product_df = pickle.load(pickle_in)
        corpus = product_df[1:20001]
        
        # Build index of corpus by product.
        for row in corpus.iterrows():
            self.index(str(row[1]['product_uid']), row[1]['description_words'], row[1]['product_title'])
            count+=1
#            if count%5000==0:
#                print("Finished indexing ", count," products")
#        
        # Finish
#        print("Totally finished, indexed ", count, " products")
        self.close()
        return

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        self.writer.commit()
        return
