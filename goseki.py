ls=[65,75,80,100]
target=750
a=1
b=0
c=0
d=0

while True:
    if (ls[0]*a+ls[1]*b+ls[2]*c+ls[3]*d)==target:
        print(f"{ls[0]}×{a}+{ls[1]}×{b}+{ls[2]}×{c}+{ls[3]}×{d}")
    a+=1
    if ls[0]*a>target:
        a=0
        b+=1
        if ls[1]*b>target:
            b=0
            c+=1
            if ls[2]*c>target:
                c=0
                d+=1
                if ls[3]*d>target:
                    break
print('done')