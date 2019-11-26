from aws_cdk import (
    aws_ec2,
    core
)
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


class Network(core.Stack):

    def __init__(self, scope: core.Stack, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            self, "Vpc",
            cidr=config['DEFAULT']['cidr'],
        )

