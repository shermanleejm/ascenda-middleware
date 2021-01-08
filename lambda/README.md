1. Run template 1
This requires the following flags 
--capabilities CAPABILITY_NAMED_IAM
--parameters ParameterKey=AWS::AccountId,ParameterValue=731706226892 ParameterKey=AWS::Region,ParameterValue=ap-southeast-1

2. Run template 2
This requires no additonal flags

Sample code for running:
aws cloudformation deploy --template lambda/template1.yaml --stackname shermanrox1 --region ap-southeast-1 