import math
name=[]
age=[]
name.append("anran")
age.append(17)
name.append("zhangyi")
age.append(16)
name.append("fangjking")
age.append(19)
name.append("yangyue")
age.append(14)
name.append("qioushui")
age.append(16)
key=input("name")
low=0
high=len(name)-1
while low<=high:
    mid=math.floor((low+high)/2)
    if key==name[mid]:
        print(name,age[mid])
        break
    else:
        if key<name[mid]:
            high=mid-1
        else:
            low=mid+1
print(key,"meiyou")
#qt