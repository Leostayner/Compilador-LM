Function Soma(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a = x + y
    Print a
    Soma = a
End Function

Function R() as Integer
    print 5
End Function

Function recursao(x as Integer) as Integer
    print(x)
    
End Function


Sub Main()
    Dim a as Integer
    Dim b as Integer
    a = 3
    Call R()
    Call recursao(5)
    b = Soma(a, 4)
    Print a
    Print b
End Sub