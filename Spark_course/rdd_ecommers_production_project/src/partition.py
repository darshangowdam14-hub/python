def get_partition_data(raw_rdd):
    def count_record(index,records):
        count=0
        for record in records:
            count+=1
        yield(
            index,count
        )    
    return raw_rdd.mapPartitionsWithIndex(count_record)    