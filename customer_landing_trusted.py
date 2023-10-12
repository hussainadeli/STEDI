import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Amazon S3
AmazonS3_node1697115644642 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="customer_landing_tbl",
    transformation_ctx="AmazonS3_node1697115644642",
)

# Script generated for node SQL Query
SqlQuery0 = """
SELECT *
FROM myDataSource
WHERE sharewithresearchasofdate IS NOT NULL AND sharewithresearchasofdate <> 0;

"""
SQLQuery_node1697116432774 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"myDataSource": AmazonS3_node1697115644642},
    transformation_ctx="SQLQuery_node1697116432774",
)

# Script generated for node customer_trusted
customer_trusted_node1697116569307 = glueContext.write_dynamic_frame.from_catalog(
    frame=SQLQuery_node1697116432774,
    database="stedi_db",
    table_name="customer_trusted",
    transformation_ctx="customer_trusted_node1697116569307",
)

job.commit()