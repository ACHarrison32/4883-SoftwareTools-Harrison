# Lecture One
```cpp
digraph G {
    rankdir = LR;
    
    node [shape = record]
    edge [arrowhead = vee color = blue]
    
    
    // Example 1
    //A;
    //B;
    //C;
    
    // Example 2
    //A [label = "<data> 1 | <next>"];
    //B [label = "<data> 2 | <next>"];
    //C [label = "<data> 3 | <next>"];
    
    // Example 3
    A [label = "<data> 1 | <next>"];
    B [label = "<data> 2 | <next>"];
    C [label = "<data> 3 | <next>"];
    
//=====================================================================================================//
    
    // Example 1 and 2 
    //A->B
    //B->C
    //C
    
    // Example 3
    //A:next:c->B:data [arrowhead = vee, arrowtail = dot, color = red, dir = both, tailclip = false]
    //B->C
    //C

}
```
