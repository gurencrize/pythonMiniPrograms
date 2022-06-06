from enum import Enum

class enumTest1(Enum):
    a=1
    b=2
    c=3
    d=4
    e=5

class enumtest2(Enum):
    a=10
    b=20
    c=30
    d=40
    e=50

# 引数の型を指定した時、それ以外の型で渡しても処理できればする
def printEnum(target:enumTest1):
    print(target)

printEnum(enumTest1.a)
printEnum(enumtest2.a)