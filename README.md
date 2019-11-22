# Jenkins on AWS

## Project Structure

```
./

./cdk/ <-- Deployment configuration

./cdk/docker/ <-- Dockerfiles and associated config files for Master and Worker images

./cdk/app.py <-- cdk application file where all stacks are instantiated and built

./cdk/requirements.txt <-- Python module requirements

./cdk/jenkins/ <-- cdk stacks to deploy Jenkins environment
```


## Requirements

To deploy this environment, we will use the [aws-cdk](https://github.com/aws/aws-cdk)
- Please follow the requirements to install from the cdk github repo
- Tested with the following version: `1.15.0 (build bdbe3aa)`

## Fargate Jenkins (Master and Workers)

Set an environment variable as follows:
```bash
export FARGATE_ENABLED=True
```

## EC2 Backed Master and Fargate Workers
Set an environment variable as follows:
```bash
export EC2_ENABLED=True
```

## Validate configs and deploy

Navigate to the cdk directory, and run:

```bash 
cdk synth
```

Output should look something like:

```console
[user@computer cdk (cdk)]$ cdk synth
Successfully synthesized to jenkins-on-aws/cdk/cdk.out
Supply a stack name (JenkinsOnAWSNetwork, JenkinsOnAWSECS, JenkinsOnAWSWorker, JenkinsOnAWSJenkinsMaster) to display its template.
```

Feel free to check out the [CloudFormation](https://aws.amazon.com/cloudformation/) templates created by the cdk in the `cdk.out` directory

Let's deploy the environment! The below command will deploy all of the stacks required to get the environment up and running:

```bash
cdk deploy Jenkins*
```

_Note:_ You will be prompted for approval during the stages of the deploy. Follow the instructions on the prompt when asked.


That's it! You now have a fully serverless Jenkins implementation running on AWS Fargate with worker nodes automatically configured to run on an as needed basis.


