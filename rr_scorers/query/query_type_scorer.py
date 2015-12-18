"""
	Contains scorers which capture properties of the queryType
	Example:
		- KeywordConfidenceScorer scores (from 0 to 1) the extent to which a query looks like a keyword
		- PolarQueryScorer scores (from 0 to 1) the extent to which a question is a Yes/No question
"""

__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'

# Local imports
import query_scorer

# Runtime imports
import re

# 3rd party imports
from spacy.en import English


class ProperNounRatioScorer(query_scorer.QueryScorer):

	def __init__(self, name='ProperNounRatioScorer', short_name='pnrs', description='Proper Noun Ratio Scorer',
					nlp=None):
		"""
			Class that computes the ratio of proper nouns in a query
			The idea is that a query with a large fraction of proper nouns will tend to be a keyword query

			Args:
				name, short_name, description (str): See query_scorer.QueryScorer
				nlp (spacy.en.English): Tokenizes incoming text
		"""
		super(ProperNounRatioScorer, self).__init__(name=name, short_name=short_name, description=description)
		if nlp:
			self.nlp_ = nlp
		else:
			self.nlp_ = English()

	def score(self, query):
		"""
			Computes the fraction of proper nouns in the underlying query text
		"""
		query_text = query['q']
		doc = self.nlp_(unicode(query_text))
		num_proper_nouns = 0
		for token in doc:
			if re.match('^NNP.*$', token.tag_):
				num_proper_nouns += 1
		return num_proper_nouns / float(len(doc))
#endclass ProperNounRatioScorer
