from pyspark import SparkConf,SparkContext

def create_spark_context():
    conf = (
        SparkConf()
        .setAppName("RDD-Ecommerce-Production-Pipeline")
        .setMaster("local[*]")
    )
    sc=SparkContext.getOrCreate(conf=conf)
    return sc

# if __name__=="__main__":
#     sc=create_spark_context()
#     print("Spark Context Created Sucessfully")
#     print("Application Name:",sc.appName)
#     print("Master:",sc.master)
#     sc.stop()