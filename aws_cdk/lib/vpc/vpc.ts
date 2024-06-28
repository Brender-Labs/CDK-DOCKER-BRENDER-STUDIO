import { RemovalPolicy } from "aws-cdk-lib";
import { GatewayVpcEndpointAwsService, IVpc, SubnetType, Vpc } from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface VpcProps {
    name: string;
    gatewayEndpointName: string;
    isPrivate: boolean;
}

export function createVpc(scope: Construct, props: VpcProps): IVpc {

    const { isPrivate, gatewayEndpointName, name } = props;

    if (!isPrivate) {
        const vpc = new Vpc(scope, name, {
            natGateways: 0,
            maxAzs: 99,
            subnetConfiguration: [
                {
                    cidrMask: 24,
                    name: 'public-subnet-1',
                    subnetType: SubnetType.PUBLIC,
                },
                {
                    cidrMask: 24,
                    name: 'public-subnet-2',
                    subnetType: SubnetType.PUBLIC,
                },
                {
                    cidrMask: 24,
                    name: 'private-subnet-1',
                    subnetType: SubnetType.PRIVATE_WITH_EGRESS,
                },
                {
                    cidrMask: 24,
                    name: 'private-subnet-2',
                    subnetType: SubnetType.PRIVATE_WITH_EGRESS,
                }
            ],
        });

        const s3GatewayEndpoint = vpc.addGatewayEndpoint(gatewayEndpointName, {
            service: GatewayVpcEndpointAwsService.S3,
        });

        vpc.applyRemovalPolicy(RemovalPolicy.DESTROY);
        return vpc;
    } else {
        const vpc = new Vpc(scope, name, {
            natGateways: 1,
            maxAzs: 99,
            subnetConfiguration: [
                {
                    cidrMask: 24,
                    name: 'public-subnet-1',
                    subnetType: SubnetType.PUBLIC,
                },
                {
                    cidrMask: 24,
                    name: 'public-subnet-2',
                    subnetType: SubnetType.PUBLIC,
                },
                {
                    cidrMask: 24,
                    name: 'private-subnet-1',
                    subnetType: SubnetType.PRIVATE_WITH_EGRESS,
                },
                {
                    cidrMask: 24,
                    name: 'private-subnet-2',
                    subnetType: SubnetType.PRIVATE_WITH_EGRESS,
                }
            ],
        });

        const s3GatewayEndpoint = vpc.addGatewayEndpoint(gatewayEndpointName, {
            service: GatewayVpcEndpointAwsService.S3,
        });


        vpc.applyRemovalPolicy(RemovalPolicy.DESTROY);
        return vpc
        // const vpc = new Vpc(scope, name);
        // return vpc;
    }
}
