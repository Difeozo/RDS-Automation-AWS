import boto3

# AWS Configuration
rds_client = boto3.client('rds', region_name='us-east-1') 
rds_instance_id = 'mydb'  

def validate_backups():
    try:
        snapshots = rds_client.describe_db_snapshots(DBInstanceIdentifier=rds_instance_id)
        for snapshot in snapshots['DBSnapshots']:
            print(f"Snapshot {snapshot['DBSnapshotIdentifier']} - Status: {snapshot['Status']}")

        completed_snapshots = [
            snapshot for snapshot in snapshots['DBSnapshots'] if snapshot['Status'] == 'available'
        ]
        if completed_snapshots:
            print(f"Found {len(completed_snapshots)} completed snapshot(s). Validation passed.")
        else:
            print("No completed snapshots found. Validation failed.")
    except Exception as e:
        print(f"Error validating snapshots: {str(e)}")

if __name__ == "__main__":
    validate_backups()
