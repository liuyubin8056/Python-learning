a={}
x=''
while(True):
    x=input("输入键，退出输入quit：")
    if(x=='quit'):                 #判断输入
        break
    else:
        a[x]=input("输入值：")
        print(a)                   #每轮输入后打印字典
print(a)

def bmi(height,weight):     #判断
    b=weight/height**2
    if(b>=18.5 and b<24):
        print("不错不错")
    elif(b<18.5):
        print("电线杆子")
    else:
        print("少喝糖水")
height=float(input("输入身高（米）："))
weight=float(input("输入体重（千克）："))
bmi(height,weight)