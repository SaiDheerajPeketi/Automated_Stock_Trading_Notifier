import csv

def write_lists(lists_to_write):
    with open("transactions.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for out_list in lists_to_write:
            writer.writerow(out_list)
