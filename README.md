
Requirements
------------
This coding challenge has been developed in Python 3.4.4 version.

Python modules that are required and imported during code execution:
sys,
collections,
csv,
datetime


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
