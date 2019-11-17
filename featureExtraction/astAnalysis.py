import ast,astunparse

identifier = []
identifierInLeft = []

assignNum = []
compareNum = []
funcArgs = []           #文件内各函数参数名列表
funcArgsNum = []        #文件内各函数参数个数列表
funcArgsLen = []
# func
expressionNum = []
listDepth = []
# func_def =

class CodeTransformer(ast.NodeVisitor):
    def walkList(self, node, depth = 1):
        maxDepth = depth
        for i in node.elts:
            if(isinstance(i,ast.List)):
                temp = self.walkList(i, depth + 1)
                if temp > maxDepth:
                    maxDepth = temp
                print("hhhhhhhhhhhhhhhhh")
        return maxDepth

    def generic_visit(self, node):
        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            #print(node.id)
        if hasattr(node, 'test'):
            expressionNum.append('1')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Attribute(self, node):
        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            # print(node.id)
        if node.attr not in identifier:
            identifier.append(node.attr)
        # print(node.attr)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self,node):
        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            # print(node.id)
        assignNum.append('1')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Compare(self,node):
        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            # print(node.id)
        compareNum.append('1')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            # print(node.id)
        # print(node.lineno)
        # print(node._fields)
        # print(node.col_offset)
        ast.NodeVisitor.generic_visit(self, node)
        # print(node.lineno)

    def visit_FunctionDef(self,node):
        # print(node.args.args)
        temp = 0
        for i in node.args.args:
            funcArgs.append(len(i.arg))
            temp += len(i.arg)
        funcArgsLen.append(temp)

        if hasattr(node, 'id'):
            if node.id not in identifier:
                identifier.append(node.id)
            # print(node.id)
        funcArgsNum.append(len(node.args.args))
        ast.NodeVisitor.generic_visit(self, node)

    # def visit_List(self,node,maxListDepth = 0):
    #     print("*******************")
    #     print(node.__class__.__name__)
    #     maxListDepth += 1
    #     if len(node.elts)!=0:
    #         for i in node.elts:
    #             if i.__class__.__name__ == 'List' :
    #                 self.visit_List(node,maxListDepth)
    #                 print("*******************")
    #                 print(maxListDepth)
    def visit_List(self, node):
        # print("---------------------")
        # print(astunparse.dump(node))
        listDepth.append(self.walkList(node))
        # print(self.walkList(node))
        ast.NodeVisitor.generic_visit(self, node)



    # def visit_BinOp(self, node):
    #     if isinstance(node.op, ast.Add):
    #         node.op = ast.Sub()
    #     self.generic_visit(node)
    #     return node
    #
    # def visit_FunctionDef(self, node):
    #     self.generic_visit(node)
    #     if node.name == 'add':
    #         node.name = 'sub'
    #     args_num = len(node.args.args)
    #     args = tuple([arg.id for arg in node.args.args])
    #     func_log_stmt = ''.join(["print 'calling func: %s', " % node.name, "'args:'", ", %s" * args_num % args])
    #     node.body.insert(0, ast.parse(func_log_stmt))
    #     return node
    #
    # def visit_Name(self, node):
    #     replace = {'add': 'sub', 'x': 'a', 'y': 'b'}
    #     re_id = replace.get(node.id, None)
    #     node.id = re_id or node.id
    #     self.generic_visit(node)
    #     return node

    # def visit_Name(self, node):
    #     print(node)
    #     ast.NodeVisitor.generic_visit(self, node)
        # return node

    # def visit_FunctionDef(self, node):
    #     self.generic_visit(node)
    #     if node.name == 'add':
    #         node.name = 'sub'
    #     args_num = len(node.args.args)
    #     args = tuple([arg.id for arg in node.args.args])
    #     func_log_stmt = ''.join(["print 'calling func: %s', " % node.name, "'args:'", ", %s" * args_num % args])
    #     node.body.insert(0, ast.parse(func_log_stmt))
    #     return node


def astAnalysis(content):
    # 初始化计数值
    identifier.clear()
    identifierInLeft.clear()
    assignNum.clear()
    compareNum.clear()
    funcArgs.clear()
    funcArgsNum.clear()
    funcArgsLen.clear()
    expressionNum.clear()
    listDepth.clear()

    r_node = ast.parse(content.read())      #这句话分析了很多内容。真正的解析就是在这句话里面
    print("AST树分析：")
    #print(astunparse.dump(r_node))
    print("*"*20)
    transformer = CodeTransformer()
    r_node = transformer.visit(r_node)
    print("listDepthlistDepthlistDepthlistDepth")
    print(listDepth)





