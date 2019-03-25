'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''
import sys
import time
#from importlib import reload
#reload(sys)
#sys.setdefaultencoding('utf8')

dirPath = './copyleaks'
if dirPath not in sys.path:
    sys.path.insert(0, dirPath)

from app.plagiarism.copyleaks.copyleakscloud import CopyleaksCloud
from app.plagiarism.copyleaks.processoptions import ProcessOptions
from app.plagiarism.copyleaks.product import Product

"""
An example of using the Copyleaks Python SDK and checking for status and reciving the results.
"""
def checkPlagiarism(string):
	"""
	Change to your account credentials.
	If you don't have an account yet visit https://copyleaks.com/Account/Register
	Your API-KEY is available at your dashboard on http://api.copyleaks.com of the product that you would like to use.
	Currently available products: Businesses, Education and Websites.
	"""

	cloud = CopyleaksCloud(Product.Businesses, 'mt476@uowmail.edu.au', '55B759BB-3FF2-4D7B-9644-5E3E8DC2BAC0')

	print("You've got %s Copyleaks %s API credits" % (cloud.getCredits(), cloud.getProduct())) #get credit balance

	options = ProcessOptions()
	"""
	Add this process option to your process to use sandbox mode.
	The process will not consume any credits and will return dummy results.
	For more info about optional headers visit https://api.copyleaks.com/documentation/headers
	"""
	options.setSandboxMode(True)
	# Available process options
#     options.setHttpCallback("http://yoursite.here/callback")
#     options.setHttpInProgressResultsCallback("http://yoursite.here/callback/results")
#     options.setEmailCallback("Your@email.com")
#     options.setCustomFields({'Custom': 'field'})
#     options.setAllowPartialScan(True)
#     options.setCompareDocumentsForSimilarity(True)  # Available only on compareByFiles
#     options.setImportToDatabaseOnly(True)  # Available only on Education API

	print("Submitting a scan request...")
	"""
	Create a scan process using one of the following methods.
	Available methods:
	createByUrl, createByOcr, createByFile, createByText and createByFiles.
	For more information visit https://api.copyleaks.com/documentation
	"""
	# process = cloud.createByUrl('https://copyleaks.com', options)
	# process = cloud.createByOcr('ocr-example.jpg', eOcrLanguage.English, options)
	# process = cloud.createByFile('test1.txt')
	process = cloud.createByText(string.encode("utf-8"))
	# processes, errors = cloud.createByFiles(['path/to/file1', 'path/to/file2'], options)

	print ("Submitted. In progress...")
	iscompleted = False
	while not iscompleted:
		# Get process status
		[iscompleted, percents] = process.isCompleted()
		print ('%s%s%s%%' % ('#' * int(percents / 2), "-" * (50 - int(percents / 2)), percents))
		if not iscompleted:
			time.sleep(2)

	# Get the scan results
	urls = []
	results = process.getResults()
	for result in results:
		if "Copyleaks internal database" in result.getTitle():
			continue
		urls.append(result.getEmbededComparison())
	return urls
			# Optional: Download result full text. Uncomment to activate
			# print ("Result full-text:")
			# print("*****************")
			# print(process.getResultText(result))

			# Optional: Download comparison report. Uncomment to activate
			#print ("Comparison report:")
			#print("**************")
			#print (process.getResultComparison(result))

		# Optional: Download source full text. Uncomment to activate.
		#print ("Source full-text:")
		#print("*****************")
		#print(process.getSourceText())
