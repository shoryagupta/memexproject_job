import os
import re
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
    pattern1 = re.compile('(.*)organ(.*)',re.IGNORECASE)
    key_list = ["traffick","sell","trade","illegal","market","transplant"]
    pattern2 = []
    for k in key_list:
    	pattern = re.compile('(.*)'+k+'(.*)',re.IGNORECASE)
    	pattern2.append(pattern)

    s1 = re.search(pattern1,data)
    s = None
    for p in pattern2:
    	s = re.search(p,data)
        if s:
            break
    if ((s != None) and (s1 != None)):
    	return 0
    else:
    	return 1
 

    #subtext = ["Organ Trafficking","organ trafficking","Organ Selling","organ selling","Organ Trade","organ trade","ORGAN TRADE","ORGAN SELLING","ORGAN TRAFFICKING","organ black market","Organ Black Market"]
     #if all(x not in data for x in subtext):
 	#return 1
     #else:
         #return 0
    
#def findkey(data):
#    if((re.match("(*.organ.*)", data)) && (re.match("(*.traffick.*)", data)) && (re.match("(*.trade.*)", data)) && (re.match("(*.transplant.*)", data)) && (re.match("(*.illegal.*)", data)) && (re.match("(*.ORGAN.*)", data)) && (re.match("(*.TRAFFICK.*)", data)) && (re.match("(*.TRADE.*)", data)) && (re.match("(*.TRANSPLANT.*)", data)) && (re.match("(*.ILLEGAL.*)", data)) ):
#        return 1
#    else:
#	return 0

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

itotal = 0
rtotal = 0
temp = 0
files = []
dir = []

target = "/home/vgc/shorya_gupta/data_ebola/data/data_target/"
text_path = "/home/vgc/shorya_gupta/data_ebola/data/textfiles/"
filelist = getfilelist(target)
filelist1 = []
dir = filelist[0]
files = filelist[1]
x=0

for i in range(0,(len(files))):
    a = [dir[i],files[i],len(files[i])]
    filelist1.append(a)
    x+=len(files[i])

print x
filelist1 = sorted(filelist1,key = itemgetter(2),reverse = 0)
#print filelist1[199][1]

for f in filelist1:
    text = open((text_path+f[0]+".txt"),'ab+')
    if(os.stat(text_path+f[0]+".txt")[6]==0):
	#text = open((text_path+dir[i]+".txt"))
        rcount = 0
        icount = 0
	rel_temp = []
	irel_temp = []
	print "Directory: "+f[0]+" Files: "+str(f[2])
    	for k in f[1]:
            try:
	    	t = target+f[0]+'/'+k
	    	htmlFile = open(t,'r')
            	html = htmlFile.read()
	    	temp = findkeyword(html)
            	htmlFile.close()
	    	if(temp == 1):
		    irel_temp.append(k)
	            icount+=1
		    print "File: "+k+" : Irrelevant ("+str(icount)+','+str(rcount)+')'
	        else:
	            rel_temp.append(k)
		    rcount+=1
		    print "File: "+k+" : Relevant ("+str(rcount)+','+str(icount)+')'
		del(temp)
            except IOError as e:
                print e
        itotal+=icount
	rtotal+=rcount
	text.write("Relevant = "+str(rcount)+"\tIrrelevant = "+str(icount)+'\n')
	text.write("Relevant Files :\n")
	text.writelines(["%s\n" % a  for a in rel_temp])
	text.write("Irrelevant Files :\n")
	text.writelines(["%s\n" % a  for a in irel_temp])
        print "Relevant = "+str(rcount)+"\tIrrelevant = "+str(icount)
    else:
	print f[0]+".txt not empty"
	position = text.seek(0,0)
	line = text.readline()
	cnt = re.findall('\d+',line)
	rtotal+=int(cnt[0])
	itotal+=int(cnt[1])
	del(cnt)
    text.close()
    print "Total Relevant: "+str(rtotal)
    print "Total Irrelevant: "+str(itotal)

del(filelist1)
del(rtotal)
del(itotal)
del(files)
del(dir)

