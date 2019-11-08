from aws_cdk import (
    aws_ec2,
    core
)


class Network(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            self, "Vpc",
            cidr='10.0.0.0/24',
        )
