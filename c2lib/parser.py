
import re

def load( fp ):    
    stack = [ [] ]
    for t in re.findall("\(|\)|[^\s\(\)]+", file(fp).read() ):
        if t=="(": 
            stack.append( [] )
        elif t==")": 
            top = stack.pop()
            stack[-1].append( top )
        else:
            stack[-1].append( t )
    assert len(stack)==1
    return stack.pop()
