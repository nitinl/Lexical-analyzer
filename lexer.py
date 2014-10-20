##..... PPL Assignment by Nitin(2012A7PS038P) and Pavan(2012C6PS331P) .....##
##..... Lexical Analyzer for Classification Domain Specific Language  .....##

import sys
import re
from collections import defaultdict
from os.path import exists
import pdb

# Rules for tokenizing
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

def lexicalAnalyzer(code, outputfile):

	# removing multi-line comments
	multiLineComments = re.compile('\/\*(.|\s)*?\*\/')
	while multiLineComments.search(code) is not None:
		mlc = multiLineComments.search(code)
		linesInComment = 0
		if mlc != None:
			mlc = mlc.group()
			linesInComment = len(re.findall('\n',mlc))
		code = multiLineComments.sub(" %s"%('\n'*linesInComment), code, 1)

	# removing single-line comments
	singleLineComments = re.compile('\/\/(.*)')
	code = singleLineComments.sub(' ', code)

	tokens = defaultdict(lambda: defaultdict(list)) 	# tokens is a dictionary(token type) of a dictionary(line number) of list(token values)
	# getting all tokens in every line
	lines = code.split('\n')
	currentLine = 1
	for line in lines:
		linecode = ' ' + line
		for rule, tokenType in rules:
			tokens[tokenType][currentLine] = re.findall(rule, linecode)
			substitute = re.compile(rule)
			linecode = substitute.sub(' ', linecode)
		linecode = linecode.strip()
		if linecode != '':
			tokens['Lexical Errors'][currentLine] = [linecode]
			# pdb.set_trace()
		currentLine = currentLine + 1

	p = re.compile(r'\.')
	outputfile = p.sub('Output.',outputfile)
	output = open(outputfile, 'w')
	for rule, tokenType in rules:
		output.write('%r:\n' % tokenType)
		pos = output.tell()
		for i in range(1, currentLine):
			if tokens[tokenType][i] != []:
				output.write('\tIn line %d: %r \n' % (i, ','.join(map(str, tokens[tokenType][i]))))
		if pos == output.tell():
			output.write("\tNONE\n")

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
		lexicalAnalyzer(code, filename)
		print "Enter one more filename to be analyzed or 0 to exit"
		filename = raw_input("> ")

if __name__ == '__main__':
	main()