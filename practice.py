n_english=int(input())
n_french=int(input())

english=[]
french=[]

for i in range(n_english):
    rollno=int(input())
    english.append(rollno)
    
for j in range(n_french):
    roll_no=int(input())
    french.append(roll_no)
    
E_set=set(english)
F_set=set(french)

Intersection=E_set&F_set

total=len(Intersection)

print(total)