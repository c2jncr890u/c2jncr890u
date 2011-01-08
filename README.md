
Top Level
---------
    type    : kind

    unit    : type unit

    bool    : type bool
    true    : bool
    false   : bool
    and     : bool * bool -> bool
    or      : bool * bool -> bool

    int     : type int
    +       : int * int -> int
    -       : int * int -> int
    *       : int * int -> int
    /       : int * int -> int
    %       : int * int -> int
    <       : int * int -> bool
    <=      : int * int -> bool
    >       : int * int -> bool
    >=      : int * int -> bool
    ==      : int * int -> bool
    !=      : int * int -> bool

    string  : type string    
    print   : string -> unit

    list    : type list
    []      : list
    cons    : 'a * list 'b -> list ('a | 'b) 
    +       : list 'a * list 'b -> list ('a | 'b) 


Module System
-------------

Each file is referenced by a URI and given its own namespace. 

    
