

def younger_person():
    ages = [72, 42, 32, 50, 56, 14, 78, 30, 51, 89, 12, 38, 67, 10]

    solution = ages[0]
    for age in ages:
        if age < solution:
            solution = age

    print(solution)

def statistics():
    data = [12,-1,123,345,412,4.55,123,23.4,123,4587,-129,94,956,14565,32, 0.001, 123]
    
    c = 0
    sumT = 0

    for i in data:
        c = c + 1
        sumT = sumT + i
    
    print(f"Elements: {c}")
    print(f"Elements: {len(data)}")
    print(f"Sum of elements: {sumT}")

    c = 0
    sumT = 0
    for i in data:
        if i < 0:
            c = c + 1
            sumT = sumT + i
    
    print(f"Sum of negative: {sumT}")
    print(f"Number of negative elements: {c}")

    c = 0
    sumT = 0
    for i in data:
        if i > 500:
            c = c + 1
            sumT = sumT + i
    
    print(f"Sum of numbers over500: {sumT}")
    print(f"Number of numbers over500: {c}")

def print_some_nums():
    # print 1 to 100
    for n in range(10, 110,10):
        print(n)
    
        




print("Test test test")
younger_person()
# statistics()
# print_some_nums()