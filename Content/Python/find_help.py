import unreal

#本段直接复制到控制台逐行使用主要用于查找文档没标记的API

#查找StaticMesh的所有方法和属性 会找到文档中没有记录的方法
print(dir(unreal.StaticMesh))

#方便可读性
for item in dir(unreal.StaticMesh):
    print(item)

#解释其中的get_world方法
print(help(unreal.StaticMesh.get_world))