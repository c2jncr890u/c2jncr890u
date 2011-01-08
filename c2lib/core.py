
import parser
import codegen

def make( fp ):
    assert fp.endswith(".c2")
    for stmt in parser.load(fp):
        put_stmt(stmt)
    prg = get_program()        
    codegen.to_py(fp[:-3]+".py",prg)
