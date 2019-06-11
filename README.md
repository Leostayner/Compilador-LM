# Compilador-LM

### Program
![Diagrama1](./Imgs/PROGRAM.png)
<br>

### FuncDec
![Diagrama2](./Imgs/FuncDec.png)
<br>

### SubDec
![Diagrama2](./Imgs/SubDec.png)
<br>

### Statement
![Diagrama2](./Imgs/STATEMENT.png)
<br>

### Rel Expression
![Diagrama3](./Imgs/REL_EXPRESSION.png)
<br>

### Expression
![Diagrama4](./Imgs/EXPRESSION.png)
<br>

### Term
![Diagrama5](./Imgs/TERM.png)
<br>

### Factor
![Diagrama6](./Imgs/FACTOR.png)
<br>

### Type
![Diagrama7](./Imgs/TYPE.png)
<br>


### Compiler EBNF

program <br/>
    : func_dec | sub_dec<br/>
    ;<br/>

func_dec = "FUNCTION", identifier, "(", {(identifier, "AS", type) | ;}*, ")", "AS", type, "\n", {(statement, "\n")}*, "END", "FUNCTION" ;


sub_dec = "SUB", identifier, "(", {(identifier, "AS", type) | ;}*, ")", "\n", {(statement, "\n")}*, "END", "SUB" ;


statement   
    : IF, rel_expression, THEN, endline, {statement, endline}* ,{else, endline, {statement, endline}} , END , IF <br/>
    | identifier, "=", rel_expression <br/>
    | print, rel_expression<br/>
    | DIN, identifier, AS, type<br/>
    | WHILE, rel_expression, endline, {statement, endline}*, WEND <br/>
    | CALL, identifier, (, {(rel_expression| ;)}* , )
    ;

rel_expression <br/>
    : expression, { ("=" | ">" | <), expression } <br/>
    ;<br/>

expression <br/>
    : term, { ("+" | "-" | or), term } <br/>
    ;<br/>

term <br/>
    : fator, { ("*" | "/"| and), fator } <br/>
    ;<br/>

factor <br/>
    : ("+" | "-" | not), fator<br/> 
    | num <br/>
    | "(", rel_expression, ")"<br/> 
    | {identifier | (, {rel_expression , ;}* ,)}<br/>
    | input <br/>
    | (True | False)<br/>
    ;<br/>

identifier<br/> 
    : letter, { letter | digit | "_" } <br/> 
    ;<br/>

type<br/>
    : (Integer | boolean)<br/>
    ;<br/>

assignment<br/> 
    : identifier, "=", rel_expression<br/> 
    ;<br/>

print <br/>
    : "print", rel_expression<br/> 
    ;<br/>

num <br/>
    : digit, { digit }<br/> 
    ;<br/>

endline <br/>
    : \n<br/>

letter <br/>
    : ( a | ... | z | A | ... | Z )<br/> 
    ;<br/>

digit <br/>
    : ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) <br/>
    ;<br/>
