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
    AMAZON_BEDROCK_METADATA: text, true
    AMAZON_BEDROCK_TEXT_CHUNK : text, true
    id: text, true
    x-amz-bedrock-kb-data-source-id: text, true
    x-amz-bedrock-kb-source-file-modality: text, true
    x-amz-bedrock-kb-source-uri: text, true

Instruction- :
    check again if AMAZON_BEDROCK_METADATA filtrable=false
Instruction- :
Create a Bedrock knowledge base named cdbac-kb In a similar technical configuration as ctx-kb knowledge base that is connected to an s3 bucket (cdbac-data)as data source in ca-central-1 (don't touch to any aconfiguration on ctx-kb)

already on ca-central-1, Create a Bedrock agent named cdbac-agent that uses Claude Sonnet 4.5 model, For agent instructions, use  Instructions-for-the-Agent.md file content 
add cdbac-kb knowledge base to the agent