data=[]
a=10
for i in range(10):
    data.append(a)
    a+=10
print(data)
temp=data[-1]
a=len(data)-1
for i in range(a-1):
    data[a]=data[a]
    a-=1
data[a]=temp
print(data)
#bl