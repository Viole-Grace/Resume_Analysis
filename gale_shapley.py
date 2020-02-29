import time

def match():
	menpref=dict();womenpref=dict()
	n=int(input("Enter no. of candidates  : "))
	for i in range(n):
		print ("Enter candidate ",i+1," : ")
		man=input()
		womenlist= []
		for j in range(n):
			print ("Enter company choice ",j+1," for the candidate : ")
			x=input()
			womenlist.append(x)
		menpref.update({man:womenlist})
	for i in range(n):
		print ("Enter company ",i+1," : ")
		woman=input()
		menlist= []
		for j in range(n):
			print ("Enter candidate ",j+1," for the company")
			x=input()
			womenlist.append(x)
		womenpref.update({woman:menlist})
	freemen=list(menpref.keys()) ;print ("Free candidates : ",freemen)
	takenwomen=[]
	final={}
	while freemen!=[]:
	    for i in freemen:
	        listofw=menpref.get(i)
	        for j in listofw:
	            if j not in takenwomen:
	                final[j]=i
	                freemen.remove(i)
	                takenwomen.append(j)
	                break
	            else:
	                listofm=womenpref.get(j)
	                r=final.get(j)
	                p=listofm.index(i)
	                q=listofm.index(r)
	                if p<q:
	                    final[j]=i
	                    freemen.remove(i)
	                    freemen.append(r)
	                    takenwomen.append(j)
	                    break
	return final