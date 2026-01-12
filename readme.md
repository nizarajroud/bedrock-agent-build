
on aws csna-opr-account
From this context , Provide clear and specific instructions for the task the bedrock Agent will perform. You can also provide certain style and tone.



===========


Create an S3 bucket named cdbac-data in ca-central-1

Create an S3 bucket named cdbac-audio in ca-central-1

Create a Bedrock knowledge base named cdbac-kb In a similar technical configuration as ctx-kb knowledge base that is connected to an s3 bucket (cdbac-data)as data source in ca-central-1 (don't touch to any aconfiguration on ctx-kb)

already on ca-central-1, Create a Bedrock agent named cdbac-agent that uses Claude Sonnet 4.5 model, For agent instructions, use  Instructions-for-the-Agent.md file content 
add cdbac-kb knowledge base to the agent# bedrock-agent-build
