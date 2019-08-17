"""

"""
from clang.cindex import Index, CursorKind, TypeKind, Type, Cursor, AccessSpecifier

class SourceManager(dict):
    pass


_source_manager = SourceManager()


class Code:
    def __init__(self, src=None, path=None):
        self.src=src
        self.path=path
        self._changes = []

    def get_changed(self):
        path = self.path
        src = self.src
        for cmd, pos, code in self._changes:
            if cmd == 'insert':
                src = src[:pos['offset']] + code + src[pos['offset']:]
            elif cmd == 'delete':
                pass
            elif cmd == 'replace':
                pass
        return src

class Node:
    """
    对clang的cursor简单封装
    """
    def __init__(self, obj, code=None):
        self.obj=obj
        self.code = code

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __iter__(self):
        for ch in self.obj.get_children():
            yield Node(ch, code=self.code)

    def __getitem__(self, name):
        if isinstance(name, int):
            return Node(list(self.get_children())[name])

    def __repr__(self):
        if self.type and self.type.kind != TypeKind.INVALID:
            type_ = f", {self.type.kind}, {self.type.spelling}"
        else:
            type_ = ''
        return f"Cursor({self.kind[11:]}, {self.spelling}{type_})"

    def __str__(self):
        return self.spelling
       

# class Code:
#     pass


class Scope:
    def __init__(self, name=None, nodes=None):
        self._nodes = [] if nodes is None else nodes
        self.name = name

    @staticmethod
    def _get_insert_pos(node):
        # path = node.obj.location.file.name
        # f = open(path, 'r', encoding='utf-8').read()
        # _source_manager[path] = f
        node.extent.end.line
        node.extent.end.offset

    def add_node(self, node):
        self._nodes.append(node)

    def classes(self):
        ret = []
        for node in self._nodes:
            for ch in node:
                if ch.kind in {CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE}:
                    ret.append(ch)

        return Scope(name='classes', nodes=ret)

    def _iter_children(self):
        for node in self._nodes:
            yield from node

    def __getitem__(self, name):
        """
        一个名字可能对应多个节点，类型相同的，合并处理
        """
        return Scope(name=name, nodes=[k for k in self._iter_children() if k.spelling==name])

    def append(self, code, **kwargs):
        if len(self._nodes) == 0:
            raise Exception("empty scope!")
        if len(self._nodes) == 1:
            node = self._nodes[0]
            loc = node.extent.end
            pos = {'name': loc.file.name, 'line': loc.line-1, 'column': loc.column-2, 'offset': loc.offset-1}
            node.code._changes.append(['insert', pos, code])
        elif len(self._nodes) == 2:
            node = self._get_head_node()
            # pos = self._get_insert_pos(node)
            loc = node.extent.end
            pos = {'name': loc.file.name, 'line': loc.line-1, 'column': loc.column-2, 'offset': loc.offset-1}
            
            decl_code = self._make_decl(code)
            node.code._changes.append(['insert', pos, decl_code])
            node = self._get_impl_node()
            # pos = self._get_insert_pos(node)
            loc = node.extent.end
            pos = {'name': loc.file.name, 'line': loc.line-1, 'column': loc.column-2, 'offset': loc.offset-1}
            
            node.code._changes.append(['insert', pos, code])


    def insert(self, code, before=None, after=None):
        pass

    def delete(self):
        pass

    def replace(self, code):
        pass

    def get_source(self):
        pass

    def get_changed(self):
        if len(self._nodes) == 1:
            return self._nodes[0].code.get_changed()
        changed = {}
        for node in self._nodes:
            path = node.path
            src = node.code.get_changed()
            changed[path] = src
        return changed

    def diff(self):
        pass

    def commit(self):
        pass

    def __repr__(self):
        return f"Scope<{self.name}: {self._nodes}>"

    __str__ = __repr__


class Parser:
    """
    基础解析器，对clang的Index的简单封装
    """
    def __init__(self):
        self._index = Index.create()
        self._scope = Scope(name="global namespace")

    def parse_file(self, path, **kwargs):
        unit = self._index.parse(path, None)
        self._scope.add_node(Node(unit.cursor, code=Code(src=s, path=path)))

    def parse_string(self, s, path="<memory_file>.cpp"):
        unit = self._index.parse(path, None, unsaved_files=[(path, s)])
        self._scope.add_node(Node(unit.cursor, code=Code(src=s, path=path)))

    def get_space(self):
        return self._scope
        

def parse_files(*files, **kwargs):
    parser = Parser()
    for file in files:
        parser.parse_file(file, **kwargs)

    return parser.get_space()

def parse(s):
    parser = Parser()
    parser.parse_string(s)

    return parser.get_space()




test_h = """

// This type wraps a variable whose constructor and destructor are explicitly
// called. It is particularly useful for a global variable, without its
// constructor and destructor run on start and end of the program lifetime.
// This circumvents the initial construction order fiasco, while keeping
// the address of the empty string a compile time constant.
//
// Pay special attention to the initialization state of the object.
// 1. The object is "uninitialized" to begin with.
// 2. Call Construct() or DefaultConstruct() only if the object is
//    uninitialized. After the call, the object becomes "initialized".
// 3. Call get() and get_mutable() only if the object is initialized.
// 4. Call Destruct() only if the object is initialized.
//    After the call, the object becomes uninitialized.
template <typename T>
class ExplicitlyConstructed {
 public:
  void DefaultConstruct() { new (&union_) T(); }

  template <typename... Args>
  void Construct(Args&&... args) {
    new (&union_) T(std::forward<Args>(args)...);
  }

  void Destruct() { get_mutable()->~T(); }

  constexpr const T& get() const { return reinterpret_cast<const T&>(union_); }
  T* get_mutable() { return reinterpret_cast<T*>(&union_); }

 private:
  // Prefer c++14 aligned_storage, but for compatibility this will do.
  union AlignedUnion {
    char space[sizeof(T)];
    int64 align_to_int64;
    void* align_to_ptr;
  } union_;
};

"""




if __name__ == '__main__':
    # main()
    p = Parser()
    p.parse_string(test_h)
    
