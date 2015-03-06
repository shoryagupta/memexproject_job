import os
import re
import random
from operator import itemgetter
from os import walk
from BeautifulSoup import BeautifulSoup,Comment

def extract(page):
    k=0
    soup = BeautifulSoup(page)
    soup = soup.find('html')
    if soup != None:
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))     #removing comments from page
        [comment.extract() for comment in comments]
        for elem in soup.findAll(['script','style']):
           elem.extract()
        text = soup.getText()
        k=findkeyword(text)
    return k

def findkeyword(data):
    pattern1 = re.compile('(.*)ebola(.*)',re.IGNORECASE)
    #key_list = ["traffick","sell","trade","illegal","market","transplant"]
    '''pattern2 = []
    for k in key_list:
    	pattern = re.compile('(.*)'+k+'(.*)',re.IGNORECASE)
    	pattern2.append(pattern)'''

    s1 = re.search(pattern1,data)
    '''s = None
    for p in pattern2:
    	s = re.search(p,data)
        if s:
            break'''
    if ((s1 != None)):
    	return 0
    else:
    	return 1
 
def getfilelist(target):
    mypath = ""
    files = []
    directories = []
    list_files = []
    list = []
    for [path, dirnames, filenames] in walk(target):
        directories.extend(dirnames)
	#print len(directories)
        for dname in dirnames:
            mypath = target+dname
            for [p,d,f] in walk(mypath):
		files.extend(f)
		#print len(files)
		list_files.append(files)
		#print len(list_files)
            files = []
    #print len(list_files)
    list.append(directories)
    list.append(list_files)
    return(list)

temp = 0
files = []
dir = []

target = "/home/vgc/shorya_gupta/ache/data/data_target/"
text_path = "/home/vgc/shorya_gupta/ache/data/Validation_results.txt"
filelist = getfilelist(target)
filelist1 = []
dir = filelist[0]
files = filelist[1]

for i in range(0,(len(files))):
    a = [dir[i],files[i],len(files[i])]
    filelist1.append(a)

del(files)
del(dir)

filelist1 = sorted(filelist1,key = itemgetter(2),reverse=0)
wt_list = []
text = open(text_path,'ab+')
i=0

if(os.stat(text_path)[6]!=0):
    with open(text_path) as x:
	for line in x:
	    i += 1
	    l = line.split()
	    wt = [l[1],l[2]]
	    wt_list.append(wt)

print i
print len(filelist1)
filelist1 = filelist1[i:]
#filelist1 = reversed(filelist1)
print len(filelist1)

if filelist1:
    for f in (filelist1):
	text = open((text_path),'ab+')
        rcount = 0
        icount = 0
	print "Directory: "+f[0]+" Files: "+str(f[2])
	if(f[2]<=200):
    	    for k in f[1]:
                try:
	    	    t = target+f[0]+'/'+k
	    	    htmlFile = open(t,'r')
            	    html = htmlFile.read()
	    	    temp = findkeyword(html)
            	    htmlFile.close()
	    	    if(temp == 1):
		        #irel_temp.append(k)
	                icount+=1
		        print "File: "+k+" : Irrelevant ("+str(icount)+','+str(rcount)+')'
	            else:
	                #rel_temp.append(k)
		        rcount+=1
		        print "File: "+k+" : Relevant ("+str(rcount)+','+str(icount)+')'
		    del(temp)
                except IOError as e:
                    print e
		
	    text.write(f[0]+" "+str(f[2])+" "+str((rcount*100)/f[2])+" %\n")
	    print(str((rcount*100)/f[2])+"% relevant")
	    wt = [f[2],((rcount*100)/f[2])]
	    wt_list.append(wt)
	
	else:
	    #print "in else"
	    f1 = random.sample(f[1],200)
	    print len(f1)
	    for k in f1:
                try:
                    t = target+f[0]+'/'+k
                    htmlFile = open(t,'r')
                    html = htmlFile.read()
                    temp = findkeyword(html)
                    htmlFile.close()
                    if(temp == 1):
                        icount+=1
                        print "File: "+k+" : Irrelevant ("+str(icount)+','+str(rcount)+')'
                    else:
                        rcount+=1
                        print "File: "+k+" : Relevant ("+str(rcount)+','+str(icount)+')'
                    del(temp)
                except IOError as e:
                    print e
	    text.write(f[0]+" "+str(f[2])+" "+str((rcount*100)/200)+" %\n")
            print(str((rcount*100)/200)+"% relevant")
            wt = [f[2],((rcount*100)/200)]
            wt_list.append(wt)
    	text.close()

rel_per = 0
total = 0
for w in wt_list:
    rel_per = rel_per + (int(w[0])*int(w[1]))
    total = total + int(w[0])

rel_per = rel_per/total
print str(rel_per)

del(filelist1)
