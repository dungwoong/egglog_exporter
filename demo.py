from __future__ import annotations
from egglog import *
from egraph2node import Node, EgglogExporter
from graphviz import Source
import json

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'


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
def _(t: Stmt, i: i64, s1: Stmt, s2: Stmt):
    yield rule(t == Stmt.IntLiteral(i)).then(
        set_(t.prop).to(i * 2)
    )
    yield rule(t == Stmt.IntLiteral(i)).then(
        set_(t.prop2).to(TestExpr.TEST(i * 3))
    )
    yield rule(t == Stmt.Add(s1, s2)).then(
        union(t).with_(Stmt.Add(s2, s1))
    )


result = graph.let("output", expr)
graph.run(10)
extracted = graph.extract(result)
# graph.
root = exporter(graph, extracted)
print(extracted)
print(root.debug_str())

g = graph._serialize()
js = g.to_json()
with open("data.json", "w", encoding="utf-8") as f:
    data = json.loads(js)
    json.dump(data, f, indent=4)

dot = g.to_dot()
Source(dot, format='svg').render("egraph", cleanup=True)