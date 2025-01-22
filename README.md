Scope
#####
this is a hello world app developed at python, and then it will be deployed at EKS Amazon, i am utilizing ECR as a private registry.

Creating ECR
##############
aws ecr create-repository --repository-name hello-world-repo --image-scanning-configuration scanOnPush=true --region us-east-1

Creating EKS Cluster at Amazon
#################################
eksctl create cluster --name eks-cluster-zealous --region us-east-1 --nodegroup-name zealous-workers --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 3 --managed --spot

Create a namespace where the app and components will be placed
#####################################################################
kubectl create ns application-ns

Creating balancer controller
#############################
refer to: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
  --cluster=eks-cluster-zealous \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::891376942769:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=eks-cluster-zealous \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller

Getting into cluster
######################
aws eks update-kubeconfig --region us-east-1 --name eks-cluster-zealous 

Pushing docker image
#####################
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 891376942769.dkr.ecr.us-east-1.amazonaws.com
docker tag hello:v1 891376942769.dkr.ecr.us-east-1.amazonaws.com/hello-world-repo:latest
docker push 891376942769.dkr.ecr.us-east-1.amazonaws.com/hello-world-repo:latest

create helm application
##########################
helm create hello-world-release 
helm upgrade hello-world-release 