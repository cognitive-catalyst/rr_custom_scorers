"""
	Utilities to be used
"""

__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'

# Local imports
import json
import os
import importlib
from collections import defaultdict
import sys


# Local imports
from document import document_scorer
from query import query_scorer
from query_document import query_document_scorer


def load_from_file(features_json_path):
	"""
		Load classes from a configuration file. Configuration files must be of the following format:
		{
		  "scorers":[
			{
			  "init_args":{
				"name":"TotalDocWordsMinusStop",
				"short_name":"tdw",
				"description":"Compute the number of total words in a Solr document, less the stop words",
				"include_stop":false
			  },
			  "type":"document",
			  "module":"document_size_scorer",
			  "class":"TotalDocumentWordsScorer"
			}
		  ]
		}

		Args:
			features_json_path (str): Path to a configuration file

		Raise:
			If scorer fails to load
			If more than one scorer has the same short name
			If scorer of a certain type does not subclass the proper module
	"""
	if not type(features_json_path) is str:
		raise ValueError('Path %r is not a string' % features_json_path)
	elif not os.path.isfile(features_json_path):
		raise ValueError('Path %s was not found' % features_json_path)
	elif not features_json_path.endswith('json'):
		raise ValueError('Path %s is not a json file' % features_json_path)
	else:
		features_json_obj = json.load(open(features_json_path))
		scorer_dict = defaultdict(list)
		short_names = defaultdict()
		for scorer_info in features_json_obj['scorers']:
			" Create an instance of the scorer "
			doc_type, module_name, class_name = scorer_info['type'], scorer_info['module'], scorer_info['class']
			init_args = scorer_info['init_args']
			full_module_name = "rr_scorers.%s.%s" % (doc_type, module_name)
			obj = instantiate(full_module_name, class_name, init_args)

			" Raise if multiple short names"
			if obj.short_name in short_names:
				raise ValueError('Scorers with name=%s and name=%s have the same short_name=%s' %
								 (obj.name, short_names[obj.short_name], obj.short_name))
			short_names[obj.short_name] = obj.name

			" Validate scorer is properly subclassed "
			if doc_type == 'document':
				if isinstance(obj, document_scorer.DocumentScorer):
					scorer_dict['document'].append(obj)
				else:
					raise ValueError('Scorer=%r of type %s is not properly subclassed' % (obj, doc_type))
			elif doc_type == 'query':
				if isinstance(obj, query_scorer.QueryScorer):
					scorer_dict['query'].append(obj)
				else:
					raise ValueError('Scorer=%r of type %s is not properly subclassed' % (obj, doc_type))
			elif doc_type == 'query_document':
				if isinstance(obj, query_document_scorer.QueryDocumentScorer):
					scorer_dict['query_document'].append(obj)
				else:
					raise ValueError('Scorer=%r of type %s is not properly subclassed' % (obj, doc_type))
			else:
				raise ValueError('Scorer with name=%s is not of type "document", "query" or "query_document"')
		return scorer_dict


def instantiate(module_name, cls_name, init_args):
	" Load in a class. Raise if the loading fails or the object is not of the correct type "
	module = importlib.import_module(module_name)
	cls = getattr(module, cls_name)
	return cls(**init_args)
