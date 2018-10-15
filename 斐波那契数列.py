x = input()
times = 0
n1 = 1
n2 = 1
while times <= x:
    if times == 0:
        print n1,n2,
        times += 1
    else:
        times += 1
        e = n1 + n2
        n1 = n2
        n2 = e
        print e,