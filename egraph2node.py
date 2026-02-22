from __future__ import annotations
from egglog import *

class Node:
    def __init__(self):
        self.children = []
        self.props = dict()
    
    # children can be other nodes or literals
    def add_child(self, c):
        self.children.append(c)
    
    def add_prop(self, k, v):
        self.props[k] = v
    
    def __repr__(self):
        children = ', '.join(repr(c) for c in self.children)
        return f'{self.__class__.__name__}({children})'
    
    def debug_str(self):
        children = ', '.join(c.debug_str() if isinstance(c, Node) else str(c) for c in self.children)
        props = ", ".join(f"{k}={v}" for k, v in self.props.items())
        props = f"<{props}>" if props else ""
        return f'{self.__class__.__name__}{props}({children})'


class EgglogExporter:
    def __init__(self):
        self._conversions = dict()
        self._props = dict()
        self._egglog_classes = set()
        self._checked = False
    
    def register_egglog_classes(self, *classes):
        self._egglog_classes = self._egglog_classes.union(classes)
    
    def register(self, egglog_fn, props=None):
        def deco(cls):
            assert issubclass(cls, Node)
            self._conversions[egglog_fn] = cls
            if props is not None:
                self._props[egglog_fn] = props
            return cls
        return deco
    
    def add_props(self, graph: EGraph, expr, node: Node, fn):
        props = self._props.get(fn, [])
        for p in props:
            o = graph.extract(getattr(expr, p))
            val = self._extract(graph, o) # recursively extract
            node.add_prop(p, val)
    
    def _extract(self, graph, root_expr):
        root = None
        s = [(root_expr, None)]
        while s:
            # we might want to use a match here
            curr, parent = s.pop()
            fn = get_callable_fn(curr)

            # construct item
            if fn is None:
                curr_node = curr.value
            else:
                curr_node = self._conversions[fn]()
                self.add_props(graph, curr, curr_node, fn)
            
            # set root if needed
            if parent is None:
                assert root is None
                root = curr_node
            else:
                parent.add_child(curr_node)
            args = get_callable_args(curr)
            if args is not None:
                s.extend((a, curr_node) for a in args)
        return root
    
    def __call__(self, graph, root_expr):
        return self._extract(graph, root_expr)
