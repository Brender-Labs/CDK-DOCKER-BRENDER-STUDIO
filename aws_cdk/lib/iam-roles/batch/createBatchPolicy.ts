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
                ],
                resources: ['*'],
            }),
        ],
    });

    return batchPolicy
}