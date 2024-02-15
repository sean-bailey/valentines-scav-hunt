from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as aws_lambda,
    aws_logs as logs,
    CfnOutput,

)
from aws_cdk.aws_lambda import Architecture

class ValentinesDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
#--------------------------------------valentines_function Lambda Function---------------------------------------------
        valentines_function_lambda_function_name="valentines_function_lambda_function"

        valentines_function_lambda_role=iam.Role(
            self,
            id="valentines_function_lambda_role",
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com")
        )

        valentines_function_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        valentines_function_lambda_function=aws_lambda.DockerImageFunction(self,valentines_function_lambda_function_name,
        
        timeout=Duration.seconds(900),
        log_retention=logs.RetentionDays.ONE_WEEK,
        environment={

        "STAGE":"",
        },
        memory_size=10240,
        retry_attempts=0,
        role=valentines_function_lambda_role,
        code=aws_lambda.DockerImageCode.from_image_asset("./valentines_docker"),
        architecture=Architecture.ARM_64,
        )

        valentines_function_lambda_function_url=valentines_function_lambda_function.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE,
            cors=aws_lambda.FunctionUrlCorsOptions(
         #Allow this to be called from websites on https://example.com.
         #Can also be ['*'] to allow all domain.
        allowed_origins=["*"]
        )
        #we need to allow all interactions with this url
        )
        CfnOutput(self, "OpenLlamaUrl",
        value=valentines_function_lambda_function_url.url + "docs"
        )