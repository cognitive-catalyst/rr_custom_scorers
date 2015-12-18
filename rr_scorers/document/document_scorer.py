"""
	Contains the class DocumentScorer, which is the base class for all scorers that:
		(1) Extract a specific signal from a single Solr Document
		(2) Want to be registered by the service as scorers

	All subclasses of DocumentScorer must override the score(doc) method, where
	doc contains the different fields for a given Solr Document
"""
__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'

# 3rd party imports
from spacy.en import English

# Local imports
from .. import scorer_exception as se


class DocumentScorer(object):

	def __init__(self, name='DocumentScorer', short_name='ds', description='Description of the scorer'):
		""" Base class for any scorers that consume a Solr document and extract
			a specific signal from a Solr document

			args:
				name (str): Name of the Scorer
				short_name (str): Used for the header which is sent to ranker
				description (str): Description of the scorer
			raise:
				ValueError : If name, short_name or description is not "string"-like
		"""
		if type(name) is not str or type(name) is not unicode:
			raise se.ScorerConfigurationException('Scorer name = %r is not "string"-like' % name)
		self.name_ = name

		if type(short_name) is not str or type(short_name) is not unicode:
			raise se.ScorerConfigurationException('Scorer short_name = %r is not "string"-like' % short_name)
		self.short_name_ = short_name

		if type(description) is not str or type(description) is not unicode:
			raise se.ScorerConfigurationException('Scorer description = %r is not "string"-like' % description)
		self.description_ = description

	@property
	def name(self):
		return self.name_

	@property
	def short_name(self):
		return self.short_name_

	@property
	def description(self):
		return self.description_

	def get_required_fields(self):
		"""
			Get the required fields from the Solr document
			args:
				None
			return:
				List : Return a list of the required fields
		"""
		raise NotImplementedError

	def score(self, document):
		"""	Number of total words in a document. This is intended to be used as a fuzzy way to filter out
			useless documents

			args:
				document (dict): Contents of the solr document. The fields in the dictionary correspond
				to the different fields in the Solr Document
		"""
		raise NotImplementedError
#endclass DocumentScorer
