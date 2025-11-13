#这是刘毓彬的作业
message = "hello word"
print(message)
a=1
print(a)
b=1.1
c=4.5
print(b+c)
list1 = [1,2,3,4,5]
print(list1)
#下面我打个分隔方便看
print("-------------------------------------")
#以下是汉诺塔，将5个盘子从x移动到z，借助y
counter = 0
x=[5,4,3,2,1]
y=[]
z=[]
def hanoi(n,x,y,z):
    global counter
    if n==1:
        z.append(x.pop())
        print("x --> z")
        print(f"x={x},y={y},z={z}")
        counter+=1
    else:
        #将n-1的盘子从x移动到y
        hanoi(n-1,x,z,y)
        #将最底下的盘子从x移动到z
        z.append(x.pop())
        print("x --> z")
        print(f"x={x},y={y},z={z}")
        #再将n-1个盘子从y移动到z
        hanoi(n-1,y,x,z)
        counter+=1
num = 5
hanoi(num,x,y,z)
print("总共移动了",counter,"次")