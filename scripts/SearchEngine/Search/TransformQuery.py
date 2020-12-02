import Classes.Query as Query
import BagOfWords.GenerateBagOfWords as Normalizer


class TransformQuery:

    def __init__(self):
        self.normalizer = Normalizer.BagOfWords()
        return

    # Return extracted queries with class Query in a list.
    def getQuries(self,q):
        self.q = q
        queries=[]
        aQuery=Query.Query()
        aQuery.setQueryId("1")
        aQuery.setQueryContent(self.transformQuery(self.q))
        queries.append(aQuery)

        return queries
    
    def transformQuery(self, text):
        tokens = self.normalizer.tokenize(text)
        stopwords_removed = self.normalizer.remove_stopwords(tokens)
        lemmatized = self.normalizer.word_lemmatizer(stopwords_removed)
        stemmed = self.normalizer.word_stemmer(lemmatized)
        return stemmed
        