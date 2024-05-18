import * as cdk from 'aws-cdk-lib';


export interface BrenderStudioStackProps extends cdk.StackProps {
  blenderVersionsList: string;
  isPrivate: boolean;
  maxvCpus: {
    onDemandCPU: number;
    spotCPU: number;
    onDemandGPU: number;
    spotGPU: number;
  }
}
