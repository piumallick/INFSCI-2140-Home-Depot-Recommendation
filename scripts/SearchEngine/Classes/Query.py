class Query:

    def __init__(self):
        return

    queryContent = ""
    queryId = ""

    def getQueryContent(self):
        return self.queryContent

    def getQueryId(self):
        return self.queryId

    def setQueryContent(self, content):
        self.queryContent=content

    def setQueryId(self, id):
        self.queryId=id