import csv
import random

csvfile= open('/Users/weihanchu/Desktop/hw4-2.csv', 'w')
writer=csv.writer(csvfile)
n=1
head=[]
while(n<9):
	head.append(n)
	n=n+1
writer.writerow(head)

m=1
while(m < 1001):
    column1 = 100*random.random()
    column2 = 100*random.random()
    column3 = column2+column1
    column4 = 2*column2+random.uniform(0,100)
    column5 = column3-0.5*random.uniform(0,100)
    column6 = 2*column4-column5
    column7 = column3+2*column5

    if(column7-column6 > 100):
    	column8='a1'
    elif(column7-column6 > 30):
    	column8='a2'
    elif(column7-column6 > -30):
    	column8='a3'
    elif(column7-column6 > -100):
    	column8='a4'
    else:
    	column8='a5'
    writer.writerow([column1,column2,column3,column4,column5,column6,column7,column8])
    m = m + 1

csvfile.close()


check= open('/Users/weihanchu/Desktop/hw4-2.csv')
reader = csv.reader(check)
for row in reader:
    print row