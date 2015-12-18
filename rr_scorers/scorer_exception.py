"""
    Define exceptions to be used by various services.

    ScorerConfigurationException: Raised if a Scorer is improperly configured
    ScorerRuntimeException: Raised if a Scorer has a runtime error
"""

# Metadata
__author__ = 'Vincent Dowling'
__email__ = 'vdowlin@us.ibm.com'


class ScorerConfigurationException(Exception):
    def __init__(self, message):
        """ Wrapper exception for configuration issues. Should be raised if:
                1) Inputs to the constructor of a scorer are bad,
                2) Invariant to scorer is violated
                etc.
        """
        super(ScorerConfigurationException, self).__init__(message)
# endclass ScorerConfigurationException


class ScorerRuntimeException(Exception):
    def __init__(self, message):
        """ Wrapper exception for general runtime issues for a scorer. Should be raised if:
                1) Input to an api method (likely .score) is invalid
                2) Unforeseen problems prevent properly scoring a query, document, query/document pair
        """
        super(ScorerRuntimeException, self).__init__(message)
# endclass ScorerRuntimeException


class ScorerTimeoutException(ScorerRuntimeException):
    def __init__(self, message, args, kwargs):
        """ Should be raised if a scorer times out
        """
        super(ScorerTimeoutException, self).__init__(message)
        self._args = args
        self._kwargs = kwargs
#endclass ScorerTimeoutException
