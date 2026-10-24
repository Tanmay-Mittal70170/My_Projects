# # s=input("enter the string")

# # if s.count("#")==s.count("*"):
# #     print("0 The string has equal number of # and *")

# # elif s.count("#")>s.count("*"):
# #     print("1 The string has greater number of # than *")

# # else:
# #     print("-1 The string has less number of # than *")


# # username=input("enter the string")
# # x=input("enter the name")
# # if x.lower()==username.lower():
# #     print("The username is valid")
# # else:
# #     print("the username is not valid")

# name=input("enter the name")

# english=int(input("enter the marks of English"))
# hindi=int(input("enter the marks of Hindi"))
# maths=int(input("enter the marks of maths"))
# science=int(input("enter the marks of science"))
# geography=int(input("enter the marks of geography"))
# History=int(input("enter the marks of History"))

# sum=english+hindi+maths+science+geography+History
# avg=sum/6

# print(name,"sum of marks",sum)
# print(name,"average of marks",avg)

# if avg>=90 and avg<100:
#     print(name,"Grade A+")
# elif avg>=80 and avg<89:
#     print(name,"Grade A")
# elif avg>=70 and avg<79:
#     print(name,"Grade B+")
# elif avg>=60 and avg<69:
#     print(name,"Grade B")
# elif avg>=45 and avg<59:
#     print(name,"Grade C")
# elif avg>=33 and avg<44:
#     print(name,"Grade D")
# else:
#     print(name,"Grade Fail")

# if avg>33:
#     print(name,"IS PASSED")
# else:
#     print(name,"IS FAILED")

# s=input("enter the string")
# c=s[::2]
# print("even position characters are",c)
# h=s[1::2]
# print("odd positions characters are",h)

# n = int(input("Enter how many prime numbers you want: "))
# for num in range(2,n+1):
#     is_prime=True

#     for i in range(2,num):
#         if num%i==0:
#           is_prime=False
#           break

#     if is_prime==True:
#       print(num)

# L=[]

# for x in range(3):
#     rollno=int(input("enter the roll no"))
#     name=input("enter the name")
#     email=input("enter the email")
#     phone=int(input("enter the phone number"))
#     t=rollno, name, email, phone
#     L.append(t)

# for r,n,e,p in L:
#     print("%5d %-15s %20s %10d"%(r,n,e,p))
# n=int(input())

# s=""

# for number in range(1,n+1):
#     new=str(number)
#     s+=new

# print(s)

# String =input("enter the string")

# Reverse=String[::-1]

# List=["a","e","i","o","u"]

# count=0

# for vowel in String:
#     if vowel in List:
#         count+=1

#     elif vowel ==" ":
#         new=vowel.replace("_")

# print(count)
# print(Reverse)
# print(String)

# for i in range(5,0,-1):
#     for j in range(1,i+1):
#         print(j,end="")
#     print()


# for i in range(0,5):
#     print(" "*i,end="")
#     for j in range(5-i):
#         print(chr(69-j),end="")
#     print()

# group=[1,2,3,4]
# search=int(input("Enter the number"))

# for element in group:
#     if element==search:
#         print("Element Found!!")
#         break
# else:
#     print("Element Not found")

# total = 0
# # loop will run at least once
# while True:
# # ask the user to enter a number
#     num = int(input("Enter a number (or 0 to exit): "))
# # exit the loop if the user enters 0
#     if num == 0:
#         break
# total += num
# # print the total
# print("Total:", total)

# x=10
# y=20
# def f1():
#     print("Hello")
# print(dir())

# l1 = [1,2,3]
# l2 = ['Rahul', 'Rakesh', 'Regina']
# print('Before extend l1 is:', l1)
# print('Before extend l2 is:', l2)
# l2.extend(l1)
# print('After extend l1 is:', l1)
# print('After extend l2 is:', l2)

# n=[1, 2, 3]
# n.remove(1)
# print(n)

# n=[1, 2, 3, 1]
# n.remove(1)
# print(n)

# n=[1, 2, 3, 4, 5]
# print(n.pop(1))
# print(n)
# print(n.pop())
# print(n)

# from functools import reduce

# n=int(input("enter the number of which you have to find the factorial"))

# l=[]

# for i in range(1,n+1):
#     l.append(i)

# factorial=reduce(lambda x,y:x*y,l)

# print(factorial)

# employee_ids = (1, 2, 3, 4, 5)
# print("same type of objects:",employee_ids)
# print(type(employee_ids))

# employee_ids = 1, 2, 3, 4, 5
# print("same type of objects:",employee_ids)
# print(type(employee_ids))

# name =("Sushanth",)
# print(name)
# print(type(name))

# emp_id = (11,)
# std_id = 120,
# print(emp_id)
# print(std_id)

# t=(10,20,30,40)
# t[1]=70

# print(t)

# t1=(10,20,30)
# t2=(40,50,60)
# t3=t1+t2
# print(t3)

# t1=(10,20,30)
# t2=t1*3
# print(t2)

# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# if 400 in d:
#     print(d[400])
# else:
#     print("key not found")


# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# print(d.get(1))
# print(d.get(100))

# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# print(d.get(1))
# print(d.get(100,'No key found'))


# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# print("Before pop:", d)
# d.pop()
# print("After pop:", d)

# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# print(d)
# for k in d.keys():
#     print(k)

# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# print(d)
# for k in d.values():
#     print(k)

# d = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# for k, v in d.items():
#     print(k, "---", v)

# d1 = {1: 'Ramesh', 2: 'Suresh', 3: 'Mahesh'}
# d2=d1.copy()
# print(d1)
# print(d2)
# print(id(d1))
# print(id(d2))

# squares={a:a*a for a in range(1,6)}
# print(squares)

# s = {10,20,30}
# l = [40,50,60,10]
# s.update(l)
# print(s)

# s = {10,20,30}
# l = [40,50,60,10]
# s.update(l, range(5))
# print(s)

# s={10,20,30}
# s.discard(59)
# print(s)

# x={10,20,30,40}
# y={30,40,50,60}
# print(x.symmetric_difference(y))
# print(x^y)

# s= {1, 2, 3, "Sharuk"}
# print(s)
# print(1 in s)
# print('S' in s)
# print(2 not in s)

# vowels = ('a', 'e', 'i', 'o', 'u')
# fSet = frozenset(vowels)
# print(fSet)
# print(type(fSet))


# name=input("enter the name")
# age=int(input("enter the age"))
# city=input("enter the name of the city")

# print(f"Hello {name}, you are {age} years old and live in {city}.")

# n=input("Enter the number")
# f=float(n)
# Int=int(f)
# comp=complex(f)

# print(f)
# print(Int)
# print(comp)

# n=int(input("enter the number you have to print the table"))

# for num in range(1,11):
#     if num==7:
#         break
#     else:
#         print(f"{n}x{num}={n*num}")

# string=input("enter the string")

# vowels=0

# List=input("enter the vowels space sperated").split()

# Reverse=string[::-1]

# for vowel in string:
#     if vowel.lower() in List or vowel.upper() in List:
#         vowels+=1

# string.replace(" ","_")

# print(string)

# print(Reverse)
# print(vowels)


# string = input("Enter the list separated: ").split()

# List = []

# for num in string:
#     new = int(num)
#     List.append(new)

# Sets = set(List)

# Final_List = list(Sets)

# print(List)
# print(Final_List)

# a=int(input())
# b=int(input())

# a,b=b,a

# print(a,b)

# n=int(input("enter the number of students"))

# students={}

# for details in range(n):
#     name=input("Enter the name of the student")
#     marks=int(input("Enter the marks of the student"))

#     students[name]=marks

# Max=max(students.items())
# Max_name,Max_marks=Max

# avg=sum(students.values())/n

# print(f"{Max_name} is having {Max_marks}")
# print(avg)

# List1=input().split()
# List2=input().split()

# new_list=[]
# new_list2=[]

# for num in List1:
#     number=int(num)
#     new_list.append(number)

# for digit in List2:
#     value=int(digit)
#     new_list2.append(value)

# comman=set(new_list) & set(new_list2)

# squares=[]

# for i in range(1,21):
#     if i%2==0:
#         square=i**2
#         squares.append(square)

# print(comman)
# print(squares)

# R1=float(input("enter the number 1"))
# X1=float(input("Enter the number 2"))

# R2=float(input("enter the number 3"))
# X2=float(input("enter the number 4"))

# z1=complex(R1,X1)
# z2=complex(R2,X2)
# z3=z1+z2

# print(f"{z3.real:.2f}")
# print(f"{z3.imag:.2f}")
# print(f"{abs(z3):.2f}")