
def codeof( sx, ns=global_ns ):
    if isinstance(sx, str): 
        if re.match("\d+",sx): return (sx,"int")
        elif re.match('^".*"$',sx): return (sx,"string")
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
    elif sx[0]=="let":
        lhs, half, rhs = [],False,[]
        for part in sx[2:]:
            if half: rhs.append( part )
            elif part=="in": half = True
            else: lhs.append( part )  
        nns = {}; nns.update(ns)
        map( lambda(t,T): nns.__setitem__( t, (uuid(),T) ), lhs )
        code = ""
        for t,T in [codeof(x,nns) for x in rhs]:
            if code!="": code += ";"
            code += t
        lets = " ".join(map( lambda(l,r):"val %s = %s"%(nns[l],codeof(r)[0]), lhs))
        return ("let %s in %s end" % (lets,code), T)
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
