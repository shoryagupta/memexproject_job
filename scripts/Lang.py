from langdetect import detect
import os
from bs4 import BeautifulSoup,Comment
from shutil import move

x=0
y=0
z=0

filelist = os.listdir(os.getcwd())
for f in filelist:
    if f!="Lang.py":
        try:
            htmlFile = open(f,'r')
            text = htmlFile.read()
           """ soup = BeautifulSoup(html)
            soup = soup.find('html')
            if soup != None:
                comments = soup.findAll(text=lambda text:isinstance(text, Comment))     #removing comments from page
                [comment.extract() for comment in comments]
                for elem in soup.findAll(['script','style']):
                    elem.extract()
                    text = soup.getText()"""
	    htmlFile.close()
        except IOError as e:
	    print e 

	try:
	    if detect(text) ==  "en":
		x = x+1
		#move(f,"/home/vgc/shorya_gupta/Seeds/")
	    else:
		y = y+1
		move(f,"/home/vgc/shorya_gupta/lang_filter/")
	except:
		z = z+1
		move(f,"/home/vgc/shorya_gupta/lang_filter/")
	del(text)

print "English Pages: "+str(x)
print "Non-English Pages: "+str(y)
print "Page Not Found: "+str(z)

