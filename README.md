Exports an e-graph into a nodes and children format

## Example (demo.py)
`Stmt.Add(Stmt.Add(Stmt.IntLiteral(1), Stmt.IntLiteral(2)), Stmt.IntLiteral(3))`
- These are symbolic nodes, difficult to work with in Python

exports to:
`Add(IntLiteral<prop=6, prop2=Test(9)>(3), Add(IntLiteral<prop=4, prop2=Test(6)>(2), IntLiteral<prop=2, prop2=Test(3)>(1)))`
These are python node objects with children and props(analysis data)
