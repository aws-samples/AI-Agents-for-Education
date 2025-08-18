## LibreChat Log Analysis Agent Infrastructure

### Prerequisites

Before you proceed to create the Agent, make sure you have Librechat solution deployed and running on AWS. For instructions on how to set it up, please refer to:
### https://github.com/sudheermanubolu/librechat-cdk/tree/main


## Infrastructure Overview

This CloudFormation template creates a serverless infrastructure for the LibreChat Log Analysis Agent, providing a custom endpoint that integrates with LibreChat solution. The architecture leverages AWS Bedrock AgentCore Runtime SDK with Strands Agents to deliver intelligent log analysis capabilities.

### Core Components

#### 1. API Gateway
- **REST API**: Creates a regional API Gateway with two main endpoints:
  - `/chat` - Standard chat interface for backward compatibility
  - `/chat/completions` - OpenAI-compatible endpoint for LibreChat integration
- **CORS Support**: Configured with proper CORS headers for cross-origin requests
- **API Key Authentication**: Secured with API key requirements and usage plans
- **Rate Limiting**: Throttling configured at 10 requests/second with burst capacity

#### 2. Lambda Functions

**API Gateway Lambda (`ApiGatewayLambda`)**
- Acts as a proxy between API Gateway and Bedrock AgentCore Runtime
- Handles both streaming and non-streaming responses
- Provides OpenAI-compatible response formatting for LibreChat
- Supports session management and conversation context
- Runtime: Python 3.12 on ARM64 architecture

**Bedrock AgentCore Deployment Lambda (`BedrockAgentCoreFunction`)**
- Creates and deploys the Bedrock Agent using Strands SDK
- Configures the agent with LibreChat log analysis capabilities
- Manages agent lifecycle and runtime deployment
- Executes during stack creation via Custom Resource

**MongoDB Analysis Lambda (`MongoAnalysisLambda`)**
- Contains all the agent tool functions for LibreChat data analysis
- Connects to DocumentDB/MongoDB to query LibreChat data
- Provides 7 core analysis functions:
  - `analyzeUserActivity` - User engagement patterns
  - `getConversationTrends` - Conversation trends over time
  - `analyzeUsagePatterns` - Usage patterns by hour/day
  - `getActiveUsers` - Most active users identification
  - `analyzeMessages` - Message content analysis
  - `getConversationSummary` - Recent conversation summaries
  - `getBasicStats` - Database statistics
- Deployed in VPC for secure DocumentDB access

#### 3. Lambda Layers
- **PyMongo Layer**: Provides MongoDB connectivity libraries
- **Strands AgentCore Layer**: Contains Strands SDK and Bedrock AgentCore dependencies for ARM64

#### 4. IAM Roles and Policies
- **DocDBLambdaExecutionRole**: Grants VPC access and Secrets Manager permissions for DocumentDB
- **BedrockAgentCoreLambdaExecutionRole**: Comprehensive permissions for Bedrock AgentCore operations, IAM role management, ECR, S3, and CodeBuild
- **ApiGatewayLambdaRole**: Permissions to invoke Bedrock AgentCore Runtime

#### 5. Security and Access Control
- **API Key Management**: Automatic generation of API keys with usage plans
- **VPC Integration**: MongoDB Lambda deployed in VPC for secure database access
- **Secrets Manager Integration**: Secure retrieval of DocumentDB credentials

#### 6. Monitoring and Observability
- CloudWatch Logs integration for all Lambda functions
- API Gateway access logging and metrics
- Configurable timeout and memory settings for optimal performance

### Architecture Benefits
- **Serverless**: No infrastructure management required
- **Scalable**: Automatically scales based on demand
- **Secure**: Multiple layers of security with VPC, IAM, and API keys
- **Cost-Effective**: Pay-per-use pricing model
- **LibreChat Compatible**: Native integration with LibreChat's OpenAI-compatible interface

## Deployment Steps

### Prerequisites
1. **LibreChat Deployment**: Ensure you have LibreChat deployed on AWS with DocumentDB
2. **VPC Information**: Gather VPC ID, subnet ID, and security group ID where DocumentDB is deployed
3. **AWS CLI**: Configure AWS CLI with appropriate permissions
4. **CloudFormation Access**: Ensure your AWS account has CloudFormation deployment permissions

### Step-by-Step Deployment

#### Step 1: Prepare Parameters
Before deploying, collect the following information from your LibreChat deployment by going to Cloudformation console:

```bash
# Parameters from your LibreChat setup (names may vary)
VPC_ID="vpc-xxxxxxxxx"          # VPC where DocumentDB is deployed
DOCDB_SUBNET="subnet-xxxxxxxxx" # Any private subnet in the VPC
DOCDB_SECURITY_GROUP="sg-xxxxx" # Use the one like *DocumentDBSecurityGroup*
DOCDB_SECRET_NAME="LibreChat/docdb/app-user"  # DocumentDB credentials secret name
```

#### Step 2: Deploy the CloudFormation Stack

1. Open AWS CloudFormation Console
2. Click "Create Stack" → "With new resources"
3. Upload the `librechat-log-analysis-agent-stack.yaml` file
4. Provide a stack name (e.g., `librechat-log-analysis-agent`)
5. Fill in the required parameters:
   - **VPCID**: Your VPC ID
   - **DocDBSubnet**: Your DocumentDB subnet ID
   - **DocDBSecurityGroupId**: Your DocumentDB security group ID
   - **DocumentDBSecretName**: Keep default unless modified
   - **BedrockModelId**: Keep default or specify preferred model
6. Review and create the stack

#### Step 3: Retrieve Deployment Outputs
After successful deployment, review the important outputs on CloudFormation console:

Key outputs include:
- **ChatEndpoint**: API Gateway endpoint for chat interface
- **ChatCompletionsEndpoint**: OpenAI-compatible endpoint
- **ApiKey**: API key for authentication
- **LibreChatConfigExample**: Configuration snippet for LibreChat

#### Step 4: Configure LibreChat Integration
Navigate to the S3 bucket that has Librechat configuration and add the following custom endpoint section to "librechat.yaml" file
1. apiKey: Copy the ApiKey from the stack outputs
2. x-api-key: Copy the API Key Secret for the key (API Gateway -> API Keys). 
3. baseURL - the InvokeURL from API Gateway "prod" stage (ex: https://xyz.execute-api.us-east-1.amazonaws.com/prod)
4. Add the configuration to your LibreChat environment (librechat.yaml):

```yaml
# Add to your LibreChat configuration
ENDPOINTS:
  custom:
    - name: 'log-analysis-assitant'
      apiKey: '<<REPLACE_ME>>'
      baseURL: '<<REPLACE_ME>>'
      models:
        default: ['Bedrock agent']
        fetch: false
      headers:
        x-api-key: '<<REPLACE_ME>>}'
      titleConvo: true
      titleModel: 'us.amazon.nova-lite-v1:0'
      modelDisplayLabel: 'log-analysis-assitant'
      forcePrompt: false
      stream: false
      iconURL: 'https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/ai-ml/machine-learning/approved/images/256f3da1-3193-441c-b93c-b2641f33fdd6.a045b9b4c4f34545e1c79a405140ac0146699835.jpeg'
```


#### Step 5: Verify LibreChat Integration
1. Restart your LibreChat application to load the new configuration
    - Go to ECS service in AWS Console
    - Locate Librechat cluster 
    - Find the LibreChatService inside the cluster
    - Select the service and do an Update/Deployment (do force deploy if necessary)
    - Wait for it to complete
2. Log into LibreChat interface, and you should see the "log-analysis-assitant" endpoint. Select "Bedrock Agent" model. 
3. Test with queries like:
   - "What's the user activity in the past 7 days?"
   - "Show me conversation trends for the last month"
   - "Who are the most active users?"

### Troubleshooting

**Common Issues:**

1. **VPC/Subnet Configuration**: Ensure the subnet has access to DocumentDB and internet connectivity for Lambda
2. **Security Group**: Verify the security group allows inbound connections on DocumentDB port (27017)
3. **Secrets Manager**: Confirm the DocumentDB secret exists and contains correct credentials
4. **API Key**: Ensure the API key is correctly configured in LibreChat

**Monitoring:**
- Check CloudWatch Logs for Lambda function errors
- Monitor API Gateway metrics for request/response patterns
- Review Bedrock AgentCore Runtime logs for agent execution details

### Cleanup
To remove all resources:

- Go to CloudFormation service on AWS Console
- Select the stack
- Click "Delete"

**Note**: This will permanently delete all created resources. Ensure you have backups of any important data or configurations.
