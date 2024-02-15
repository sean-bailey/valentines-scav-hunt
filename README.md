# valentines-scav-hunt

My mother started a tradition on Valentine's day where we would go on a Scavenger hunt and then do a feast together as a family. 

I've decided to carry on this tradition using serverless technologies and AI. Using pure Lambda, you can deploy an AI clue generating agent for your scavengers to hunt clues at.

Ideally, you'd use a QR code generator for the endpoints, providing the QR codes to your searchers as clues, and running the hunt in a sequential order. The beauty of this system is that, should the clue not be sufficient and your players want another hint, they can simply hit the endpoint again and the AI will generate a new clue related to the target, while subroutines prevent it from leaking the exact place to where the clue points. Naturally to keep this lightweight and stress free on infrastructure, I'll run it on Lambda using StableLM-zephyr-3B in a GGUF quantized format, using `llama-cpp-python`.


## Prerequisites:

* An AWS Account with proper credentials
* Docker installed locally
* The AWS CDK installed
* Python3 and Pip

## Installation

Clone this repo, then open a terminal and `cd` into the `valentines-scav-hunt` directory (the root of this repo), then do the following:

```

cd valentines_deployment
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cdk deploy


```

Once done you'll get an output which looks something like this:


```

Outputs:
ValentinesDeploymentStack.OpenLlamaUrl = https://krwc5zps7ns4frqrjbd5k55eju0hsyqp.lambda-url.us-east-1.on.aws/docs

```

That's the docs page for your fastAPI endpoint to the Lambda function. It uses `llama-cpp-python` in "chat" mode and StableLM-zephyr-3B in a gguf quantized format for the clue generation, so note it could take 30-60 seconds to generate a clue. You can shorten this by using a lower quantized model and/or lowering the total tokens generated. Keep the Lambda function hot to defend against cold starts!


## Cleanup

```
cdk destroy

```

Then make sure you go into your ECR and manually delete any images which didn't get cleaned up.

Enjoy!