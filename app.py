# --------------------------------------------------------------------------------------- #
# Importing Required Libraries
# --------------------------------------------------------------------------------------- #
import os
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image


# --------------------------------------------------------------------------------------- #
# Configuring API Key by loading environment variables
# --------------------------------------------------------------------------------------- #
load_dotenv()  # Loading all Environment Variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# NOTE: Change the API key in '.env' file and put your API key there. You can get your api key from ai.google.dev


# --------------------------------------------------------------------------------------- #
# Defining Functions
# --------------------------------------------------------------------------------------- #
def generate_response(prompt, image):
    """
    Generate Response from Gemini's pro-vision model by
    providing it with an image and appropriate prompt.
    """
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([prompt, image[0]])
    return response.text


def image_setup(uploaded_file):
    """
    Takes the input image and generates a list contining
    the image's MIME type and the image in byte format.
    """
    if uploaded_file is not None:  # Checking if the file has been uplaoded
        bytes_data = uploaded_file.getvalue()  # Reading the file into bytes

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Getting the MIMME type of the uploaded file
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# --------------------------------------------------------------------------------------- #
# Driver Code
# --------------------------------------------------------------------------------------- #
st.set_page_config(page_title="CARL - AI Nutritionist")

st.header("CARL - AI Nutritionist")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the Nutrients in this food")

# You can modify the prompt according to your requirements to retrieve specific information.

prompt = """
You are an expert nutritionist whose job is to see the food items from the image to calculate the total calories and provide the details of every food items with calories intake in the format below

1. Item 1 - no of calories
2. Item 2 - no of calories
---
---

Finally, you have to mention whether the food is healthy or not and mention the percentage split of the ratio of carbohydrates, fats, fibers, sugar and other important things required in our diet.
As an expert in the field of nutrition, provide further suggestions.    
"""

if submit:
    image_data = image_setup(uploaded_file)
    response = generate_response(prompt=prompt, image=image_data)

    headings = [
        "Carl says, ",
        "According to Carl, ",
        "Carl thinks that,",
        "Carl's expertise suggests, ",
        "Carl states, ",
        "In Carl's view, ",
        "In Carl's opinion, ",
        "Drawing on his expertise, Carl highlights, ",
        "According to Carl's nutritional expertise",
        "As a nutritionist, Carl points out, ",
        "Your nutritionist Carl thinks that, ",
        "Carl, your personal expert thinks that, ",
        "According to Carl, your personal nutritionist, ",]

    st.header(random.choice(headings))
    st.write(response)
