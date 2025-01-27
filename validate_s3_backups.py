import boto3

# Configuration
region_name = 'us-east-1'
s3_bucket_name = 'rds-backup-bucket-25'

# Initialize S3 client
s3_client = boto3.client('s3', region_name=region_name)

def validate_s3_exports():
    try:
        # List objects in the S3 bucket
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        if 'Contents' in response:
            print("Exported snapshots in S3 bucket:")
            for obj in response['Contents']:
                print(f"File: {obj['Key']} - Last Modified: {obj['LastModified']}")
        else:
            print("No exported snapshots found in the bucket.")
    except Exception as e:
        print(f"Error validating S3 exports: {str(e)}")

validate_s3_exports()
