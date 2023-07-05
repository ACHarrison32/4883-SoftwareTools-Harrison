## Code
```cpp
digraph linkedlist 
{        
        node [shape=record,color=red];
      
        A [label=" <prev> | <data> 5 | <next>  "];
        B [label=" <prev> | <data> 3 | <next>  "];
        C [label=" <prev> | <data> 8 | <next>  "];
        D [label=" <prev> | <data> 2 | <next>  "];
        E [label=" <prev> | <data> 7 | <next>  "];
        F [label=" <prev> | <data> 4 | <next>  "];
        G [label=" <prev> | <data> 9 | <next>  "];
        
        
        A:prev:c->B:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
        A:next:c->C:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
        B:prev:c->D:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
        C:prev:c->E:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
        B:next:c->F:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
        C:next:c->G:data [arrowhead=vee, arrowtail=dot, color=black, dir=both, tailclip=false];
}    
```

## Diagram
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A04/graphviz.svg">
