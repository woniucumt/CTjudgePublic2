
import random
n1=random.randint(1,100)
n2=random.randint(1,100)
sum=0
if n1>n2:
    temp=n1
    n1=n2
    n2=temp
a=n1
while a<=n2:
    if a%2==0:
        sum+=a
    a+=1
print(sum)
#qt

