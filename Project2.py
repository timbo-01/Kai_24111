import random
import string
lower = string.ascii_lowercase
upper = string.ascii_uppercase
digits = string.digits
special = "!@#$%^&*()-_=+[]{};:,.<>?/|~"

while True:
    try:
        length = int(input("Какая должна быть длина пароля? "))
        if length < 1:
            print("Длина должна быть больше 0")
            continue
        break
    except ValueError:
        print("Введите число")

print("\nКакие типы символов использовать?")
print("1 - строчные буквы (abc)")
print("2 - заглавные буквы (ABC)")
print("3 - цифры (123)")
print("4 - спецсимволы (!@#)")
print("Можно ввести несколько цифр подряд, например: 1234")

while True:
    choice = input("Ваш выбор: ").strip()

    if not choice:
        print("Введите хотя бы одну цифру")
        continue

    valid = True
    for c in choice:
        if c not in "1234":
            valid = False
            break

    if not valid:
        print("Можно вводить только цифры от 1 до 4")
        continue

    break

pools = []
if "1" in choice:
    pools.append(lower)
if "2" in choice:
    pools.append(upper)
if "3" in choice:
    pools.append(digits)
if "4" in choice:
    pools.append(special)

if length < len(pools):
    print(f"Длина должна быть хотя бы {len(pools)}, чтобы вместить все выбранные типы")
    exit()

password_chars = []

for pool in pools:
    password_chars.append(random.choice(pool))

all_chars = "".join(pools)
while len(password_chars) < length:
    password_chars.append(random.choice(all_chars))

random.shuffle(password_chars)

password = "".join(password_chars)
print(f"\nВаш пароль: {password}")