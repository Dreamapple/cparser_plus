# CppStatic
轻量级的C++语言解析器。基于正则表达式和栈分析。目标是提供对C++语言重构的支持。

## 使用方式
```python
from cppstatic import parse_files, ClassMethod
cpp = parse_files("main.cpp", "test.cpp", "test.h")
# cpp 现在保存着各个文件的信息，并对文件的交叉引用进行简单的分析。
print(cpp.classes())  # 打印各个类的名字或者repr类，记录文件名，但是内容和文件无关。
cpp["ClassA"].append(ClassMethod("""
    int test(const ClassB& b){
        return b.b;
    }
""", public=True, inline=False))  # 自动检查是否有对应的实现文件，分开为头文件和实现文件。
cpp.diff()  # 打印diff信息。
cpp.commit() # 应用diff，将内容协会原始文件。
```
