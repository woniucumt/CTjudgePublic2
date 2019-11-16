sum=0
a=1
sw=0
while a<=100:
    if sw==0:
        sum+=a
        sw=1
    else:
        sum-=a
        sw=0
    a+=1
print(sum)
#qt


