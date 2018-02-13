
Requirements
------------
This coding challenge has been developed in Python 3.4.4 version.

Python modules that are required and imported during code execution:
sys,
collections,
csv,
datetime,
string,
pytest,
bisect


Approach
--------------------------------
Decided to use Generators to iterate through the input file and process it 'lazily' line by line. This would enable us to process huge files that would not fit in memory. This function uses the 'yield' command to yield a value, remember its state so after the value has been dealt with it yields the next value and so on..

Filtered out unnecessary columns before performing computations on each row. Retained the following columns that is required for generating the output file:
CMTE_ID,
NAME,
ZIP_CODE,
TRANSACTION_DT,
TRANSACTION_AMT,
OTHER_ID

Used the python dictionary data structure:
1) to keep track of the output_key (CMTE_ID, ZIP_CODE, TRANSACTION_DT/YEAR)
2) to compute the values to store along with the keys - the running percentile, total amount of contributions, total number of contributions

As each row is read from the input file, the computations that are required for the output file, repeat_donors.txt is performed

Additionally, used the python list of lists data structure to store the computations (running percentile, total etc) The list data structure would help preserve the order of the lines appearing in the input file.


Source Code and Run Instructions
--------------------------------
The source code is in the file 'donation_analytics.py', located in the src folder
The shell script 'run.sh' contains the following command which will execute the code:

python ./src/donation_analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt


Flow of Execution
-----------------
The 'main()' module defines the structure of the input file and outlines the fields in it. This module  identifies the columns that are relevant for processing. The module also defines the key columns required to identify a donor and the key columns required to compute the donation metrics (running percentile, total amount of contributions, total number of contributions)
It calls the 'parse_input()'' module and passes the input filename and percentile filename parameters to it.
The 'parse_input()' module in turn calls the 'read_input()' module that reads the input file and hands over a row at a time to be processed. Once one row has been processed, the next row is handed over.
The 'parse_input()' module performs the needed computations and returns a list of lists data structure to the 'main()' module. The list of lists data structure is then written out to the repeat_donors.txt output file  

A time decorator module, 'time_decorator', has been included to capture the run time of the program

The code computes running percentile amount using nearest-rank method. The python sort module is used for the first sort. The sort module uses timsort method for sorting. This is a combination of merge and insertion sort. This is O(nlogn) Operation Complexity in the worst case. In best case when input is already sorted, it should run in linear time.
In this specific scenario since we need to append new value to the list and recompute percentile each time, the python bisect.insort module is optimal for re-computations. Since if the list is already sorted, then we just need to binary search the list for insertion point and insert the new value. This is O(n) Operation Complexity for Insertion in the worst case

Run Timing Results

First Run
----------
./run_tests.sh
Total time running parse_input: 0.004230022430419922 seconds
[PASS]: test_1 repeat_donors.txt
Total time running parse_input: 0.9205238819122314 seconds
[PASS]: test_2 repeat_donors.txt
[Tue Feb 13 08:28:04 PST 2018] 2 of 2 tests passed

Second Run
-----------
./run_tests.sh
Total time running parse_input: 0.003670930862426758 seconds
[PASS]: test_1 repeat_donors.txt
Total time running parse_input: 0.5931611061096191 seconds
[PASS]: test_2 repeat_donors.txt
[Tue Feb 13 08:43:26 PST 2018] 2 of 2 tests passed
