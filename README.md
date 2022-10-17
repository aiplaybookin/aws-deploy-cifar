# Demo deployment using ECS and Fargate Spot

- Assumption 
-- Model is trained and stored in S3
-- Docker image is stored in ECR. e.g. Public ECR : https://gallery.ecr.aws/o8u9e4v2

Instructions on how to run the Container

## Create AWS ECS Cluster and Task

1. Go to ECS and click create cluster

2. Give an name and leave network and other settings as is

3. Hit 'Create'

Your cluster is automatically configured for AWS Fargate (serverless) with two capacity providers. Add Amazon EC2 instances, or external instances using ECS Anywhere.

If fails, logout login again create.

Note : Till here there is no services deployed or task running on clusters.

4. Next, Create a Task Definition under ECS

Go to ECS--> Task Definition -> Create new Task Definition

5. Give name to task e.g. CifarInferenceTask

6. Give name to repo, and get URI of repo and paste in Image URI, Get repo URI from ECR as see below

7. Change / add port e.g. 7860 if required

8. Env variables, if any

9. Specify the task size CPU, Memory as required by app

10. Task roles (Using S3 on Fargate will require a role to access S3 in Task Definition), network mode 

11. Uncheck logging if you do not wish (it is also charged $)

12. Create Task, Done!!


## Deploy

1. Go to Cluster created in step 1 above and click ```Deploy```

2. Compute configuration -> Capacity provider -> Choose ```Fargate Spot```

3. Deployment Configuration -> Select ```Service```
- **Service** : Launch a group of tasks handling a long-running computing work that can be stopped and restarted. For example, a web application. 
- **Task** : Launch a standalone task that runs and terminates. For example, a batch job. 

4. Specify the Task deifinition name (e.g. CifarInferenceTask) in Family text box with tags 

5. Specify Service Name, e.g. CifarService 

6. Security Group : Must select security group defined earlier with port enabled (e.g. testsg with port 80) 

7. Public IP is ```ON``` 

8. Load Balancer - not needed here (when you expect huge volume of requests) 
- Application LB 
- Network Load Balancer 

9. Hit Deploy, wait for few minutes 

NOTE : Go to Service -> Networking -> Service Role -> Add S3 full access to get access to s3 working in this group Got to Cluster-> Tasks (running one) -> click on task id hex -> Get Public IP In browser :80 , you app should run here!!


### Others :
- How to provide custom name model registry ?
- Save every inference input and output to S3, along with date and time of inference
    -[Ref-1](https://gradio.app/using_flagging/)
    -[Ref-2](https://github.com/gradio-app/gradio/blob/master/gradio/flagging.py)
- The Model S3 URI and the Inference input and output S3 URI must be changeable (environment variables)

Example: 
```
docker run -it your_image:latest -e "model=s3://my-bucket/models/resnet18.pth" -e "flagged_dir=s3://my-bucket/outputs/resnet18"
```
- HINT : Using S3 on Fargate will require a role to access S3 in Task Definition (Task role)
- HINT : Demo Web UI which runs on port 80 and be publicly accessible (Security Group must have publicly accessibile port 80 set)



- Generally prefered to have 2 workers per GPU . Or 12 cores CPU = 12 workers.