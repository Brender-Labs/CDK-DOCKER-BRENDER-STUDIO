import { ManagedPolicy, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";


export function createBatchPolicy(scope: Construct) {

    const batchPolicy = new ManagedPolicy(scope, 'BatchPolicy', {
        statements: [
            new PolicyStatement({
                actions: [
                    'batch:DescribeJobDefinitions',
                    'batch:DescribeJobQueues',
                    'batch:DescribeJobs',
                    'batch:SubmitJob',
                    'batch:TerminateJob',
                    'ses:SendTemplatedEmail',
                    'ses:SendEmail',
                    'ses:SendRawEmail',
                    'ses:SendBulkTemplatedEmail',
                    'sts:GetCallerIdentity',
                    'sts:AssumeRole',
                    'iam:PassRole',
                    'iam:GetRole',
                    'iam:ListRoles',
                    'iam:ListInstanceProfiles',
                    'iam:ListPolicies',
                    'iam:GetPolicy',
                ],
                resources: ['*'],
            }),
        ],
    });

    return batchPolicy
}