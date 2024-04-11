#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { BrenderStudioStack } from '../lib/cdk-brender-studio-stack';

const app = new cdk.App();
const stackName = app.node.tryGetContext('stackName');
const blenderVersionsList = app.node.tryGetContext('blenderVersions');
const isPrivate = app.node.tryGetContext('isPrivate') === 'true' ? true : false;

// Test the context values
// const account = app.node.tryGetContext('account');
// const region = app.node.tryGetContext('region');

const brenderStack = new BrenderStudioStack(app, 'BRENDER-STACK-V1', {
  stackName,
  blenderVersionsList,
  isPrivate,
  description: 'BRENDER-STUDIO-STACK: This stack deploys all the essential resources to enable rendering Blender scenes in the cloud using AWS. It includes configurations for services such as AWS Batch, Amazon ECS, Amazon ECR, and Amazon EFS, providing a robust and scalable infrastructure for efficiently and reliably executing rendering jobs.',
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT, 
    region: process.env.CDK_DEFAULT_REGION,
  }
});

cdk.Tags.of(brenderStack).add('StackName', stackName);