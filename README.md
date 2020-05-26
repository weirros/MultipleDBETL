# MultipleDBETL
AP BO,集团多帐套取数工具；

目前是用pd的写excel方法，有复制到多个DW的部分；本项目里并没有包括这个内容；

**任务；**

可以理解任务是若干个取数语句、输出对应表排序构成的作业集合；

Jobs = [
			[SQL1,目标表1],
			[SQL2,目标表2]
]
这里用到了List，每次运行按照不同的SQL排队取数，最后输出到Excel；


**代码发布：**

1,程序依赖包
pip install -r requirements.txt
或者自行安装sqlalchemy,pandas,pymssql等常用包；
命令使用方法pip install 包名；

2,程序运行；
Python EtGroupETL.py
