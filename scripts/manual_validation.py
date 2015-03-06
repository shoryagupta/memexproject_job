import os
import random
from os import walk
from BeautifulSoup import BeautifulSoup,Comment

def extract(page):
    soup = BeautifulSoup(page)
    soup = soup.find('html')
    if soup != None:
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))     #removing comments from page
        [comment.extract() for comment in comments]
        for elem in soup.findAll(['script','style']):
           elem.extract()
        text = soup.getText()
        print text
	del(text)

def getfilelist(target):
    mypath = ""
    files = []
    list = []
    for [path, dirnames, filenames] in walk(target):
        for dname in dirnames:
            mypath = target+dname
            for [p,d,f] in walk(mypath):
		for f1 in f:
                    files.append(target+dname+'/'+f1)
    return(files)

target = "/home/vgc/shorya_gupta/ache/data/data_target/"
filelist = getfilelist(target)
filelist = random.sample(filelist,20)
#print filelist
relev = 'y'
for x in filelist:
    try:
	print x
        htmlFile = open(x,'r')
        html = htmlFile.read()
        extract(html)
        htmlFile.close()
	relev = raw_input("Is the file relevant? [y/n]: ")
	text = open("/home/vgc/shorya_gupta/scripts/text.txt",'ab+')
	if relev == 'y':
	    text.write("File: "+x+" : Relevant")
	else:
	    text.write("File: "+x+" : Irrelevant")
	text.close()
    except IOError as e:
	print e
