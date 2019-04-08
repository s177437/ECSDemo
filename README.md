#AWSFargateDemo

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

### How to deploy


### How to debug/run locally


### How to Contribute:
