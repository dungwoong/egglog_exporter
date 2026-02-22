from __future__ import annotations
from egglog import *
from egraph2node import Node, EgglogExporter


class TestExpr(Expr):
    @classmethod
    def TEST(cls, i: i64) -> TestExpr: ...

class Stmt(Expr):
    @classmethod
    def Add(cls, s1: Stmt, s2: Stmt) -> Stmt: ...

    @classmethod
    def IntLiteral(cls, i: i64) -> Stmt: ...

    @property
    def prop(self) -> i64: ...

    @property
    def prop2(self) -> TestExpr: ...

exporter = EgglogExporter()
exporter.register_egglog_classes(Stmt)

# define these nodes for each method in your IR
@exporter.register(Stmt.IntLiteral, props=("prop", "prop2"))
class IntLiteral(Node): ...

@exporter.register(Stmt.Add)
class Add(Node): ...

@exporter.register(TestExpr.TEST)
class Test(Node): ...

expr = Stmt.Add(Stmt.Add(Stmt.IntLiteral(1), Stmt.IntLiteral(2)), Stmt.IntLiteral(3))
graph = EGraph()

@graph.register
def _(t: Stmt, i: i64):
    yield rule(t == Stmt.IntLiteral(i)).then(
        set_(t.prop).to(i * 2)
    )
    yield rule(t == Stmt.IntLiteral(i)).then(
        set_(t.prop2).to(TestExpr.TEST(i * 3))
    )


result = graph.let("output", expr)
graph.run(10)
extracted = graph.extract(result)
root = exporter(graph, extracted)
print(extracted)
print(root.debug_str())