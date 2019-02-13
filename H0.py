inp = input("Digite a operação: ")

op_list = []
signal  = ["+", "-"]

number = ""
result = 0

for n in inp:
    text = str(n)

    if text in signal:
        op_list.append(number)
        number = text

    elif text.isnumeric():
        number += text

if number != "":
    op_list.append(number)
      
for i in op_list:
    result += int(i)

print("Resultado: ", result)



