import csv


def writeCSV(data, filepath):
    csvfile = open(filepath, "a", newline='')
    writer = csv.writer(csvfile)
    for i in data:
        writer.writerows([i])
    csvfile.close()


def writeStepCSV(data, filepath):
    csvfile = open(filepath, "a", newline='')
    for i in data:
        csvfile.write("%.3e,\n" % i[4])
    csvfile.close()
