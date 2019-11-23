from aws_cdk import (
    aws_ecs,
    aws_ec2,
    aws_efs,
    core
)

from os import getenv


class ECSCluster(core.Stack):

    def __init__(self, scope: core.Stack, id: str, vpc, service_discovery_namespace, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.vpc = vpc
        self.service_discovery_namespace = service_discovery_namespace

        # Create VPC for cluster - best practice is to isolate jenkins to its own vpc
        self.cluster = aws_ecs.Cluster(
            self, "ECSCluster",
            vpc=self.vpc,
            default_cloud_map_namespace=aws_ecs.CloudMapNamespaceOptions(name=service_discovery_namespace)
        )

        if getenv('EC2_ENABLED'):
            self.asg = self.cluster.add_capacity(
                "Ec2",
                instance_type=aws_ec2.InstanceType("t3.xlarge"),
                key_name="jenkinsonaws",
            )

            self.efs_sec_grp = aws_ec2.SecurityGroup(
                 self, "EFSSecGrp",
                 vpc=self.vpc,
                 allow_all_outbound=True,
            )

            self.efs_sec_grp.add_ingress_rule(
                peer=self.cluster.connections.security_groups[0],
                connection=aws_ec2.Port(protocol=aws_ec2.Protocol.ALL,string_representation="ALL",from_port=2049,to_port=2049),
                description="EFS"
            )

            self.efs_filesystem = aws_efs.CfnFileSystem(
                self, "EFSBackend",
            )

            counter = 0
            for subnet in self.vpc.private_subnets:
                aws_efs.CfnMountTarget(
                    self, "EFS{}".format(counter),
                    file_system_id=self.efs_filesystem.ref,
                    subnet_id=subnet.subnet_id,
                    security_groups=[
                        self.efs_sec_grp.security_group_id
                    ]
                )
                counter += 1

            self.user_data = """
                sudo yum install -y amazon-efs-utils 
                sudo mkdir /mnt/efs
                sudo chown -R ec2-user: /mnt/efs
                sudo chmod -R 0777 /mnt/efs
                sudo mount -t efs -o tls /mnt/efs {}:/ efs
                """.format(self.efs_filesystem.ref)

            self.asg.add_user_data(self.user_data)

