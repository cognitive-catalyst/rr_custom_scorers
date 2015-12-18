"""
    Scorers that extract statistics related to the size of the document
    These scorers are useful in situations where you want to bias the system
    against or in favor of documents of a certain length.

    For example, if all of the documents are of medium length (i.e. relevant
    documents are never short or long), then, ideally, the ranker would learn
    to prefer medium length documents to short or long documents
"""

# Metadata
__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'

# Local imports
from document_scorer import DocumentScorer

# 3rd party imports
from spacy.en import English


class TotalDocumentWordsScorer(DocumentScorer):

	def __init__(self, name='DocumentScorer', short_name='ds', description='Description of the scorer',
				 include_stop=False):
		""" Base class for any scorers that consume a Solr document and extract
			a specific signal from a Solr document

			Args:
				name (str): Name of the Scorer
				short_name (str): Used for the header which is sent to ranker
				description (str): Description of the scorer
		"""
		super(TotalDocumentWordsScorer, self).__init__(name=name, short_name=short_name, description=description)
		self.nlp_ = English()
		self.include_stop_words_ = include_stop

	def score(self, document):
		"""	Number of total words in a document. This is intended to be used as a fuzzy way to filter out
			useless documents

			Args:
				document (dict): Contents of the solr document. The fields in the dictionary correspond
				to the different fields in the Solr Document
		"""
		text = document['text']
		doc = self.nlp_(unicode(text))
		total_words = 0
		for token in doc:
			if not token.is_stop:
				total_words += 1
			elif self.include_stop_words_:
				total_words += 1
		return total_words
# endclass DocumentSizeScorer
