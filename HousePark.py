# -*- coding:utf8 -*-
class HousePark:
    lastname = "박"

    def __init__(self, name):
        self.fullname = self.lastname + name

    def travel(self, where):
        print("%s, %s여행을 가다." % (self.fullname, where))

    def love(self, other):
        print("%s, %s 사랑에 빠졌네" % (self.fullname, other.fullname))

    def __add__(self, other):
        print("%s, %s 결혼헀네" % (self.fullname, other.fullname))


class HouseKim(HousePark):
    lastname = "김"
    def travel(self, where, day):
        print("%s, %s 여행 %d일 가네" % (self.fullname, where, day))

pey = HousePark("응영")
juliet = HouseKim("줄리엣")
pey.love(juliet)
pey + juliet