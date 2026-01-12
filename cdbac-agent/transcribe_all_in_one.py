import json
import boto3
import urllib.parse
import urllib.request
import time
import re
import os
from datetime import datetime

def lambda_handler(event, context):
    transcribe = boto3.client('transcribe')
    s3 = boto3.client('s3')
    
    # Get destination bucket from environment variable
    destination_bucket = os.environ.get('DESTINATION_BUCKET')
    if not destination_bucket:
        return {
            'statusCode': 500,
            'body': json.dumps('Missing required environment variable: DESTINATION_BUCKET')
        }
    
    # Get bucket and object from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Only process MP3 files
    if not key.lower().endswith('.mp3'):
        return {'statusCode': 200, 'body': 'Not an MP3 file'}
    
    # Generate job name and output key
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    clean_key = key.replace('/', '-').replace('.mp3', '').replace(' ', '_')
    # Remove any characters not allowed in job names
    clean_key = re.sub(r'[^0-9a-zA-Z._-]', '_', clean_key)
    job_name = f"transcribe-{timestamp}-{clean_key}"
    output_key = key.replace('.mp3', '.txt')
    
    try:
        # Start transcription job
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket}/{key}'},
            MediaFormat='mp3',
            LanguageCode='fr-CA',
            Settings={'ShowSpeakerLabels': False}
        )
        
        print(f"Started transcription job: {job_name}")
        
        # Wait for job completion (with timeout)
        max_wait_time = 600  # 10 minutes
        wait_time = 0
        
        while wait_time < max_wait_time:
            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            
            if status == 'COMPLETED':
                # Get transcript URL and extract text
                transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                
                # Download and parse transcript
                with urllib.request.urlopen(transcript_uri) as resp:
                    transcript_data = json.loads(resp.read().decode())
                
                # Extract clean text
                transcript_text = transcript_data['results']['transcripts'][0]['transcript']
                
                # Upload to destination bucket
                s3.put_object(
                    Bucket=destination_bucket,
                    Key=output_key,
                    Body=transcript_text.encode('utf-8'),
                    ContentType='text/plain'
                )
                
                print(f"Uploaded transcript to: {destination_bucket}/{output_key}")
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(f'Transcription completed: {output_key}')
                }
                
            elif status == 'FAILED':
                print(f"Transcription job failed: {job_name}")
                return {'statusCode': 500, 'body': 'Transcription failed'}
            
            # Wait 30 seconds before checking again
            time.sleep(30)
            wait_time += 30
        
        print(f"Transcription job timeout: {job_name}")
        return {'statusCode': 408, 'body': 'Transcription timeout'}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
