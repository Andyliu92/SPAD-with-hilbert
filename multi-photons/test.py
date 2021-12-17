import csv
csvfile = open("csv.csv", "w", newline='')
writer = csv.writer(csvfile)
writer.writerow(['row1', 'row2', 'row3', 'row4'])
data = [('1', '2', '3', '4'), ('4', '5', '6', '7')]
writer.writerows(data)
csvfile.close()
