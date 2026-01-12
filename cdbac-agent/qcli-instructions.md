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
    already on ca-central-1, Create a Bedrock agent named cdbac-agent that uses Claude Sonnet 4.5 model, For agent instructions, use  Instructions-for-the-Agent.md file content 
    add cdbac-kb knowledge base to the agent