import math
import typing as tp


def calc(num1: float, command: str, num2=1.0) -> tp.Union[float, str]:
    if command == "+":
        return num1 + num2
    if command == "-":
        return num1 - num2
    if command == "*":
        return num1 * num2
    if command == "/":
        if num2 == 0:
            return "На ноль делить нельзя"
        return num1 / num2
    if command == "**":
        return num1**num2
    if command == "**2":
        return num1**2
    if command == "sin":
        return math.sin(num1)
    if command == "cos":
        return math.cos(num1)
    if command == "tan":
        if math.cos(num1) == 0:
            return "Аргумент не должен быть равен pi/2 + pi*k"
        return math.tan(num1)
    if command == "ln":
        if num1 <= 0:
            return "Аргумент должен быть положительным"
        return math.log(num1)
    if command == "log":
        if num1 <= 0:
            return "Аргумент должен быть положительным"
        return math.log10(num1)
    else:
        return f"Неизвестный оператор: {command!r}."


a = float(input("Введите первое число: "))
sign = input("Введите знак операции: ")
if sign in "+-/**":
    print(calc(a, sign, float(input("Введите второе число: "))))
else:
    print(calc(a, sign))
