import * as cdk from 'aws-cdk-lib';
import { AllocationStrategy, EcsEc2ContainerDefinition, EcsJobDefinition, EcsVolume, JobQueue, ManagedEc2EcsComputeEnvironment } from "aws-cdk-lib/aws-batch";
import { ISecurityGroup, IVpc, InstanceType, SubnetType } from "aws-cdk-lib/aws-ec2";
import { Repository } from "aws-cdk-lib/aws-ecr";
import { ContainerImage } from "aws-cdk-lib/aws-ecs";
import { IFileSystem } from 'aws-cdk-lib/aws-efs';
import { ManagedPolicy, Role, ServicePrincipal } from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";
import { createS3Policy } from '../iam-roles/s3/createS3Policy';
import { v4 as uuidv4 } from 'uuid';
import { createBatchPolicy } from '../iam-roles/batch/createBatchPolicy';



interface BatchResourcesProps {
    vpc: IVpc,
    sg: ISecurityGroup,
    efs: IFileSystem;
    ecrRepositoryName: string,
    s3BucketName: string,
    blenderVersionsList: string,
    isPrivate: boolean,
    maxvCpus: {
        onDemandCPU: number;
        spotCPU: number;
        onDemandGPU: number;
        spotGPU: number;
    }
}

export function createBatchResources(scope: Construct, props: BatchResourcesProps) {
    const { vpc, sg, ecrRepositoryName, efs, s3BucketName, blenderVersionsList, isPrivate, maxvCpus } = props;


    console.log('maxvCpus inside createBatchResources:', maxvCpus);
    
    console.log('Type of maxvCpus: ', typeof maxvCpus);
    console.log('Max vCPUs: ', maxvCpus.onDemandCPU, maxvCpus.spotCPU, maxvCpus.onDemandGPU, maxvCpus.spotGPU)


    const ecrRepository = Repository.fromRepositoryName(scope, 'ECRRepository', ecrRepositoryName);
    ecrRepository.grantPull(new ServicePrincipal('batch.amazonaws.com'))


    const s3Policy = createS3Policy(scope, { s3BucketName })
    const batchPolicy = createBatchPolicy(scope);

    // obtener todas las subnets de la vpc
    const allSubnets = vpc.selectSubnets({
        subnetType: isPrivate ? SubnetType.PRIVATE_WITH_EGRESS : SubnetType.PUBLIC
    }).subnets;

    allSubnets.forEach(subnet => {
        console.log(`Subnet ${subnet.subnetId} en la zona de disponibilidad ${subnet.availabilityZone}`);
    });

    // =================COMPUTE ENVIRONMENTS CPU=================

    const computeEnvOnDemandCPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvOnDemandCPU-' + uuidv4(), {
        useOptimalInstanceClasses: true,

        instanceRole: new Role(scope, 'ComputeEnvironmentRoleOnDemandCPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
                s3Policy,
                batchPolicy,
            ],
        }),
        vpc,
        // all az subnets 
        vpcSubnets: {
            // subnetType: isPrivate ? SubnetType.PRIVATE_WITH_EGRESS : SubnetType.PUBLIC,
            subnets: allSubnets,
        },
        computeEnvironmentName: 'ComputeEnvOnDemandCPU-' + uuidv4(),
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: maxvCpus.onDemandCPU,
        enabled: true,
        instanceTypes: [new InstanceType('c5')]
    })



    const computeEnvSpotCPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvSpotCPU-' + uuidv4(), {
        // useOptimalInstanceClasses: true,
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleSpotCPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
                s3Policy,
                batchPolicy,
            ],
        }),
        vpc,
        vpcSubnets: {
            subnets: allSubnets,
        },
        instanceTypes: [
            new InstanceType('optimal')
            // ADD MORE INSTANCES TYPES (CPU)
        ],
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: maxvCpus.spotCPU,
        enabled: true,
        computeEnvironmentName: 'ComputeEnvSpotCPU-' + uuidv4(),
        spot: true,
        spotBidPercentage: 100,
        allocationStrategy: AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
    });


    // =================COMPUTE ENVIRONMENTS GPU=================

    const computeEnvOnDemandGPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvOnDemandGPU-' + uuidv4(), {
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleOnDemandGPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
                s3Policy,
                batchPolicy,
            ],
        }),
        vpc,
        vpcSubnets: {
            subnets: allSubnets,
        },
        instanceTypes: [
            new InstanceType('g5')
            // ADD MORE INSTANCES TYPES (GPU)
        ],
        computeEnvironmentName: 'ComputeEnvOnDemandGPU-' + uuidv4(),
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: maxvCpus.onDemandGPU,
        enabled: true,
    })

    const computeEnvSpotGPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvSpotGPU-' + uuidv4(), {
        // useOptimalInstanceClasses: true,
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleSpotGPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'),
                s3Policy,
                batchPolicy,
            ],
        }),
        vpc,
        vpcSubnets: {
            subnets: allSubnets,
        },
        instanceTypes: [
            new InstanceType('g5')
        ],
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: maxvCpus.spotGPU,
        enabled: true,
        computeEnvironmentName: 'ComputeEnvSpotGPU-' + uuidv4(),
        spot: true,
        spotBidPercentage: 100,
        allocationStrategy: AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
    });


    // =================JOB QUEUES CPU=================
    const jobQueueSpotCPU = new JobQueue(scope, 'JobQueueSpotCPU-' + uuidv4(), {
        computeEnvironments: [{
            computeEnvironment: computeEnvSpotCPU,
            order: 1,
        }],
        jobQueueName: 'JobQueueSpotCPU-' + uuidv4(),
        priority: 10,
    });

    const jobQueueOnDemandCPU = new JobQueue(scope, 'JobQueueOnDemandCPU-' + uuidv4(), {
        computeEnvironments: [{
            computeEnvironment: computeEnvOnDemandCPU,
            order: 1,
        }],
        priority: 10,
        jobQueueName: 'JobQueueOnDemandCPU-' + uuidv4(),
    });


    // =================JOB QUEUES GPU=================
    const jobQueueSpotGPU = new JobQueue(scope, 'JobQueueSpotGPU-' + uuidv4(), {
        computeEnvironments: [{
            computeEnvironment: computeEnvSpotGPU,
            order: 1,
        }],
        jobQueueName: 'JobQueueSpotGPU-' + uuidv4(),
        priority: 10,
    });

    const jobQueueOnDemandGPU = new JobQueue(scope, 'JobQueueOnDemandGPU-' + uuidv4(), {
        computeEnvironments: [{
            computeEnvironment: computeEnvOnDemandGPU,
            order: 1,
        }],
        jobQueueName: 'JobQueueOnDemandGPU-' + uuidv4(),
        priority: 10,
    });

    // Context param ex: "4.0.0,4.0.0,3.6.0" : new version

    let blenderList = blenderVersionsList.split(',').map(version => version.toLowerCase());
    console.log('blenderList: ', blenderList);

    blenderList.map((version, index) => {
        let versionBlender = version.replace(/\./g, '_');
        let jobDefinitionName = `JobDefinition_VERSION__${versionBlender}__${uuidv4()}`;
        let containerDefinitionName = `ContainerDefinition_VERSION__${versionBlender}__${uuidv4()}`;
        console.log('jobDefinitionName: ', jobDefinitionName);

        new EcsJobDefinition(scope, jobDefinitionName, {
            timeout: cdk.Duration.minutes(60),
            retryAttempts: 3,
            jobDefinitionName: jobDefinitionName,
            container: new EcsEc2ContainerDefinition(scope, containerDefinitionName, {
                image: ContainerImage.fromEcrRepository(ecrRepository, version),
                // Add max memory for the container
                memory: cdk.Size.gibibytes(192),
                cpu: 256, // review this value 
                volumes: [EcsVolume.efs({
                    name: 'efs-volume',
                    fileSystem: efs,
                    containerPath: '/mnt/efs',
                    rootDirectory: '/',
                    enableTransitEncryption: true,
                })],
            }),
        });
    });

}