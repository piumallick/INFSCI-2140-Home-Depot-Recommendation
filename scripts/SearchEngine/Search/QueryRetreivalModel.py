import Classes.Query as Query
import Classes.Document as Document
from collections import OrderedDict
from collections import defaultdict

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        
        # Length of the entire corpus
        docCount = self.indexReader.getDocumentCount()
        #print("docCount: ", docCount)
        self.corpusLength = self.calc_coll_len(docCount)
        
        # Set the parameter value
        self.muVal = 2000
        
        # Define Cache Dictionaries
        self.termCorpusFreq = defaultdict(int)
        self.termDocumentFreq = defaultdict(dict)
        self.documentLength = defaultdict(int)
        
        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        # Get matching documents
        queryTokens = query.getQueryContent().split()
        
        # Store documents in a dictionary
        documents = defaultdict(int)
        
        # Extract Unique Documents
        for term in queryTokens:
            postings = self.getPostings(term)
            self.setTermDocumentFreq(term, postings)
            for docId in postings.keys():
                documents[docId] = ""
        
        for docId in documents.keys():

            # Calculate score            
            score = self.dirichletSmoothing(queryTokens, docId)
            
            # Populate a new document
            newDoc = Document.Document()
            newDoc.setDocId(docId)
            newDoc.setDocNo(self.indexReader.getDocNo(docId))
            newDoc.setDocTitle(self.indexReader.getDocTitle(docId))
            newDoc.setScore(score)
            
            documents[docId] = newDoc
        
        return [v for v in sorted(documents.values(), key=lambda doc: doc.getScore(), reverse = True)][:topN]
    
    # Query likelihood language model
    def dirichletSmoothing(self, terms, docId):
        score = 1.0 # Default the score to 1
        docLength = self.getDocumentLength(docId)
        adjustedLength = docLength + self.muVal
        
        l1 = docLength / adjustedLength
        r1 = self.muVal / adjustedLength
        
        for term in terms:
            termCorpusFreq = self.getTermCorpusFreq(term)
            if termCorpusFreq:
                docTermFrequency = self.getTermDocumentFreq(term, docId)
                l2 = docTermFrequency / docLength
                r2 = termCorpusFreq / self.corpusLength
                score = score * (l1 * l2 + r1 * r2)
        return score
    
    # Term Corpus Frequency
    def getTermCorpusFreq(self, term):
        if term in self.termCorpusFreq:
            termFreq = self.termCorpusFreq[term]
        else:
            termFreq = self.indexReader.CollectionFreq(term)
            self.termCorpusFreq[term] = termFreq
        return termFreq
    
    # Document Length
    def getDocumentLength(self, docId):
        docLength = self.documentLength[docId]
        if not docLength:
            docLength = self.indexReader.getDocLength(docId)
            self.documentLength[docId] = docLength
        return docLength
    
    # Term Document Frequency
    def getTermDocumentFreq(self, term, docId):
        try:
            termDocumentFreq = self.termDocumentFreq[term][docId] 
        except KeyError:
            termDocumentFreq = 0
        return termDocumentFreq
    
    # Set Term document frequency
    def setTermDocumentFreq(self, term, postings):
        termData = self.termDocumentFreq[term]
        if not termData:
            self.termDocumentFreq[term] = postings
          
    # Get term postings
    def getPostings(self, term):
        return self.indexReader.getPostingList(term)
    
    # Calculate number of terms in the corpus
    def calc_coll_len(self, doc_count):
        coll_len = 0
        for i in range(doc_count):
            coll_len = coll_len + self.indexReader.getDocLength(i)
        return coll_len
    
    # Return the corpus length
    def getCorpusLength(self):
        return self.corpusLength