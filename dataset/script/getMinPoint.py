import csv

f = open('result.csv', 'r')
reader = csv.reader(f, delimiter=":")
sorted_data = sorted(reader, key=lambda x : x[1])
for d in sorted_data:
    print d
f.close()