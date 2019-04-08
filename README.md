# ECSDemo

This repository contains a three part setup for provisioning an infrastructure with ability to run a simple HelloWorld application with the use of AWS ECS/Fargate. 
The repository contains three subrepos: 
 1. **Utils.SimpleVPCSetup** - Basic CloudFormation infrastructure setup for configuring a VPC with a loadbalancer setup. This infrastructure must be running before continuing deploying the sub-projects below.
 2. **Utils.HelloWorld** - CloudFormation setup + Dockerfile for running a small Flask based HelloWorld REST API in a AWS ECS container.
 3. **Utils.InstanceTagging** - Simple AWS Lambda that can be deployed with the use of the serverless framework. The lambda is currently configured to tag specific AWS resources with a global tag.
 

### System prerequisites 
#### Ansible Setup
In order to test this repo, you must have ansible installed locally. Please refer to documentation: [Installing Ansible Doc](https://www.cyberciti.biz/python-tutorials/linux-tutorial-install-ansible-configuration-management-and-it-automation-tool/) for installing ansible

#### Python 3.7
Python must be installed (version 3.6 or above). Refer to link: [Installing Python 3](https://realpython.com/installing-python/) for more information 

#### Docker 
Docker must be installed. Refer to [Installing Docker](https://docs.docker.com/get-started/) for more information. 

#### AWS CLI 
A working AWS must be installed locally on the machine. (Valid aws credentials must be available) for running the setup. 
AWS cli can be installed using `pip`

```bash 
pip install awscli
```
#### How to run the CFN templates locally
Copy the file `config/config.sample` into the file `config/config.yml``
```bash
cp config/config.sample config/config.yml
```
Replace the `aws_access_key` and `aws_access_secret` values with valid AWS credentials. (The credentials should have Administrator access to the AWS console where this setup is tested) 

### Utils.SimpleVPCSetup 
The setup can be executed by entering the following command (With a valid `config/config.yml` file available

```bash
cd Utils.SimpleVPCSetup
ansible-playbook site.yml -vvv # -vvv=verbose mode
```
**IMPORTANT** The `Utils.SimpleVPCSetup` must be configured before invoking the `Utils.HelloWorld` setup. The CFN-stack in `Utils.HelloWorld` relies on some output variables from `Utils.SimpleVPCSetup`.

### Utils.HelloWorld 
The CloudFormation setup can be executed by entering the following command (With a valid `config/config.yml` file available

```bash
cd Utils.HelloWorld
ansible-playbook site.yml -vvv # -vvv=verbose mode
``` 
A version of the HelloWorld Flask application is already pushed to Dockerhub. The provided image url should work out of the box.

The setup support uploading the docker repository to AWS ECR. For pushing manually to AWS ECR. Please refer to https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html 

In `config/config.yml` change the ´docker_image_url` if you want to use another docker image. 


### Utils.InstanceTagging
This is a serverless based project that deploys a lambda with ability to tag some AWS resources. The lambda has been specifically built to tag *all* AWS resources of a given type with the provided tag. (The referenced example tag is an owner tag)

You need to have serverless running locally to deploy the lambda. For information about setting up serverless, refer to https://serverless.com/framework/docs/providers/aws/guide/installation/

You need to have a local AWS credential with Programmatic access to the AWS console to deploy the application. Refer to https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html for info

Edit `Utils.InstanceTagging/variables.yml` if you want to change the tag name that is added to your AWS resources. 

To deploy the project, issue the following commands: 
```bash 
# Install the serverless-python-requirements using npm 
npm install --save serverless-python-requirements@4.2.5
serverless deploy --aws-profile <aws_profile_name> --stage dev --log-level debug
```
To run locally, boto3 must be installed. This can be installed with the provided pipfile. 
```bash
pipenv shell 
pipenv install
```
or by manually installing boto3 
```bash
pip install boto3
```

You can run the thing by issuing 

```bash
python test.py
```
