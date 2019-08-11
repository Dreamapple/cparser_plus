# CppStatic
轻量级的C++语言重构器。基于clang的Python绑定cindex。目标是提供一套简单一致的API对C++语言重构的支持。

## 使用方式Tutorial
```Python
import cpp_refactor
from cpp_refactor import parse_files, Class, Function, Method

# global_namespace 现在保存着各个文件的全局命名空间的信息。
global_namespace = parse_files("main.cpp", "test.cpp", "test.h")

# 可以通过classes()方法获取所有的类的声明
print(global_namespace.classes())  # 打印各个类的简单描述。名字或者repr类，记录文件名，但是内容和文件无关。

# 通过__getitem__可以获取具体的类
cls_a = global_namespace["ClassA"]

# append replace delete
cls_a.append(ClassMethod("""
    int test(const ClassB& b){
        return b.b;
    }
""", public=True, inline=False))  # 自动检查是否有对应的实现文件，分开为头文件和实现文件。

或者直接
cls_a.append("""
    int test(const ClassB& b){
        return b.b;
    }
""", public=True, inline=False)  # 自动检查是否有对应的实现文件，分开为头文件和实现文件。

global_namespace.diff()  # 打印diff信息。
global_namespace.commit() # 应用diff，将内容协会原始文件。
```

## 参考文档Referance
该模块依赖clang模块，clang
核心模块是cpp_refactor，
