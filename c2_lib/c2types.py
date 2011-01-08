
def uuid( n=[0] ):
    n[0] += 1
    return "us_"+str(n[0])

def type_accepts( l, r ): return l==r
def type_print( t ):
    if isinstance(t,str):
        if t.startswith("'"): return t
        assert t in global_ns and global_ns[t][1]=='type', t
        return global_ns[t][0]
    elif t[0]=="->": return "("+"->".join(map(type_print,t))+")"
    elif t[0]=="*": return "("+"*".join(map(type_print,t))+")"
    else: return "("+" ".join(map(type_print,t[-1:]+t[:-1]))+")"
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
    yield "'a"