from pathlib import Path
import json
path_j=Path('names_and_counts.json')

try:
    path=Path(r'F:\Code\Python\homework\homework_2025.10.30\红楼梦.txt')
except:
    pass
else:
    contents=path.read_text(encoding='utf-8').rstrip()
    lines=contents.splitlines()



sum1=0              #总行数
for line in lines:
    sum1+=1
print(f"共有{sum1}行")

def search(name):          #定义查找函数
    sum2=0              #含有指定名字的行数
    for line in lines:
        if(name in line):
            sum2+=1
    return sum2

n={}
x=''
while(True):
    x=input("输入你想查找的人名（退出输入quit）：")
    if(x=='quit'):
        break
    else:
        n[x]=search(x)     #写入字典


contents=json.dumps(n)
path_j.write_text(contents)    #写入json文件

print(n)