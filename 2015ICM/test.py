import random
a = [random.gauss(50,20) for i in range(37000)]
a.sort()
print a[30/5*100]
print a[(30+150/5)*100]
print a[(30+150+110/5)*100]
print a[(30+150+110+25/5)*100]
print a[(30+150+110+25+25/5)*100]
print a[(30+150+110+25+25+20/5)*100]
print a[(30+150+110+25+25+20+10/5)*100]
