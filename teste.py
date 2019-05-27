
n = input()
fizz = 0000
buzz = 1111
fizzbuzz = 00001111
flag = True

while n > 0:
    tres = (n - (n / 3 * 3))
    cinco = (n - (n / 5 * 5))

    print (n)

    if (tres == 0) and (cinco == 0):
        print (fizzbuzz)
        flag = False

    if (tres == 0) and (flag == True):
        print (fizz)
        flag = False

    if (cinco == 0) and (flag == True):
        print (buzz)
        flag = False
    
    flag = True
    n = n - 1
