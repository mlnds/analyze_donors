# Import Required Modules
import sys
from collections import defaultdict
from datetime import datetime
import csv
import string
import time
from functools import wraps
import bisect

# decorator module to compute the program run time
def time_decorator(function):
    @wraps(function)
    def timer_wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print ("Total time running %s: %s seconds" %
               (function.__name__, str(end_time-start_time))
               )
        return result
    return timer_wrapper

# Check validity of TRANSACTION_DT format to ensure it is not malformed
# This module is invoked by read_input module
def valid_date(trx_date):
    try:
        d = datetime.strptime(trx_date, '%m%d%Y')
    except ValueError:
        return False
    else:
        return True

# Check validity of NAME format to ensure it is not malformed
# This module is invoked by read_input module
def valid_name(name):
    name = name.replace(" ","")
    strip_name = "".join((char for char in name if char not in string.punctuation))
    n = strip_name.isalpha()
    return n

# Reads input file. This module is invoked by the parse_input module
# Using 'lazy'(generator) method with yield statement to process input file row by row instead of loading entire file into memory
# This method would work well for large files.
# Ensure the fields OTHER_ID, TRANSACTION_DT, ZIP_CODE, NAME, CMTE_ID and TRANSACTION_AMT meet the required criteria
# Only keep the required fields and filter out the rest
def read_input(filename, cols, cols_relevant):
    with open(filename) as f:
        for line in f:
            data = line.split('|')
            row = {k:v.strip() for k,v in zip(cols, data)}
            if not row['OTHER_ID']:
                if valid_date(row['TRANSACTION_DT']):
                    year = datetime.strptime(row['TRANSACTION_DT'], '%m%d%Y').year
                    row['TRANSACTION_DT'] = year
                    if len(row['ZIP_CODE']) >= 5:
                        row['ZIP_CODE'] = row['ZIP_CODE'][:5]
                        if valid_name(row['NAME']):
                            if row['CMTE_ID'] and row['TRANSACTION_AMT']:
                                row_filtered = {k:v for k,v in row.items() if k in cols_relevant}
                                yield row_filtered

# This module is called from the main module
# this module parses each row returned by the read_input module
# computes the running percentile amount, total amount of contributions and total transactions of contributions from repeat donors
# computes percentile amount using nearest-rank method. The python sort module uses timsort method for sorting. This is a combination of merge and insertion sort. O(nlogn) Operation Complexity worst case. In best case when input is already sorted, it should run in linear time.
# In this specific scenario since we need to append new value to the list and recompute percentile each time, the python bisect.insort module is optimal for recomputations. Since if the list is already sorted, then just need to binary search the list for insertion point and insert the new value. O(n) for Insertion worst case
# generates these computations by CMTE_ID, ZIP_CODE and YEAR
# returns these computations to the main module
@time_decorator
def parse_input(input_filename, percentile_filename, cols, cols_relevant, cols_donor_id, cols_output_id):
    donor_list = []
    total_amt_by_output_key = {}
    trx_amt_by_output_key = defaultdict(list)
    count_trx_by_output_key = {}
    aggregated_by_output_key_sublist = []
    aggregated_by_output_key_list = []

    with open(percentile_filename) as f:
        percentile = int(f.read())
        # print(percentile)

    for row in read_input(input_filename, cols, cols_relevant):
        # print(row)
        donor_key = tuple(row[c] for c in cols_donor_id)
        # print(donor_key)
        output_key = tuple(row[c] for c in cols_output_id)
        # print(output_key)
        if donor_key not in donor_list:
            donor_list.append(donor_key)
        else:
            total_amt_by_output_key[output_key] = total_amt_by_output_key.setdefault(output_key, 0) + float(row['TRANSACTION_AMT'])
            count_trx_by_output_key[output_key] = count_trx_by_output_key.setdefault(output_key, 0) + 1
            if trx_amt_by_output_key[output_key] is None:
                trx_amt_by_output_key[output_key].append(float(row['TRANSACTION_AMT']))
                trx_amt_by_output_key[output_key].sort()
            else:
                bisect.insort(trx_amt_by_output_key[output_key], float(row['TRANSACTION_AMT']))
            N = len(trx_amt_by_output_key[output_key])
            percentile_idx = int((percentile/100) * N)
            running_percentile = trx_amt_by_output_key[output_key][percentile_idx]
            aggregated_by_output_key_sublist = [row[c] for c in cols_output_id]
            aggregated_by_output_key_sublist.extend([round(running_percentile),round(total_amt_by_output_key[output_key]),count_trx_by_output_key[output_key]])
            aggregated_by_output_key_list.append(aggregated_by_output_key_sublist)

    return aggregated_by_output_key_list

# Main Module
# Defines columns found in the input file and columns needed for the computations
# Calls parse_input module to perform the needed computations. Passes the input file and percentile file parameter to this module
# Creates the output file 'repeat_donors.txt'
if __name__ == '__main__':
    cols = ['CMTE_ID','col2','col3','col4','col5','col6','col7','NAME','col9', 'col10', 'ZIP_CODE', 'col12','col13','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID', 'col17', 'col18', 'col19', 'col20', 'col21']
    cols_relevant = ['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT', 'OTHER_ID']
    cols_donor_id = ['NAME', 'ZIP_CODE']
    cols_output_id = ['CMTE_ID', 'ZIP_CODE', 'TRANSACTION_DT']
    output_list = parse_input(sys.argv[1], sys.argv[2], cols, cols_relevant, cols_donor_id, cols_output_id)

    with  open(sys.argv[3],'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')
        for item in output_list:
            writer.writerow([item[0], item[1], item[2], int(item[3]), int(item[4]), item[5]])
