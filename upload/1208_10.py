sum=0
xiangshu=int(input("xaingshu"))
a=1
b=1
sum+=a
sum+=b
for i in range(xiangshu-2):
    c=a+b
    sum+=c
    a=b
    b=c
print(c)
