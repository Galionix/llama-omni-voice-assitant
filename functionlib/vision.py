from PIL import Image
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get('GENAI_API_KEY'))

generation_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048


}

safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
     },
    #   {
    #       'category': 'HARM_CATEGORY_NUDITY',
    #       'threshold': 'BLOCK_NONE'
    #   },
    #   {
    #       'category': 'HARM_CATEGORY_RACISM',
    #       'threshold': 'BLOCK_NONE'
    #   },
    #   {
    #        'category': 'HARM_CATEGORY_SEXUAL_CONTENT',
    #        'threshold': 'BLOCK_NONE'
       

    #   },
      {
            'category':  'HARM_CATEGORY_SEXUALLY_EXPLICIT',
             'threshold':  'BLOCK_NONE'
       },{
            'category':  'HARM_CATEGORY_HATE_SPEECH',
             'threshold':  'BLOCK_NONE'
       },
    #    {
    #        'category':   'HARM_CATEGORY_VIOLENCE',
    #        'threshold':  'BLOCK_NONE'

    #   },
       {
           'category':   'HARM_CATEGORY_DANGEROUS_CONTENT',
           'threshold':  'BLOCK_NONE'

      }
]

model = genai.GenerativeModel('gemini-1.5-flash-latest',
                              generation_config=generation_config,
                              safety_settings=safety_settings
                              )

def vision_prompt(prompt, photo_path):
          
    img = Image.open(photo_path)

    prompt = (
        "You are the vision analysis AI that provides semantic meaning from images to provide context "
        "to send to another AI that will create a response to the user. Do not respond as the AI assistant "
        "to the user. Instead, take the user prompt input and try to extract all meaning from the photo "
        "relevant to the user prompt. Then generate as much objective data about the image for the AI "
        f"assistant who will respond to the user. \nUSER PROMPT: {prompt}"
    )

    response = model.generate_content([prompt, img])
    return response.text
