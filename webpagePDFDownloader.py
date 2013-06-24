#!/usr/bin/python

import sys, getopt, urllib2, os, shutil

# sudo apt-get install python-bs4
from bs4 import BeautifulSoup

def main(argv):
  scriptName = os.path.basename(__file__)
	usage = 'Usage: ' + scriptName + ' -u <URL>'
	try:
		opts, args = getopt.getopt(argv,"hu:",["url="])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	if not opts:
		print usage
		sys.exit()
	for opt, arg in opts:
		if opt in ("-u", "--url"):
			dlPDFs(arg)
		else: 
			print usage 
			sys.exit()
		 
def dlPDFs(url):
	# PDFs directory
	pdfsDir = 'pdfs'

	# Get domain
	domain = url.rpartition('/')[0]
	
	# Get html
	htmlDoc = urllib2.urlopen(url).read()
	soup = BeautifulSoup(htmlDoc)
	shutil.rmtree(pdfsDir, 1)
	os.makedirs(pdfsDir)
	for a in soup.find_all('a'):
		if 'href' in a.attrs:
			href = a['href']
			if href.endswith('.pdf'):
				print 'Downloading ' + href
				u = urllib2.urlopen(domain + '/' + href)
				decompHref = href.rpartition('/')
				if not decompHref[1]:
					href = decompHref[0]
				else:
					href = decompHref[2]
				pdfFile = open(pdfsDir + '/' + href, 'w')
				pdfFile.write(u.read())
				pdfFile.close()
				print 'Saved ' + pdfsDir + '/' + href
	print 'Done!'
	
if __name__ == "__main__":
   main(sys.argv[1:])
