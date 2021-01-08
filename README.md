# Running Instructions
### Running Django Backend (Windows Commands)
```bash
$ pip install virtualenv
$ virtualenv --version # just test O.K
$ cd initial_app\ascendas_apps\itsa_backend
$ virtualenv venv # default, in .gitignore
$ venv\Scripts\activate.bat # assuming you're in project_folder
$ pip install -r requirements.txt
$ cd itsa_backend
$ python manage.py runserver
```

### EB Configs
vpc-01c86d7583e799403
subnet-034262533c13e31c7,subnet-0e82e659052960d44
subnet-025664adf0602ca48,subnet-011b66e17c3b9b32e
sg-0717fa10e232af881,sg-0bcc610785acd29e2

# Steps to replicate our environment
1. Run Terraform commands as stated in section below in our AWS Organisation, change neccesary variables if needed
2. Run Lambda Setup Instructions below
3. Do API Gateway Setup instructions below

### TERRAFORM COMMANDS
#### COMMANDS TO REPLICATE ENV
```bash
$ cd eb_terraform
$ terraform plan -var-file=fixtures.tfvars 70+ resources
$ terraform apply -var-file=fixtures.tfvars
```
#### COMMANDS TO DESTROY ENV
`$ terraform destroy -var-file=fixtures.tfvars`

### API Gateway Setup
1. Replace the backend url with the deployed beanstalk url from terraform
2. Import API Gateway using REST API
3. Select Swagger File from project folder and Click Import. 
4. Import `api-gateway-configs.json` in root folder
5. Deploy API and Select New Deployment Stage
6. Create a new Deployment Stage with prod as the name and click on deploy
7. Go to Usage Plans and Click on Create
8. Enter a Name (prod) and enter 500 for Rate and 300 for Burst and 1000 requests for Quota
9. Add Associated API Stage prod for the Usage Plan
10. Add API Key to Usage Plan and Add Bank API Key to the Usage Plan
11. Deploy API and Enable API Cache and Save Changes
12. Go to stages and change /users resource settings to disable CloudWatch Logs and disable Method Cache and Save changes

### Lambda Setup
1. Run template 1
This requires the following flags 
```bash
--capabilities CAPABILITY_NAMED_IAM
--parameters ParameterKey=AWS::AccountId,ParameterValue=731706226892 ParameterKey=AWS::Region,ParameterValue=ap-southeast-1
```
Change the `accountid` and `region` to what suits you

2. Run template 2
This requires no additonal flags

Sample code for running:
aws cloudformation deploy --template lambda/template1.yaml --stackname shermanrox1 --region ap-southeast-1 

# SECRETS NEEDED FOR DEV AND PROD PIPELINES
1. `AWS_ACCESS_KEY_ID`: AWS Access Key ID
2. `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key
3. `DEV_EB_DOMAIN`: Development Elastic Beanstalk Domain
4. `PROD_EB_DOMAIN`: Production Elastic Beanstalk Domain
5. `RDS_DEV_HOST`: RDS Development Host
6. `RDS_PASSWORD`: RDS Development Password
7. `RDS_USER`: RDS Development Username
8. `RDS_PROD_HOST`: RDS Production Host
9. `RDS_PROD_PASSWORD`: RDS Production Host Password
10. `RDS_PROD_USER`: RDS Production Username

# Application

## Screenshots
### Bank Application
[![image.png](https://i.postimg.cc/xTns5ZJw/image.png)](https://postimg.cc/pycYXqBC)
[![image.png](https://i.postimg.cc/hPDrT7Ng/image.png)](https://postimg.cc/V5hnc5YH)
[![image.png](https://i.postimg.cc/sDHpWHp9/image.png)](https://postimg.cc/gnRXFDtn)
[![image.png](https://i.postimg.cc/Jn8J8fLm/image.png)](https://postimg.cc/Z9f0FDnD)
[![image.png](https://i.postimg.cc/Fs6Lzd4T/image.png)](https://postimg.cc/8jh5nCsv)
[![image.png](https://i.postimg.cc/9fY0dz65/image.png)](https://postimg.cc/DWm7FffB)
[![image.png](https://i.postimg.cc/KvTZ7RTq/image.png)](https://postimg.cc/LnHK24NL)

### Loyalty Partner Application
[![image.png](https://i.postimg.cc/PqTr5TP6/image.png)](https://postimg.cc/FYCQPtbc)

## Demo Videos
### Application Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/7o445uO3m9o/0.jpg)](https://www.youtube.com/watch?v=7o445uO3m9o)

### CICD Pipeline Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/IVqaVrpS7Bs/0.jpg)](https://www.youtube.com/watch?v=IVqaVrpS7Bs)
