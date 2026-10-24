n = int(input("Enter the number of students: "))

students = {}

for i in range(n):
    line = input("Enter the details: ").split()

    name = line[0]
    marks = float(line[1])

    students[name] = marks

topper = max(students.values())

for name in students:
    if students[name] == topper:
        print("Topper:", name, topper)

average = sum(students.values()) / n

print("Average:", average)