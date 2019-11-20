import random
data=[]
for i in range(10):
    data.append(random.randint(1,100))
min=data[0]
a=1
while a<len(data):
    if data[a]<min:
        min=data[a]
    a+=1
print(data,min)
#qt
    