
def sexpr_load( fp ):    
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

global_ns = {
    'bool': ('bool', 'type'),
    'true': ('true', 'bool'),
    'false': ('false', 'bool'), 
    'and bool': ('andalso',['->', 'bool','bool','bool']),

    'int': ('int','type'),
    '+ int': ('(fn a => fn b => Int.+ (a,b))',['->', 'int','int','int']),
    '- int': ('(fn a => fn b => Int.- (a,b))',['->', 'int','int','int']),
    '* int': ('(fn a => fn b => Int.* (a,b))',['->', 'int','int','int']),
    '/ int': ('(fn a => fn b => Int.div (a,b))',['->', 'int','int','int']),
    '% int': ('(fn a => fn b => Int.mod (a,b))',['->', 'int','int','int']),
    '< int': ('(fn a => fn b => Int.< (a,b))',['->', 'int','int','bool']),
    '<= int': ('(fn a => fn b => Int.<= (a,b))',['->', 'int','int','bool']),
    '> int': ('(fn a => fn b => Int.> (a,b))',['->', 'int','int','bool']),
    '>= int': ('(fn a => fn b => Int.>= (a,b))',['->', 'int','int','bool']),
    '== int': ('(fn a => fn b => a=b)',['->', 'int','int','bool']),
    '!= int': ('(fn a => fn b => not (a=b))',['->', 'int','int','bool']), 
    'print int': ('(General.o (TextIO.print,Int.toString))',['->','int','unit']),
}

import os
import re
import subprocess
import sys

def uuid( n=[0] ):
    n[0] += 1
    return "us_"+str(n[0])

def type_accepts( l, r ): return l==r
def type_print( t ):
    if isinstance(t,str):
        assert t in global_ns and global_ns[t][1]=='type'
        return global_ns[t][0]
    elif t[0]=="->": return "("+"->".join(map(type_print,t))+")"
    elif t[0]=="*": return "("+"*".join(map(type_print,t))+")"
    else: assert False
def type_apply( l, r ):
    assert isinstance(l,list) and len(l)>=3 and l[0]=="->" and l[1]==r, str(l) + " " + str(r)
    if len(l)==3: return l[2]
    else: return ["->"] + l[2:]

def codeof( sx, ns=global_ns ):
    if isinstance(sx, str): 
        if re.match("\d+",sx): return (sx,"int")
        else: return ns[sx]
    elif sx[0]=="fun":
        name = sx[1]
        lhs, ret, rhs = [],[],[]
        for part in sx[2:]:
            if len(ret)>0: rhs.append( part )
            elif part[0]=="returns": ret.append( part )
            else: lhs.append( part )  
        types = map(lambda (l,r): r, lhs)
        ns[name+" "+type_print()] = ( uuid(), ['->']+types+[ret[1]] )
        nns = {}; nns.update(ns)
        map( lambda t,T: nns.define( t, (uuid(),T) ), lhs )
        code = ""
        for t,T in [codeof(x,nns) for x in rhs]:
            if code!="": code += ";"
            code += t
        assert type_accepts( ret[1], T ), "return type from function does not match declared type" 
        parms = " ".join(map( lambda(l,r):"(%s: %s)"%(nns[l],type_print(r)), args))
        return ("fun %s %s: %s = %s" % (name,parms,type_print(ret[1]),code), None)
    elif sx[0]==",":
        results = [ codeof(t,ns) for t in sx[1:] ]
        code = '('+ ','.join(map(lambda(l,r):l,results)) +')'
        type = '('+ '*'.join(map(lambda(l,r):r,results)) +')'
        return (code,type)
    elif re.match('#\d+',sx[0]): raise NotImplementedError()
    else:
        hd = sx[0]; tl = tuple(codeof(x,ns) for x in sx[1:])
        if isinstance(hd,str): hd = ns[hd+" "+type_print(tl[0][1])]
        else: hd = codeof(hd)
        for arg in tl:
            hd = ( "(%s %s)"%(hd[0],arg[0]), type_apply(hd[1],arg[1]) )
        return hd

if __name__=="__main__":
    if sys.argv[0]=="python": args = sys.argv[2:]
    else: args = sys.argv[1:]
    assert len(args)==1 and args[0].endswith('.c2')
    in_file = args[0]
    out_file = in_file[:-3] + ".sml"
    of = open(out_file,'w')
    for line in sexpr_load(in_file):
        of.write( codeof(line)[0] )
        of.write( ";\n\n" )
    of.close()
    subprocess.Popen(["mlton",out_file]).wait()
    os.remove(out_file)











