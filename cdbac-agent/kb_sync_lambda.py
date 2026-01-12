import json
import boto3
import urllib.parse
import os

def lambda_handler(event, context):
    bedrock_agent = boto3.client('bedrock-agent')
    
    # Get knowledge base and data source IDs from environment variables
    knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID')
    data_source_id = os.environ.get('DATA_SOURCE_ID')
    
    if not knowledge_base_id or not data_source_id:
        return {
            'statusCode': 500,
            'body': json.dumps('Missing required environment variables: KNOWLEDGE_BASE_ID or DATA_SOURCE_ID')
        }
    
    # Get bucket and object from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    print(f"Object {key} added to bucket {bucket}")
    
    try:
        # Start ingestion job for the data source
        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
            description=f'Auto-sync triggered by {key}'
        )
        
        ingestion_job_id = response['ingestionJob']['ingestionJobId']
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Knowledge base sync started: {ingestion_job_id}')
        }
        
    except Exception as e:
        print(f"Error starting ingestion job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
