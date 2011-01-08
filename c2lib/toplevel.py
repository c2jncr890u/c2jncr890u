

builtins.define( 'bool', 'bool', 'type' )
builtins.define( 'true', 'True', 'bool' )
builtins.define( 'false', 'False', 'bool' )
builtins.define( 'and', '(lambda a: lambda b: a and b)', ['->', 'bool', ['->','bool','bool']] )
builtins.define( 'or', '(lambda a: lambda b: a and b)', ['->', 'bool', ['->','bool','bool']] )

builtins.define( 'int', 'int', 'type' )
builtins.define( '+', '(lambda a: lambda b: a + b)', ['->','int',['->','int','int']] )
builtins.define( '-', '(lambda a: lambda b: a - b)', ['->','int',['->','int','int']] )
builtins.define( '*', '(lambda a: lambda b: a * b)', ['->','int',['->','int','int']] )
builtins.define( '/', '(lambda a: lambda b: a / b)', ['->','int',['->','int','int']] ) 
builtins.define( '%', '(lambda a: lambda b: a % b)', ['->','int',['->','int','int']] )
builtins.define( '<', '(lambda a: lambda b: a < b)', ['->','int',['->','int','bool']] )
builtins.define( '<=', '(lambda a: lambda b: a <= b)', ['->','int',['->','int','bool']] )
builtins.define( '>', '(lambda a: lambda b: a > b )', ['->','int',['->','int','bool']] )
builtins.define( '>=', '(lambda a: lambda b: a >= b)', ['->','int',['->','int','bool']] )
builtins.define( '==', '(lambda a: lambda b: a==b)', ['->','int',['->','int','bool']] )
builtins.define( '!=', '(lambda a: lambda b: a!=b)', ['->','int',['->','int','bool']] ) 
builtins.define( 'print', 'print_function', ['->','int','unit'] )

builtins.define( 'string', None, 'type' )
builtins.define( 'print', 'print_function', ['->','string','unit'] )

builtins.define( 'list', None, 'type')
builtins.define( '[]', '[]', 'list')
builtins.define( '+', '(lambda a: lambda b: a+b)', 
    ["->",
        ['list',"'a"],
        ['->',
            ["list","'b"],
            ["list",["|","'a","'b"]],
        ],
    ]
)
