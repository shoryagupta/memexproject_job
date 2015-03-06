wt_lst = []
x=0
reslt = "/home/vgc/shorya_gupta/data_ot/data/Validation_results.txt"
with open(reslt) as x:
    for line in x:
	l = line.split()
	if(len(l) == 0):
	    x=1
	    break
	else:
	    wt = [l[1],l[2]]
	    wt_lst.append(wt)

a=0
b=0
for w in wt_lst:
    a = a+(int(w[0])*int(w[1]))
    b = b+int(w[0])

text = open(reslt,'ab+')
text.write("\nTotal no. of Pages = "+str(b))
text.write("\nPercentage of Relevant Pages = "+str(a/b)+"%")
text.close()
a = a/b
print a
print b

