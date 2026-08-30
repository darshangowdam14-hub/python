import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from src.sparkSession import create_spark_context
from src.ingesion import read_file,remove_header
from src.partition import get_partition_data
from src.Parser import parser_transaction
from src.validators import validate_transactions
from src.common.utils import generate_run_id
from pathlib import Path
from src.transformation import format_parsing_rejects,format_validation_rejects


def main():
    
    sc = create_spark_context()
    
    run_id = generate_run_id()

    file_path = "data/raw/transactions_2026_08_21.csv" 
    source_file = Path(file_path).name
    rejected_path = (
        f"data/rejected/"
        f"{source_file.replace('.csv','')}_{run_id}"
    )

    raw_rdd = read_file(
        sc,
        file_path
    )

    print("Transaction  file loaded successfully")

    total_count = raw_rdd.count()
    print("total count including Header: ", total_count)

    print("Number of partitions: ", raw_rdd.getNumPartitions())

    partition_count_rdd = get_partition_data(raw_rdd)
    partition_count = partition_count_rdd.collect()

    for partition_index,count in partition_count:
        print(
            f"parition {partition_index}: {count} records"
        ) 

    header,act_data = remove_header(raw_rdd)

    print("Header: ", header)
    print("Count of actual data except header: ",act_data.count())
    
    parsed_rdd = act_data.map(parser_transaction)
    
    valid_parsed_rdd = parsed_rdd.filter(
        lambda record: record[0] == "VALID"
    )
    
    invalid_parsed_rdd = parsed_rdd.filter(
        lambda record: record[0] == "INVALID"
        )
    
    valid_transaction_rdd=valid_parsed_rdd.map(lambda record:record[1])
    
    validated_rdd=valid_transaction_rdd.map(validate_transactions)
    
    buiness_valid_rdd=validated_rdd.filter(lambda record:record[0]=="VALID")

    buiness_invalid_rdd=validated_rdd.filter(lambda record:record[0]=="INVALID")

    clean_transactions_rdd=buiness_valid_rdd.map(lambda record:record[1])
    
    formatted_parsing_rejects_rdd = invalid_parsed_rdd.map(format_parsing_rejects)
    
    formatted_validation_rejects_rdd = buiness_invalid_rdd.map(format_validation_rejects)
    
    all_rejected_rdd = formatted_parsing_rejects_rdd.union(formatted_validation_rejects_rdd)
    
    print("\nData")
    for record in all_rejected_rdd.take(10):
        print(record)
        
    all_rejected_rdd.saveAsTextFile(rejected_path)   

    

if __name__ == "__main__":
    print("Program started")
    main()
  