##..... Lexical Analyzer for Domain Specific Languages ..............................##
##..... Rules can be easily customized to recognize tokens for desired language .....##
##..... Program written in Python 2.7 ...............................................##

import sys
import re
from collections import defaultdict
from os.path import exists
import pdb

# Regex rules for matching different types of tokens
rules = [																														
			(r'[\"][^\"]*?[\"]|[\'][^\']*?[\']',																		    					'LITERAL: STRING'),
			(r'\-?\b\d*\.\d+\b',												    							 								'LITERAL: DOUBLE'),
			(r'\-?\b\d+\b',												     																	'LITERAL: INT'),
			(r'\bint\b|\bdouble\b|\bbool\b|\bstruct\b|\bchar\b|\bstring\b',																		'KEYWORD: ELEMENTARY DATATYPE'),
			(r'\bvector\b|\bset\b|\btree\b|\blist\b|\bqueue\b|\bstack\b|\bdataContainer\b|\bmodel\b|\btestResults\b|\bclassificationModel\b',	'KEYWORD: COMPLEX DATATYPE'),
			(r'\bprintf\b|\bscanf\b|\bsigma\b|\bsigmoid\b|\bexp\b|\bconnect\b',																	'KEYWORD: STANDARD FUNCTION'),
			(r'\btrainModel\b|\btestModel\b|\bclassify\b|\bloadModelFromFile\b|\bsaveModelToFile\b|\bclassifyFromFile\b',						'KEYWORD: MODEL FUNCTION'),
			(r'\bget\b|\bput\b|\bpost\b|\bdelete\b',																							'KEYWORD: HTTP FUNCTION'),
			(r'\bfor\b|\bwhile\b|\bdo\b|\buntilConverge\b|\brange\b|\biterator\b',																'KEYWORD: ITERATION'),
			(r'\bif\b|\belse\b|\bswitch\b|\bcase\b|\bcontinue\b|\bbreak\b|\breturn\b|\bin\b',													'KEYWORD: DECISION/BRANCH STATEMENT'),
			(r'\baudio\b|\bimage\b|\bcsv\b|\btxt\b|\bxls\b',																					'KEYWORD: EXTENDED TYPE'),
			(r'\bANN\b|\bRGD\b|\bnaiveBayes\b|\bKNN\b',																							'KEYWORD: MODEL TYPE'),
			(r'\bfrom\b|\bimport\b|\bvoid\b|\btrue\b|\bfalse\b|\bnonBlocking\b|\bdatabase\b',													'KEYWORD: OTHERS'),		
			(r'\+\+|\-\-|\^\=|\|\||\&\&|\!\=|\=\=|\?|\:\=',                   																	'OPERATORS: COMPLEX'),
			(r'\-|\+|\/|\*|\^|\||\&|\=|\<|\>|\!',                   																			'OPERATORS: SIMPLE'),
			(r'\{|\}|\[|\]|\(|\)|\;|\,|\.|\:',                                                         											'DELIMITERS'),   
			(r'(?<=\s)[a-zA-Z][a-zA-Z0-9_]*',                                                            										'IDENTIFIERS')
]

# Function to identify tokens in given code and store output in outputfile
def lexicalAnalyzer(code, outputFile):

	# removing multi-line comments
	multiLineComments = re.compile('\/\*(.|\s)*?\*\/') 						# regex for matching C style multiline comments
	while multiLineComments.search(code) is not None:
		mlc = multiLineComments.search(code)		   						# mlc contains first occurence of multiline comment in the code
		linesInComment = 0
		if mlc != None:
			mlc = mlc.group()
			linesInComment = len(re.findall('\n',mlc)) 						# finding no. of lines spanned by multiline comment mlc
		code = multiLineComments.sub(" %s"%('\n'*linesInComment), code, 1) 	# replacing the multiline comment by its line span

	# removing single-line comments
	singleLineComments = re.compile('\/\/(.*)')								# regex for matching C style single line comments
	code = singleLineComments.sub(' ', code) 								# replacing all single line comments with a whitespace

	tokens = defaultdict(lambda: defaultdict(list)) 						# tokens[tokenType][lineNumber] is a list of tokens of tokenType in lineNumber
	# getting all tokens in every line
	lines = code.split('\n')												# lines is a list of lines in the code
	currentLine = 1															# starting with line number 1
	for line in lines:
		linecode = ' ' + line 												# adding a whitespace before every line for easily matching identifiers
		for rule, tokenType in rules:
			tokens[tokenType][currentLine] = re.findall(rule, linecode)		# for every rule in rules list(line 12), storing all matches in dictionary
			substitute = re.compile(rule)
			linecode = substitute.sub(' ', linecode)						# replacing the matches with a whitespace in the code(line code)
		linecode = linecode.strip()
		if linecode != '':													# if linecode is not empty after stripping whitespace, the
			tokens['Lexical Errors'][currentLine] = [linecode]				# remaining content has not matched any rule of the language and is a lexical error
		currentLine = currentLine + 1

	
	output = open(outputFile, 'w')
	# Warning: output file opened in 'w' mode, will overwrite any file with same name in working directory


	# writing all tokens category wise arranged by line no. into the output file
	for rule, tokenType in rules:
		output.write('%r:\n' % tokenType)
		pos = output.tell()
		for i in range(1, currentLine):
			if tokens[tokenType][i] != []:
				output.write('\tIn line %d: %r \n' % (i, ','.join(map(str, tokens[tokenType][i]))))
		if pos == output.tell():
			output.write("\tNONE\n")

	# writing lexical errors to output file
	output.write('LEXICAL ERRORS:\n')
	pos = output.tell()
	for i in range(1, currentLine):
			if tokens['Lexical Errors'][i] != []:
				output.write('\tIn line %d: %r \n' % (i, ','.join(map(str, tokens['Lexical Errors'][i]))))
	if pos == output.tell():
		output.write("\tNONE")
	output.close()
	return


def main():
	print "Enter filename to be analyzed or 0 to exit"
	filename = raw_input("> ")
	while filename != '0':
		# checking for existence of file
		while exists(filename) == False :
			print "File '%s' does not exist. Don't forget to enter complete path of the file if not in the same directory" % filename
			print "Renter filename or press 0 to exit"
			filename = raw_input("> ")
			if filename == '0':
				exit(0)


		fileHandle = open(filename)	# code contains file to be analyzed
		code = fileHandle.read() # copying contents of file
		fileHandle.close()	# closing file
		outputFile = raw_input('Enter name of output file:')
		print "Now tokenizing code"
		lexicalAnalyzer(code, outputFile)
		print "Results of lexical analysis stored in %s" % outputFile
		print "Enter one more filename to be analyzed or 0 to exit"
		filename = raw_input("> ")

if __name__ == '__main__':
	main()