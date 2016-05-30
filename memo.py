# -*- coding:utf8 -*-
import sys
option = sys.argv[1]


if option == '-a':
    memo = sys.argv[2]
    f = open('memo.txt', 'a')
    f.write(memo)
    f.write('\n')
    f.close()

elif opriotn == '-v':
    f = open('memo.txt')
    memo = f.read()
    f.close()
    print(memo)