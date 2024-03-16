
# Data Processing and Analysis

script for Banking Document Data Processing and Analysis

## Requirements

#### Install Python 3.10.0
[Python3.10 ](https://www.python.org/downloads/release/python-3100/)

#### Install Numpy

```
pip install numpy==1.26.4

```

## Configure .csv file path
Please change the .csv file path in the **input_file** variable in script.py
```
    # provide file path .csv file 
    input_file = r"E:\script\banking_data_assignment.csv"
```
also change path where output files wnat to save in script.py
```
     # change output file path
     cleaned_output_file = r"E:\script\cleaned_banking_data.csv"
     individual_output_file = r"E:\script\individual_transactions.csv"
     aggregated_output_file = r"E:\script\aggregated_transactions.csv"
     anomalies_output_file = r"E:\script\anomalies_detected.csv"
```
## Run Script.py file 
Open the terminal where the script.py file is located and run the command:
```
python script.py
```
## output of Script.py  
on terminal basic output will show like this
```
individual_total 17320.0
aggregated_total -124248.0
Transaction totals not matching
13 anomalies detected
```
and seprate output files are generated on destination path

## How Script.py work
there is 4 main function
```

    1: clean_data

    2:separate_transactions

    3:reconcile_transactions

    4:detect_anomalies
```
#### Data cleaning
The **input_file** first goes to the **clean_data** function, which replaces all unwanted data, including negative values for withdrawal, from the account_number. After cleaning the data, it generates the **cleaned_output_file**.


#### Data Analysis
After generating the **cleaned_output_file**, we can separate individual and aggregated data using the **separate_transactions** function. This function creates two output files: **individual_output_file** and **aggregated_output_file**.

To check if individual and aggregated data match, we pass both the **individual_output_file** and **aggregated_output_file** to the **reconcile_transactions** function. This function sums all amounts from both files and then prints whether the transaction totals match or not.

#### Anomaly Detection 
For anomaly detection, we utilize the **detect_anomalies** function, setting a threshold of 1.6 and passing the **individual_output_file**. This function calculates the z-score of individual data amounts and compares it to the threshold. If the z-score is greater than the threshold, this data is passed to the **anomalies_output_file**.
