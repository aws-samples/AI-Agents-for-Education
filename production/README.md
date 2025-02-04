## To integrate with Streamlit front end:

pip install streamlit streamlit-chat

cd streamlitapp

streamlit run genericstreamlitapp.py

## To integrate with Lex front end:

deploy cloudformation template under lexapp directory 

## To setup KB using cloudformation templates:

Setting up OpenSearch Serverless (Collection, dashboard, index) 
- Have access to your IAMUserArn. This can be obtained using Cloud9 command - `aws sts get-caller-identity --query Arn --output text` 
- Go to cloudformation on AWS Console and Upload the `OpenSearch-Serverless.yml` and enter the parameters like stack name and IAMUserArn (output of above command)
- Create Stack and wait for the resources to be created. 
- Once the stack is created, Go to the Amazon OpenSearch Service in the AWS Console, and under the Collections section, you will see the collection we just created. Click to open the collection “rag-bedrock-kb” and under the Indexes tab, click “Create vector index.” The default vector index name used by this template is - `rag-bedrock-index`. Add a field: `vector` dimension: `1024` engine:`faiss` distance: `Euclidean`
- Click create index and make sure index is created

Setting up Bedrock Knowledge Base 
- We will need the outputs from OpenSearch-serverless stack to create this one in cloudformation. 
- Go to cloudformation on AWS Console and Upload the `Bedrock-Kb.yml` and enter the stack name. 
- Enter the parameters  `AmazonBedrockExecutionRoleForKnowledgeBasearn` , `CollectionARN` and `S3BucketName` as DataSource by fetching the values from output of previous stack. (Can be found under Outputs tab of previous Cloudformation Stack)
- And then click create Stack and the knowledge base will be created and ready for use. 

****Sync data****

Upload sample document to S3 bucket (the one from previous step) -
- Download course catalog sample from here: https://www.portervillecollege.edu/_resources/assets/pdfs/Academics/2024-2025_Catalog.pdf 
- Upload the pdf to S3
- Sync Bedrock Knowledge Base
