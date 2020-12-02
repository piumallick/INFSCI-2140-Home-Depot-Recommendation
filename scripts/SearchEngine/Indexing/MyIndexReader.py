import whoosh.index as index
from whoosh.reading import IndexReader
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexTokenizer
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
import Classes.Path as Path
import pathlib

class MyIndexReader:

    searcher=[]

    def __init__(self):
        rootPath = pathlib.Path(__file__).parent.parent.__str__()
        self.searcher = index.open_dir(rootPath + Path.IndexPath).searcher()
        self.document_term_freq=defaultdict(dict)

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return self.searcher.document_number(doc_no=docNo)

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        return self.searcher.stored_fields(docId)["doc_no"]
    
    # Return the document title
    def getDocTitle(self, docId):
        return self.searcher.stored_fields(docId)["doc_title"]

    # Return DF.
    def DocFreq(self, token):
        results = self.searcher.search(Term("doc_content", token))
        return len(results)

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        results = self.searcher.search(Term("doc_content", token), limit=None)
        count = 0
        for result in results:
            words = self.searcher.stored_fields(result.docnum)["doc_content"].split(" ")
            for word in words:
                if word==token:
                    count+=1
        return count

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        results = self.searcher.search(Term("doc_content", token), limit=None)
        postList = {}
        for result in results:
            words = self.searcher.stored_fields(result.docnum)["doc_content"].split(" ")
            count=0
            for word in words:
                if word==token:
                    count+=1
            postList[result.docnum]=count
        return postList

    # Return the length of the requested document.
    def getDocLength(self, docId):
        words = self.searcher.stored_fields(docId)["doc_content"].split(" ")
        return len(words)

    # Return the total length of documents in Index
    def getDocumentCount(self):
        return self.searcher.doc_count()
    
    def getTermDocumentFreq(self, term, docId):
        try:
            termDocumentFreq = self.document_term_freq[term][docId] 
        except KeyError:
            termDocumentFreq = 0
        return termDocumentFreq
    
    # Set Term document frequency
    def setTermDocumentFreq(self, term, postings):
        termData = self.document_term_freq[term]
        if not termData:
            self.document_term_freq[term] = postings