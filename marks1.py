# -*- coding:utf8 -*-
marks = [90, 25, 67, 45, 80]

for mark in marks:
    if mark >= 60:
        print("%d번 학생은 합격입니다." % mark )
    else:
        print("%d번 학생은 불합격입니다." % mark )