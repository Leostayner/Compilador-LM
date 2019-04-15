# Compilador-LM

### Expression
![Diagrama](./Imgs/EXPRESSION.png)
<br>

### Factor
![Diagrama2](./Imgs/FACTOR.png)
<br>

### Rel Expression
![Diagrama3](./Imgs/REL_EXPRESSION.png)
<br>

### Statement
![Diagrama4](./Imgs/STATEMENT.png)
<br>

### Statements
![Diagrama5](./Imgs/STATEMENTS.png)
<br>

### Term
![Diagrama6](./Imgs/TERM.png)
<br>

### Compiler EBNF

statements = statement {\n , statement };

statement =  | num, "=", ecpression | print, expression, while, rel_expression, statements, wend | if, rel_expression, if, statements, {else, statements}, end, if; 

print = "print", expression ;

expression = term, { ("+" | "-" | or), term } ;

rel_expression = expression, { ("=" | ">" | <), expression } ;

term = fator, { ("*" | "/"| and), fator } ;

fator = ("+" | "-" | not), fator | num | "(", expression, ")" | identifier |input ;

identifier = letter, { letter | digit | "_" } ;

assignment = identifier, "=", expression ;

num = digit, { digit } ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
