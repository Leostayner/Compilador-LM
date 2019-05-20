# Compilador-LM

### Program
![Diagrama1](./Imgs/PROGRAM.png)
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
    : SUB, MAIN, "(", ")", endline {statement, endline}, END, SUB<br/>
    ;<br/>

statement   
    : IF, rel_expression, THEN, endline, {statement, endline}* ,{else, endline, {statement, endline}} , END , IF <br/>
    | identifier, "=", rel_expression <br/>
    | print, rel_expression<br/>
    | DIN, identifier, AS, type<br/>
    | WHILE, rel_expression, endline, {statement, endline}*, WEND <br/>
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
    | identifier <br/>
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
