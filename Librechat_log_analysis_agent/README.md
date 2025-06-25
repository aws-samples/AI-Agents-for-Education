## Prerequisites of using the agent:
### Deploy librechat solution on AWS: https://github.com/sudheermanubolu/librechat-cdk/tree/main
### Create new S3 bucket in your AWS account, and upload the lambda layer pymongo-layer.zip to the bucket. Update the LambdaLayerS3Bucket CFN parameter with your bucket name.
### Update Librechat configuration file with below configuration to test the Bedrock Agent in LibreChat app
```yaml
  custom:
    - name: 'log-analysis-assitant'
      apiKey: '{AWS_API_GATEWAY_KEY}'
      baseURL: '{AWS_API_GATEWAY_URL}'
      models:
        default: ['Bedrock agent']
        fetch: false
      headers:
        x-api-key: '{AWS_API_GATEWAY_KEY}'
      titleConvo: true
      titleModel: 'us.amazon.nova-lite-v1:0'
      modelDisplayLabel: 'log-analysis-assitant'
      forcePrompt: false
      stream: false
      iconURL: 'https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/ai-ml/machine-learning/approved/images/256f3da1-3193-441c-b93c-b2641f33fdd6.a045b9b4c4f34545e1c79a405140ac0146699835.jpeg'
