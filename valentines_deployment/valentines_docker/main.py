from fastapi import FastAPI
from mangum import Mangum
from llama_cpp import Llama
import os
import re


app = FastAPI()
MODEL = os.environ.get("MODELPATH")

print("Model loaded")
locationdict = {
    1:"Garden Shed",
    2:"Chicken Coop",
    3:"Chevy Truck Engine Bay",
    4:"Dining Room for Dinner"
}

def censor_text(input_text, censorship_list, replacement="this place"):
    """
    Replace each occurrence of words in the censorship_list with the replacement text, case-insensitively.
    
    :param input_text: The original text to process.
    :param censorship_list: A list of words to replace in the text, case-insensitively.
    :param replacement: The text to replace the censored words with. Defaults to "***".
    :return: The processed text with censored words replaced, preserving the original case.
    """
    def replace_func(match):
        return replacement
    
    for word in censorship_list:
        # Use re.sub() with a function as the replacement to preserve case
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        input_text = pattern.sub(replace_func, input_text)
    return input_text

@app.get("/valentines_clue")
async def process_number(number: int):
    print("loading model...")
    llm = Llama(
        model_path=MODEL,
        chat_format="chatml"
        # n_gpu_layers=-1, # Uncomment to use GPU acceleration
        # seed=1337, # Uncomment to set a specific seed
        # n_ctx=2048, # Uncomment to increase the context window
    )
    print("now processing number "+str(number))
    # You can replace the logic here with whatever you need
    nextlocation=locationdict[number]

    output = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant specifically designed to write Valentines Clues for a Scavenger Hunt. You follow instructions exactly, and you do not reveal the true location, only clues.",
        },
        {"role": "user", "content": "Generate a Valentines Day themed clue for a scavenger hunt item found at the following location: '"+nextlocation+"'. Keep your clue as clear and straightforward as possible."},
    ],
    #response_format={
    #    "type": "json_object",
    #},
    temperature=0.7,
    max_tokens=100,
    )

    #output = llm(
    #  "Generate a Valentines Day themed clue for a scavenger hunt for the following location: "+nextlocation+". Use rhymes and proper themes, but do not mention the exact words '"+nextlocation+"' in your clue.",
    #  max_tokens=100,
    #  #stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
    #  #echo=True # Echo the prompt back in the output
    #)
    outputtext = output['choices'][0]['message']['content']
    outputtext = censor_text(outputtext,list(locationdict.values()))
    return{"clue": outputtext}

# Wrap the FastAPI app with Mangum
handler = Mangum(app)
