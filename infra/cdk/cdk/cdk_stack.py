"""AWS CDK module to create ECS infrastructure"""
from aws_cdk import (core, aws_ecs as ecs, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam,aws_ecs_patterns as ecs_patterns)

class EcsDevopsSandboxCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the ECR Repository
        ecr_repository = ecr.Repository(self,
                                        "image-repo",
                                        repository_name="image-repo", image_scan_on_push=False)

        # Create the ECS Cluster (and VPC)
        vpc = ec2.Vpc(self,
                      "ecs-vpc",
                      max_azs=2, cidr="10.2.0.0/16")
        vpc_test = ec2.Vpc(self,
                      "ecs-vpc-test",
                      max_azs=2, cidr="10.1.0.0/16")
        cluster = ecs.Cluster(self,
                              "ecs-cluster",
                              cluster_name="ecs-devops-sandbox-cluster",
                              vpc=vpc)
        cluster_test = ecs.Cluster(self,
                              "ecs-cluster-test",
                              cluster_name="ecs-devops-sandbox-test-cluster",
                              vpc=vpc_test)
         # Create the ECS Task Definition with placeholder container (and named Task Execution IAM Role)
        execution_role = iam.Role(self,
                                  "ecs-devops-sandbox-execution-role",
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                  role_name="ecs-devops-sandbox-execution-role")
                                  
        execution_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
                ]
        ))
        task_definition = ecs.FargateTaskDefinition(self,
                                                    "ecs-devops-sandbox-task-definition",
                                                    execution_role=execution_role,
                                                    family="ecs-devops-sandbox-task-definition")
        container = task_definition.add_container(
            "ecs-devops-sandbox",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )

        service = ecs.FargateService(self,
                                     "ecs-service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     service_name="ecs-service")
        service = ecs.FargateService(self,
                                     "ecs-service-test",
                                     cluster=cluster_test,
                                     task_definition=task_definition,
                                     service_name="ecs-service-test")


