import csv
def write_lists(out_list):
    with open("transactions.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(out_list)
