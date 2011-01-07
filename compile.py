
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

    'string': ('string','type'),
    'print string': ('print',['->','string','unit']),

    'list': ('list','type'),
    'nil': ('list',["list","'a"]),
    ":: (list 'a)": ('(fn a => fn b => (a :: b))',["->","'a",["list","'a"],["list","'a"]]),
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
        if t.startswith("'a"): return t
        assert t in global_ns and global_ns[t][1]=='type', t
        return global_ns[t][0]
    elif t[0]=="->": return "("+"->".join(map(type_print,t))+")"
    elif t[0]=="*": return "("+"*".join(map(type_print,t))+")"
    else: return "("+" ".join(map(type_print,t))+")"
def type_apply( l, r ):
    assert isinstance(l,list) and len(l)>=3 and l[0]=="->" and type_unify(l[1],r)!=None, str(l) + " " + str(r)
    if len(l)==3: return type_sub( l[2], type_unify(l[1],r) )
    else: return type_sub( ["->"] + l[2:], type_unify(l[1],r))
def type_sub( t, b ):
    if isinstance(t,list): return [type_sub(x,b) for x in t]
    if t in b: return b[t]
    else: return t
def type_unify( l, r ):
    if l==r: return {}
    if isinstance(l,str) and l.startswith("'"):
        assert not (isinstance(r,str) and r.startswith("'"))
        return {l: r}
    if isinstance(r,str) and r.startswith("'"):
        assert not (isinstance(l,str) and l.startswith("'"))
        return {r: l}
    if isinstance(l,list) and isinstance(r,list) and len(l)==len(r):
        if l[0]!=r[0]: return None
        d = {}
        for l,r in zip(l[1:],r[1:]):
            c = type_unify(l,r)
            if c==None: return None
            d.update( c )
        return d
def type_weaken( t ):
    yield t
    if isinstance(t,list) and len(t)==2:
        yield [t[0],"'a"]

def codeof( sx, ns=global_ns ):
    if isinstance(sx, str): 
        if re.match("\d+",sx): return (sx,"int")
        else: return ns[sx]
    elif sx[0]=="fun":
        name = sx[1]
        lhs, ret, rhs = [],[],[]
        for part in sx[2:]:
            if len(ret)>0: rhs.append( part )
            elif part[0]=="returns": ret = part
            else: lhs.append( part )  
        types = map(lambda (l,r): r, lhs)
        ns[name+" "+type_print(lhs[0][1])] = ( uuid(), ['->']+types+[ret[1]] )
        nns = {}; nns.update(ns)
        map( lambda(t,T): nns.__setitem__( t, (uuid(),T) ), lhs )
        code = ""
        for t,T in [codeof(x,nns) for x in rhs]:
            if code!="": code += ";"
            code += t
        assert type_accepts( ret[1], T ), "return type from function does not match declared type" 
        parms = " ".join(map( lambda(l,r):"(%s: %s)"%(nns[l],type_print(r)), args))
        return ("fun %s %s: %s = %s" % (name,parms,type_print(ret[1]),code), None)
    elif sx[0]=="datatype":
        ns[sx[1]] = (sx[1],'type') 
        for cons in sx[2:]:
            assert len(cons)==2
            ns[cons[0]] = (cons[0],['->',cons[1],sx[1]])
        return ( "datatype %s = %s;" % 
            (sx[1], ' | '.join([ (cons[0]+" of "+type_print(cons[1])) for cons in sx[2:]]) )
            , None )
        
    elif sx[0]==",":
        results = [ codeof(t,ns) for t in sx[1:] ]
        code = '('+ ','.join(map(lambda(l,r):l,results)) +')'
        type = '('+ '*'.join(map(lambda(l,r):r,results)) +')'
        return (code,type)
    elif re.match('#\d+',sx[0]): raise NotImplementedError()
    else:
        hd = sx[0]; tl = tuple(codeof(x,ns) for x in sx[1:])
        if isinstance(hd,str): 
            for weak in type_weaken(tl[0][1]):
                try: 
                    hd = ns[hd+" "+type_print(weak)]
                    break
                except KeyError: pass
            if isinstance(hd,str):
                raise KeyError("No method matching, %s %s" % (hd,str(tl[0][1])) )
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











