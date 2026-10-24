n=int(input("enter the number"))

count=0
number=2

while count<n:
    if_prime=True

    for i in range(2,number):
        if number%i==0:
            if_prime=False
            break

    if if_prime==True:
        print(number)
        count+=1
    number+=1
