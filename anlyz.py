f = open('results.csv', 'r')
f.readline()

s_tv, s_ti, s_rv, s_ri = (0, 0, 0, 0)

i = 0
for line in f:
    i += 1
    tv, ti, rv, ri = line.split(',')
    
    s_tv += float(tv)
    s_ti += float(ti)
    s_rv += float(rv)
    s_ri += float(ri)

print('Avg time (video): {}\nAvg time (interactions): {}\nAvg rate (video): {}\nAvg rate (interactions): {}'.format(s_tv / i, s_ti / i, s_rv / i, s_ri / i))