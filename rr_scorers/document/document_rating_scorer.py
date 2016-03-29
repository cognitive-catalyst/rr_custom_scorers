__author__ = 'lkrishna'
from document_scorer import DocumentScorer

# Scorer to score to compute the popularity of a post/document using number of views and answers provided
class PopularityScorer(DocumentScorer):

    def __init__(self, name='DocumentScorer', short_name='ds', description='Description of the scorer',
                 include_stop=False):
        """ Base class for any scorers that consume a Solr document and extract
            a specific signal from a Solr document

            Args:
                name (str): Name of the Scorer
                short_name (str): Used for the header which is sent to ranker
                description (str): Description of the scorer
        """
        super(PopularityScorer, self).__init__(name=name, short_name=short_name, description=description)

    def score(self, document):
        views = document['views']
        accepted = document['accepted']

        if views is not None:
            # if no views, then assuming it is a low rating
            if views < 0:
                return 0
            elif 100 < views <= 2000 and accepted <0:
                return 0.25
            elif 0 < views <= 2000 and accepted > 0:
                return 0.5
            elif 2000 < views <= 5000 and accepted > 0:
                return 0.75
            elif views > 5000 and accepted > 0:
                return 1