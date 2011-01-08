c2 programming language
=======================

Dynamic languages need a "c" language to unite them.

+ No Syntax - Symbolic expressions make mechanical input simpler.
+ Any Syntax - custom syntax + proper blame-tracking is supported through annotated S-expressions. 
+ Value Semantics - Duck is a duck is a duck is a duck.
+ Flexible Type System - Less big words, more simple logic. It helps, not hinders.

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

Each file is referenced by a URI. No implicit namespace partitioning is performed, though duplicate imports will be eliminated. Circular imports will be found and scolded.

Macro System
------------

Hygienic macros will be supported to a limited extent. The major constraint here is that blame tracking needs to still work.  

