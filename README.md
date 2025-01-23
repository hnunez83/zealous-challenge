# Zealous Challenge - Deploy to Amazon EKS with Helm and Validation

This project demonstrates how to deploy a containerized application to an Amazon EKS cluster using Helm and GitHub Actions, with built-in validation for readiness and liveness probes.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. AWS Setup](#1-aws-setup)
  - [2. GitHub Secrets Configuration](#2-github-secrets-configuration)
- [Workflow Overview](#workflow-overview)
- [Helm Deployment Details](#helm-deployment-details)
- [Validation Steps](#validation-steps)
- [License](#license)

---

## Prerequisites

Ensure you have the following set up before proceeding:

- **AWS CLI** installed and configured with sufficient permissions.
- **kubectl** installed and configured to access your EKS cluster.
- **Helm** installed (v3 or later).
- A Docker repository in Amazon ECR.

---

## Setup Instructions

### 1. AWS Setup

## Creating ECR

aws ecr create-repository --repository-name hello-world-repo --image-scanning-configuration scanOnPush=true --region us-east-1

## Creating EKS Cluster at Amazon

eksctl create cluster --name eks-cluster-zealous --region us-east-1 --nodegroup-name zealous-workers --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 3 --managed --spot

## Creating balancer controller
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


## Workflow Overview
This repository contains a GitHub Actions workflow that performs the following steps:

Checkout the code from the repository.
Configure AWS credentials to access EKS and ECR.
Build and push the Docker image to Amazon ECR.
Deploy the application using Helm to an EKS cluster.
Validate readiness and liveness probes via Kubernetes Ingress.
Perform rollback in case of a failed rollout.
The workflow file is located at .github/workflows/deploy.yml

## Helm Deployment Details
Helm Chart Structure
This repository uses a Helm chart located at ./hello-world-release/. The chart structure is as follows:

hello-world-release/
├── Chart.yaml       # Chart metadata
├── values.yaml      # Default configurations
├── templates/
│   ├── deployment.yaml   # Kubernetes Deployment
│   ├── ingress.yaml      # Kubernetes Ingress
│   └── service.yaml      # Kubernetes Service
│   └── ns.yaml           # Kubernetes namespace

## Validation Steps
The following validations are performed as part of the CI/CD pipeline:

# Rollout Status Check: Ensures that the deployment completes successfully.

kubectl rollout status deployment/hello-world-deployment -n application-ns --timeout=120s

# Readiness and Liveness Probes: Validates the application is reachable:

Root Path: http://<ingress-endpoint>/
Health Path: http://<ingress-endpoint>/health

# Rollback on Failure: If a rollout fails, the workflow initiates a rollback:

kubectl rollout undo deployment/hello-world-deployment -n application-ns

## License
develop by Hildebrando Nunez