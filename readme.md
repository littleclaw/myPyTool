## 知识点列表

- 常用变量类型
    * 数字型，如12，-24，3.1415
    * 字符型，如"abc", "刘小辰"，‘男’，”Доброе утро“
    * 布尔型，只有True和False
    * 列表, 如
    ``` python
    ["张三", "李四", "王五"]
    ```
    * 字典,如 
   ```
    {
    createBy":"zhuyaofeng",
    "createTime":"2022-03-06 19:10:34",
    "updateBy":"zhuyaofeng",
    "updateTime":"2022-03-06 19:10:56",
    "userId":8,
    "userName":"朱耀锋",
    "type":"1",
    "time":"2022-03-06",
    "summary":"今日总结1",
    "plan":"明日计划2", 
    }
   ```
   
- 变量赋值

    * 用一个等号表示赋值，把右边的计算结果赋给左边的变量
    ``` python
    asya = "Ася"
    anton = "Антон"
    sentence = asya + " люблю " + anton #字符型用+会把字符拼在一块
    needLoseWeight=True
    canLoseWeight=False
    result = needLoseWeight and canLoseWeight
    ```
    * 自增赋值，自减、自乘都一个道理
    ``` python
    age= 18
    age+= 1
    age-= 2
    age*= 3
    age/= 4
    ```
    * 批量赋值
    ```python
name,age="Asya", 18
    ```
- 分支语句
    ``` python
    age = 3
    if age >= 18:
        print('adult')
    elif age >= 6:
        print('teenager')
    else:
        print('kid')
    ```
- 循环语句
    * for x in list形式
    ``` python
    sum = 0
    for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    	sum = sum + x
    print(sum)
    
    # 和上面一样的，range(11)方法生成一个列表，不需要自己一个个写了
    sum = 0
	for x in range(11):
    	sum = sum + x
	print(sum)
    ```
    * while condition形式 
    ``` python
    # 100以内所有奇数求和
    sum = 0
	n = 99
	while n > 0:
    	sum = sum + n
    	n = n - 2   #这句和 n-=2 是一回事
	print(sum)
    ```
- 方法，或者叫函数
    * 调用函数，函数名(参数列表)
    ``` python
    print("情书正文：")  # 打印，无返回值
    max(12, 3922, 7111) # 取最大值方法, 返回结果为 7111
    str(3.14) # 把数值型转成字符型，结果为"3.14"
    exit()  # 退出程序，无返回值
    ["小辰"].append("尚怼怼") #列表的添加方法，无返回值
	chen = {"name": "小辰", "gender": "女"}
	chen.get("name")  
	#字典的取值方法，等价于chen["name"],返回键对应的值
	```
	* 定义函数，在Python中，定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:，然后，在缩进块中编写函数体，函数的返回值用return语句返回。
 ``` python
    #求绝对值的方法
     def my_abs(x):
    		if x >= 0:
        		return x
    		else:
        		return -x
 ```
 	* 方法递归调用，方法可以调用方法本身实现循环，例如求阶乘，汉诺塔问题(有兴趣自己研究，没兴趣可以不管)
 - 文件相关方法
   * 打开文件方法 ,open(文件路径，打开方式)
   * 路径可以是绝对路径或者相对路径
   * 打开方式可以是'r'(read),'w'(write)用来读写文本，或者'rb','wb'用来读写图片、音频、视频等其他复杂格式。
   * 用'w'方法写已经存在的文件会覆盖掉原来的内容，相当于删掉原文件重新建文件，如果不想这样想在后面追加内容可以用'a'(append)方式
   

```python
f = open('test.txt', 'r', encoding='utf-8')
#第三个参数现在有点印象就行，那天晚上出错就是文件编码不匹配了
print(f.read())
f.close() #这种方法文件用完后要close()，否则会一直平白占用电脑内存
# 等价于下面这样，一般最好用下面的方法打开，因为用下面的不用考虑关闭文件的事情
with open('test.tex', 'r') as f:
	print(f.read())
   
with open('C:\chenchen.py', 'w') as ch:
	ch.write("# 刘小辰问魔镜：\“魔镜魔镜告诉我，这个世上谁最美？\”")
```

 * 新建文件夹方法，用os.makedirs(文件路径)

 os是操作系统operating system简称，dirs是directories简称，方法效果是新建一个文件夹，如果文件夹已经存在会报错,可以再加一个参数exist_ok=True来忽略错误
 	
 	```
 	day_folder_name = str(27)+"日"
 	file_path = "2022年工作\\5月工作报告\\" + day_folder_name
 	os.makedirs(file_path, exist_ok=True)
 	# 上面代码会在当前目录新建一个2022年工作文件夹，文件夹里有一个5月工作报告文件夹，再里面是27日文件夹
 	```

 * 列出路径下所有文件和文件夹方法os.listdir(路径)，返回一个文件名字符串列表

 	``` python
 		for f_name in os.listdir("D:\\WeChat"):
 	    	print(f_name)
 	```
