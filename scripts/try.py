import re

pattern1 = re.compile('(.*)organ(.*)',re.IGNORECASE)
key_list = ["traffick","sell","trade","illegal","market","transplant"]
pattern2 = []
for k in key_list:
    pattern = re.compile('(.*)'+k+'(.*)',re.IGNORECASE)
    pattern2.append(pattern)

str = "kjbgksajhg ORganaskjhgkduhglksd jkhg jhgodtradergkjb traiCKING"
s1 = re.search(pattern1,str)
s = None
for p in pattern2:
    s = re.search(p,str)
    if s:
	break
print s
print s1
if ((s != None) and (s1 != None)):
    print "valid"
else:
    print "false"
