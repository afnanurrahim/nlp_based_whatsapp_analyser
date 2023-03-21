import openai
import random

api= "sk-"
openai.api_key=api

def about_summary(msg_list):

    msg_50=''
    for i in range(50):
        random_number = random.randint(0, len(msg_list)-1)
        msg_50+= msg_list[random_number]+" "

    prompt = (f"Please give me context as to what this whatsapp group is about:\n\n"
            f"Text: {msg_50}"
            f"Summary:")

    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
        max_tokens=400,
        temperature=0.5,
    stop=None,
        
    )
    summary = response.choices[0].text.strip()
    return summary
