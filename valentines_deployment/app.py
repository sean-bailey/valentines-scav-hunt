#!/usr/bin/env python3

import aws_cdk as cdk

from valentines_deployment.valentines_deployment_stack import ValentinesDeploymentStack


app = cdk.App()
ValentinesDeploymentStack(app, "ValentinesDeploymentStack")

app.synth()
