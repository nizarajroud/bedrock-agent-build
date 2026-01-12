Instruction- :
    Create an S3 bucket named cdbac-data in ca-central-1

Instruction- :
    Create an S3 bucket named cdbac-audio in ca-central-1

Instruction- :
    in ca-central-1, Create an open search serverless Vector search data collection named cdbac-data-collection
        Redundancy not enabled
        Security easy  create

Instruction- :
    Once cdbac-data-collection created:
    Create an index named cdbac-dc-index
    Add a vector field with the following configuration: 
    - field name : cdbac-dc-index-vector
    - Engine : faiss
    - Precision : FP32
    - Dimensions : - 
    - Distance type : euclidiean
    - M : 16
    - ef_construction: 512
    - ef_search : -

    Create this metadata:
    AMAZON_BEDROCK_METADATA : text, false
    AMAZON_BEDROCK_TEXT_CHUNK : text, true
    id: text, true
    x-amz-bedrock-kb-data-source-id: text, true
    x-amz-bedrock-kb-source-file-modality: text, true
    x-amz-bedrock-kb-source-uri: text, true

From AWS console , DIY:
    Create a Bedrock knowledge base named cdbac-kb that uses the recently created data collection (including index and Vector configuration),
    Use this Metadata field mapping:
        Text field name : AMAZON_BEDROCK_TEXT_CHUNK
        Bedrock-managed metadata field name: AMAZON_BEDROCK_METADATA
Instruction- :
    already on ca-central-1, Create a Bedrock agent 
    name: cdbac-agent
    model : use category anthropic, model Claude Sonnet 4.5 v1 and inference profile = US Anthropic Claude Sonnet 4.5
    Instructions for the Agent : use  Instructions-for-the-Agent.md file content
    Knowledge Bases : cdbac-kb knowledge base

From AWS console , DIY:
    for cdbac-agent :select model : (uncheck Bedrock Agents optimized) use category anthropic, model Claude Sonnet 4.5 v1 and inference profile = US Anthropic Claude Sonnet 4.5
    Save
    prepare

Instruction- :
    Already in ca-central-1, create a Lambda function named cdbac-kb-sync that:
        uses code from kb_sync_lambda.py file name 
        Configure environment variables KNOWLEDGE_BASE_ID and DATA_SOURCE_ID with the values for cdbac-kb and its data source  respectively
        Configure the Lambda function to be triggered by s3 event notification (named cdbac-kb-auto-sync-trigger)on cdbac-data S3 bucket for All object create events
Instruction- :
    Already in ca-central-1, create a Lambda function named cdbac-mp3-transcribe-function that:
        uses code from kb_sync_lambda.py file name 
        Configure environment variables KNOWLEDGE_BASE_ID and DATA_SOURCE_ID with the values for cdbac-kb and its data source  respectively
        Configure the Lambda function to be triggered by s3 event notification (named cdbac-kb-auto-sync-trigger)on cdbac-data S3 bucket for All object create events