Python-lexical-analyzer
=======================

Program identifies tokens in given code based on certain rules.

Rules for identifying different tokens are written as regex expressions. These are stored as a list of tuples of the form (regex, token type).

The function lexicalAnalyzer takes in code to be analyzed and name of output file.