class Document:

    def __init__(self):
        return

    docid = ""
    docno = ""
    docTitle = ""
    score = 0.0

    def getDocId(self):
        return self.docid

    def getDocNo(self):
        return self.docno

    def getScore(self):
        return self.score
    
    def getDocTitle(self):
        return self.docTitle

    def setDocId(self, docid):
        self.docid = docid

    def setDocNo(self, no):
        self.docno = no

    def setScore(self, the_score):
        self.score = the_score
    
    def setDocTitle(self, docTitle):
        self.docTitle = docTitle
