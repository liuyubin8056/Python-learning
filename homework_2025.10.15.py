list1 = [1, 2, 3, 4, 5]
for i in list1:#遍历列表
    print(i)
print(list1[:3])#列表切片
for i in list1[:3]:#遍历切片
    print(i)

dict1 = {'name': 'Alice', 'age': 30, 'city': 'New York'}
print(dict1['name'])#访问字典中的元素
for key in dict1:#遍历字典
    print(key, dict1[key])

#列表和字典相互嵌套并访问
dict2={
    "roommate":["张三","李四","王五"],
    "score":[90, 85, 88]
}
print(dict2["roommate"][0])#访问列表中的第一个元素
list2=[
    {"name":"张三","age":20},
    {"name":"李四","age":21},
    {"name":"王五","age":22}
]
print(list2[0]["name"])#访问字典中的name键对应的值

#关于if阿巴阿巴的一大堆
n=input("请输入一个正整数\n")
if n.isdigit():
    if int(n)%2==0:
        a=list2[0]["age"]
        if a>=21:
            print("玛卡巴卡")
        elif a>=20 or a<5:
            print("唔系迪系")
        else:
            print("晚安玛卡巴卡")
if "渣渣" not in dict2["roommate"]:
    dict2["roommate"].append("渣渣")
print(dict2["roommate"])
lap_hang=["Lenovo","Mac","Dell","Asus"]
lap_la=["Colorful","Huawei","jige"]
my_lap=input("请输入你的电脑品牌\n").lower()
if my_lap in [i.lower() for i in lap_hang]:
    print("你也有一台",my_lap,"电脑")
elif my_lap in [i.lower() for i in lap_la]:
    print("你咋想的")
else:
    print("买了个啥这是")