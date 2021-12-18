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


def writePdfCdf(div_center, div_count, cumulate_sum, pdf, cdf, filepath):
    if len(div_center) == len(pdf) and len(pdf) == len(cdf):
        csvfile = open(filepath, "w", newline='')
        for i in range(0, len(pdf), 1):
            csvfile.write("%lf,%d,%d,%lf,%lf,\n" % (
                div_center[i], div_count[i], cumulate_sum[i], pdf[i], cdf[i]))
        csvfile.close()
    else:
        print("data length error!")
        exit()


def result_output(all, same, close, smallestStep, largestCurrent, ratio, bit, outfile):
    print('\n')

    # Result output
    print(len(all), " Combinations in total.")
    outfile.write(format(len(all)))
    outfile.write(' Combinations in total.\n\n\n')

    print("Same: \n ", same)
    outfile.write("Same:\n ")
    outfile.write(format(same))
    outfile.write('\n')

    outfile.write("\n\n############################################\n\n")

    print("Close: \n ", close)
    outfile.write("Close:\n ")
    outfile.write(format(close))
    outfile.write('\n')

    outfile.write("\n\n############################################\n\n")

    print("For all close pairs:")
    for i in close:
        print(i, ':\n', close[i], '\ncurrent pair max step:', max(
            abs(i[2]-close[i][2]), abs(i[3]-close[i][3])))
        outfile.write(format(i)+':\n' + format(close[i]) + '\ncurrent pair max step:' + format(max(
            abs(i[2]-close[i][2]), abs(i[3]-close[i][3]))) + '\n\n')

    outfile.write("\n\n############################################\n\n")

    print("Smallest Step = ", smallestStep)
    outfile.write("Smallest Step = " + format(smallestStep)+"\n")

    print("Largest Current = ", largestCurrent)
    outfile.write("Largest Current = " + format(largestCurrent)+"\n")

    print("ratio = ", ratio)
    outfile.write("ratio = "+format(ratio)+"\n")
    print("bit = ", bit)
    outfile.write("bit = "+format(bit)+"\n")
