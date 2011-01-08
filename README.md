
    unit    : type
    
    bool    : type
    true    : bool
    false   : bool
    and     : bool -> bool -> bool
    
    
    int     : type
    +       : int -> int -> int
    -       : int -> int -> int
    *       : int -> int -> int
    /       : int -> int -> int
    %       : int -> int -> int
    <       : int -> int -> int
    <=      : int -> int -> int
    >       : int -> int -> int
    >=      : int -> int -> int
    ==      : int -> int -> int
    !=      : int -> int -> int
    print   : int -> int -> int
    
    
    string  : type
    print   : string -> unit
    
    
    list    : type
    nil     : list 'a
    ::      : 'a -> list 'a -> list 'a
    
    
    ref     : type
    ref 'a  : 'a -> ref 'a
    
    
    ifile       : type
    ifile.open  : string -> ifile
    ifile.readAll : ifile -> string
    ifile.close : ifile -> unit
    
    ofile       : type
    ofile.open  : string -> ofile
    ofile.writeAll : ofile -> string -> unit
    ofile.close : ofile -> unit







