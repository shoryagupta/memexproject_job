from os import walk
from bs4 import BeautifulSoup

mypath = "/home/vgc/shorya_gupta/ache/data/data_target/"
for dirpath, dirnames, filenames in walk(mypath):
    for d in dirnames:
	mypath = mypath + '/' + d
	for (dir, dirm, fname) in walk(mypath):
	    for f in fname:
		try:
            	htmlFile = open(f,'r')
           	html = htmlFile.read()
            	soup = BeautifulSoup(html)
            	soup = soup.find('html')
            	    if soup != None:
                	comments = soup.findAll(text=lambda text:isinstance(text, Comment))     #removing comments from page
                	[comment.extract() for comment in comments]
                	for elem in soup.findAll(['script','style']):
			    elem.extract()
                    	    text = soup.getText()
                    	    if text.find("ebola",0,len(text)) != -1 :
				x+=1
			    elif text.find("ebola",0,len(text)) != -1 :
                                x+=1
			    elif text.find("ebola",0,len(text)) != -1 :
                                x+=1
	

mypath1 = "/home/vgc/shorya_gupta/memexcrawler/analysis/BingSearch/ValidationPges/"
for dirpath, dirnames, filenames in walk(mypath1):
    f2.extend(filenames)

list1 = []
list2 = []
str = ""
for f in f1:
   str = f
   str = str.replace("%3A",":")
   str = str.replace("%2F","/")
   list1.append(str)

for f in f2:
   str = f
   str = str.replace("%20","/")
   list2.append(str)

print list1[0]
print list2[0]

print set(list1).intersection(list2)
