from passlib.hash import argon2
import random
import math
import time
import re

def entropy(text):
        stat = {}
        leng = 0
        for znak in text:
                leng += 1
                if znak in stat:
                        stat[znak] += 1
                else:
                        stat[znak] = 1

        H = 0.0 
        for znak in stat:
                p_i = stat[znak] / leng
                H -= p_i * math.log2(p_i)
        return H

def generateTenValues():
    condition = True    
    while(condition):
        condition = False
        random.seed(time.perf_counter())
        randomNumbers = [random.randint(1, 30) for i in range(8)]
        sortedNumbers = sorted(randomNumbers)
        holder = -1
        for value in sortedNumbers:
            if holder + 1 == value or holder == value:
                condition = True
                continue
            else:
                holder = value
    return sortedNumbers


givenPassword = "aA1!b4B1FG"

if entropy(givenPassword) < 1.5:
    print("weak")
if entropy(givenPassword) >= 1.5 and entropy(givenPassword)<2.5:
    print("weak")
if entropy(givenPassword) >=2.5:
    print("strong")

if len(givenPassword) > 30 or len(givenPassword) < 10:
    print("incorrect password too long")

specialCharacters = "!@$%^&*[]"
lowerCase = True
upperCase = True
number = True
special = True

for char in givenPassword:
    if char.islower():
        lowerCase = False
    if char.isupper():
        upperCase = False
    if char.isdigit():
        number = False
    if char in specialCharacters:
        special = False

if lowerCase or upperCase or number or special:
    print("incorrect password must contain sth")

sequences = []

for i in range(10):
    sequences.append(generateTenValues())

passwords = []

for sequence in sequences:
    counter = 0
    password = ""
    for letter in givenPassword:
        if counter not in sequence:
            password += letter
        counter += 1
    passwords.append([password, sequence])

for password in passwords:
     
     print(password[0])
     print(password[1])

h = []
h = [argon2.hash(password[0]) for password in passwords]

print(h)
",".join(str(num) for num in passwords[i][1])
i=0
for password in h:
     print("INSERT INTO passwords (password, sequence, idUsername) VALUES ('"+ password +"', '"+ ",".join(str(num) for num in passwords[i][1]) +"','2');")
     i += 1



for i in range(len(h)):
    print(argon2.verify(passwords[i][0], h[i]))
