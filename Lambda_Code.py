import boto3
import datetime

rds_client = boto3.client('rds')
s3_client = boto3.client('s3')

rds_instance_id = 'mydb'
s3_bucket_name = 'rds-backup-bucket-25'
kms_key_id = 'arn:aws:kms:us-east-1:430118839072:key/f9dcca30-f3af-4931-af08-8be804b1a048'

def lambda_handler(event, context):
    try:
        snapshot_identifier = f"{rds_instance_id}-snapshot-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        rds_client.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=rds_instance_id
        )
        
        export_task_identifier = f"export-task-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        snapshot_arn = "arn:aws:rds:us-east-1:430118839072:snapshot:mydb-snapshot"  # Using the specific snapshot ARN
        iam_role_arn = 'arn:aws:iam::430118839072:role/Lambda-RDS-Backup-Role'

        rds_client.start_export_task(
            ExportTaskIdentifier=export_task_identifier,
            SourceArn=snapshot_arn,
            S3BucketName=s3_bucket_name,
            IamRoleArn=iam_role_arn,
            KmsKeyId=kms_key_id
        )
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
