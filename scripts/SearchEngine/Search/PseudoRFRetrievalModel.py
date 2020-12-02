import Search.QueryRetreivalModel as QueryRetreivalModel
import Classes.Document as Document
from operator import attrgetter
from collections import defaultdict

class PseudoRFRetreivalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.qrm = QueryRetreivalModel.QueryRetrievalModel(ixReader)
        
        # Get the corpus length
        self.length =0
        for i in range(self.indexReader.getDocumentCount()):
             self.length +=self.indexReader.getDocLength(i) 
        
        # Set the parameter value
        self.mu = 2000
        
        return

    # Search for the topic with pseudo relevance feedback.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # query: The query to be searched for.
    # TopN: The maximum number of returned document
    # TopK: The count of feedback documents
    # alpha: parameter of relevance feedback model
    # return TopN most relevant document, in List structure

    def retrieveQuery(self, query, topN, topK, alpha):
        # this method will return the retrieval result of the given Query, and this result is enhanced with pseudo relevance feedback
        # (1) you should first use the original retrieval model to get TopK documents, which will be regarded as feedback documents
        # (2) implement GetTokenRFScore to get each query token's P(token|feedback model) in feedback documents
        # (3) implement the relevance feedback model for each token: combine the each query token's original retrieval score P(token|document) with its score in feedback documents P(token|feedback model)
        # (4) for each document, use the query likelihood language model to get the whole query's new score, P(Q|document)=P(token_1|document')*P(token_2|document')*...*P(token_n|document')

        # get P(token|feedback documents)
        TokenRFScore={}
        queries_result=query.getQueryContent().split()
        TokenRFScore = self.GetTokenRFScore(query, topK)
#        print(TokenRFScore)
        self.document_result=defaultdict(int)
        for word in queries_result:
            posting_list=self.indexReader.getPostingList(word)
            self.indexReader.setTermDocumentFreq(word,posting_list)
            for document_id in  posting_list.keys():
                self.document_result[document_id]=Document.Document()
                self.document_result[document_id].setDocNo(self.indexReader.getDocNo(document_id))
                self.document_result[document_id].setDocTitle(self.indexReader.getDocTitle(document_id))
                self.document_result[document_id].setScore(self.dirichletSmoothMethPseudo(queries_result,document_id,alpha,TokenRFScore))
                self.document_result[document_id].setDocId(document_id)
        return [doc for doc in sorted(self.document_result.values(), key=attrgetter('score'), reverse = True)][:topN]
    
    def dirichletSmoothMethPseudo(self, queries, document_id,alpha,TokenRFScore):
        doc_score = 1.0 
        alphaminus=1-alpha
        document_len = self.indexReader.getDocLength(document_id)
        document_len_adj = document_len + self.mu
        adj_length=self.mu/self.length
        for word in queries:
            Collection_freq = self.qrm.getTermCorpusFreq(word)
            if Collection_freq:
                docTermFrequency = self.indexReader.getTermDocumentFreq(word, document_id)
                doc_score *=  alpha*((docTermFrequency + adj_length * Collection_freq)/document_len_adj)+(alphaminus*TokenRFScore[word])
        return doc_score
    
    

    def GetTokenRFScore(self, query, topK):
        # for each token in the query, you should calculate token's score in feedback documents: P(token|feedback documents)
        # use Dirichlet smoothing
        # save {token: score} in dictionary TokenRFScore, and return it
        TokenRFScore={}
        
        feedbackDocs = self.qrm.retrieveQuery(query, topK)
        queryTerms = query.getQueryContent().split()
        psuedo_doc_length = self.PsuedoDocLength(feedbackDocs)
        adjustedLength = psuedo_doc_length + self.mu
        adj_length=self.mu/self.length      
        for term in queryTerms:
            Collection_freq = self.qrm.getTermCorpusFreq(term)
            if Collection_freq:
               pseudoDocTermFrequency = self.PsuedoTermDocFreq(term, feedbackDocs)
               TokenRFScore[term] =(pseudoDocTermFrequency + (adj_length * Collection_freq))/adjustedLength
            else:
                TokenRFScore[term] = 0
        return TokenRFScore

    def PsuedoDocLength(self, feedbackDocs):
        document_length = 0
        for doc in feedbackDocs:
            document_length += self.indexReader.getDocLength(doc.getDocId())
        return document_length
    
    def PsuedoTermDocFreq(self, term, feedbackDocs):
        document_freq = 0
        for doc in feedbackDocs:
            document_freq +=  self.indexReader.getTermDocumentFreq(term, doc.getDocId())
        return document_freq
            
        
        
        
