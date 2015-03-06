import os
from bs4 import BeautifulSoup,Comment
from shutil import move

x=[]
text = ""
filelist = os.listdir(os.getcwd())
for f in filelist:
    text = ""
    if f!="Final.py":
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
        	    
	        subtext = ["Organ Trafficking","organ trafficking","Organ Selling","organ selling","Organ Trade","organ trade","ORGAN TRADE","ORGAN SELLING","ORGAN TRAFFICKING","organ black market","Organ Black Markey"]
		if any(x in text for x in subtext):
		    x.append(f)
		    move(f,"/home/vgc/shorya_gupta/False_Neg/")

                htmlFile.close()
            
        except IOError as e:
            print e

print len(x)
