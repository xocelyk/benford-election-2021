import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

new_data = list()
with open('copied_election_data.csv', 'r') as f:
    reader = csv.reader(f)
    line_data = []
    cell_num = 1
    header = []
    for line in reader:
        if cell_num % 2 == 1:
            line_data.append(line[0].strip())
            if cell_num < 18:
                header.append(line[0].strip())
        if cell_num % 18 == 16:
            if 'Precinct' not in line_data:
                new_data.append(line_data)
            line_data = []
        cell_num += 1

header = ['index', 'precinct', 'biden', 'trump', 'jorgensen', 'blankenship', 'hawkins', 'delafuente', 'total']
df = pd.DataFrame(new_data[1:], columns=header)
df.to_csv('election_data.csv')

def gen_benford(df, col_name):
    digits = {}
    total_digits = 0
    for i in range(1, 10):
        digits[i] = 0
    column = df[col_name]
    for num in column:
        num = num.replace(',', '')
        if num == '0':
            continue
        dig = int(num[0])
        assert num.isnumeric()
        total_digits += 1
        digits[dig] += 1
    for key, item in digits.items():
        digits[key] = item/total_digits
    return digits

biden = gen_benford(df, 'biden')
biden_list = []
for key, item in biden.items():
    biden_list.append(item)
trump = gen_benford(df, 'trump')
trump_list = []
for key, item in trump.items():
    trump_list.append(item)
jorgensen = gen_benford(df, 'jorgensen')
jorgensen_list = []
for key, item in jorgensen.items():
    jorgensen_list.append(item)

x = [i for i in range(1, 10)]

true_benford = [.301, .176, .125, .097, .079, .067, .058, .051, .048]

width = np.array(.2)

fig = plt.figure()
ax = fig.add_subplot(111)
# rects1 = ax.bar(x + -1.5*width, true_benford, width, color='seagreen')
rects1 = ax.plot(x, true_benford, c='seagreen')
rects2 = ax.bar(x - width, trump_list, width, color='red')
rects3 = ax.bar(x, biden_list, width, color='royalblue')
rects4 = ax.bar(x + width, jorgensen_list, width, color='orange')

plt.xticks(ticks=[i for i in range(1,10)], labels=[str(i) for i in range(1,10)])
ax.set_ylabel('first digit occurence')
ax.set_xlabel('digit')
ax.set_title('Detroit Precinct Benford')

ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), ('true benford', 'trump', 'biden', 'jorgensen') )

plt.show()

#
# plt.plot(x, true_benford, c='g')
# plt.plot(x, biden_list, c='b')
# plt.plot(x, trump_list, c='r')
# plt.plot(x, jorgensen_list, c='y')
# # plt.scatter(x, true_benford, biden_list, trump_list, jorgensen_list)
# plt.show()
# # print(len(new_data))
# # for line in new_data:
# #     print(line)
