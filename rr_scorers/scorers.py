"""
    Scorers to handle    
"""

# Metadata
__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'

# Local imports
import utils
from document import document_scorer as ds
from query import query_scorer as qs
from query_document import query_document_scorer as qds
import scorer_exception as se

# Runtime imports
import sys
import os
from concurrent import futures
import time

# 3rd party imports
import numpy as np


class Scorers(object):

    def __init__(self, feature_json_file, timeout=10, max_workers=10):
        """
            Pipeline that manages scoring of multiple custom feature scorers
            This is the API that almost all scorers will access when training \
                a Retrieve & Rank instance with custom features

            args:
                feature_json_file (str): Path to a feature configuration file. \
                    This file defines the pipeline of custom scorers used
            raise:
                se.ScorerConfigurationException : If any of the individual scorers raise during configuration, \
                    If the file feature_json_file cannot be found or is not of the proper type
        """
        scorer_dict = utils.load_from_file(feature_json_file)
        self._document_scorers = scorer_dict.get('document', [])
        self._query_scorers = scorer_dict.get('query', [])
        self._query_document_scorers = scorer_dict.get('query_document', [])
        self._timeout = timeout
        self._interval = 0.1
        self._thread_executor = futures.ThreadPoolExecutor(max_workers)

    def get_headers(self):
        " Get the custom headers "
        headers = list()
        headers.extend([scorer.short_name for scorer in self._document_scorers])
        headers.extend([scorer.short_name for scorer in self._query_scorers])
        headers.extend([scorer.short_name for scorer in self._query_document_scorers])
        return headers

    def get_required_fields(self):
        " Get the required fields for the underlying scorers "
        required_fields = list()
        for qs in self._query_scorers:
            required_fields.extend(qs.get_required_fields())
        for qds in self._query_document_scorers:
            required_fields.extend(qds.get_required_fields())
        return list(set(required_fields))

    def _score(self, scorer, *args, **kwargs):
        """ Score an individual item
            args:
                scorer (Scorer) : Scorer object
                args (list)     : List of additional unnamed args
                kwargs (dict)   : Dictionary of additional named args
            raise:
                se.ScorerRuntimeException : If scorer fails along the way
                se.ScorerTimeoutException : If scorer times out
            return:
                score (float) : Score
        """
        f = None
        try:
            f = self._thread_executor.submit(scorer.score, *args, **kwargs)
            return f.result(timeout=self._timeout)
        except futures.TimeoutError, e:
            if f is not None:
                f.cancel()
            raise se.ScorerTimeoutException('Scorer %r timed out', args, kwargs)
        except se.ScorerRuntimeException, e:
            raise e

    def scores(self, query, doc):
        """
            Score the query/document pair using all registered scorers

            args:
                query (dict): Dictionary containing contents of the query
                doc (dict): Dictionary containing contents of individual Solr Doc
            raises:
                se.ScorerRuntimeException: If there are any issues scoring \
                    individual query/document pairs
            returns:
                vect (numpy.ndarray): Numpy array containing the feature vectors
        """
        vect = list()

        # Score the docs
        for document_scorer in self._document_scorers:
            score = self._score(document_scorer, doc)
            vect.append(score)

        # Score the queries
        for query_scorer in self._query_scorers:
            score = self._score(query_scorer, query)
            vect.append(score)

        # Score the query-document pairs
        for query_document_scorer in self._query_document_scorers:
            score = self._score(query_document_scorer, query, doc)
            vect.append(score)

        return np.array(vect)
# endclass Scorers
