import json


class EClass:
    def __init__(self, name, t):
        self.name = name
        self.type = t
        self.nodes = []
        self.props = dict()
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def add_prop(self, prop, value):
        assert prop not in self.props, prop
        self.props[prop] = value
    
    def __repr__(self):
        children = ', '.join(n.type for n in self.nodes)
        return f'{self.name}({children})'

class ENode:
    def __init__(self):
        self.type = None
        self.id = None
        self.children_eclasses = []
        self.props = dict()
    
    def add_child(self, c):
        self.children_eclasses.append(c)
    
    def add_prop(self, prop, value):
        assert prop not in self.props, prop
        self.props[prop] = value


class FromJson:
    """
    The desired format would be nodes of specific types,
    and then data is attached as properties of the nodes
    """
    def __init__(self):
        self.eclasses = dict()
        self.enodes = dict()

    def from_json(self, data):
        for k, v in data["class_data"].items():
            # Don't retain class type for now
            self.eclasses[k] = EClass(k, v["type"])
        self.populate_enodes(data)
    
    def populate_enodes(self, data):
        for k, v in data["nodes"].items():
            node = self.construct_enode(k, v)
            self.enodes[k] = node
            eclass = self.eclasses[v["eclass"]]
            eclass.add_node(node)
        for k, v in data["nodes"].items():
            self.add_children(k, v)

    def construct_enode(self, k, v):
        node = ENode()
        node.type = v["op"]
        node.id = k
        return node
    
    def add_children(self, k, v):
        for c in v["children"]:
            self.enodes[k].add_child(self.enodes[c])
        if v["op"].startswith("·."): # property/Eclass analysis
                prop = v["op"][2:]
                eclass = self.eclasses[v["eclass"]]
                for c in v["children"]:
                    self.enodes[c].add_prop(prop, eclass)


fj = FromJson()


with open("data/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fj.from_json(data)
for _, eclass in fj.eclasses.items():
    print(repr(eclass))