from lavis.models import load_model_and_preprocess
import torch
from openai import OpenAI  
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)


def get_composed(cation, text, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a composed assistant, skilled in composing text and image content for better query in text-image retrieval."},
        {"role": "user", "content": f"Combine '{cation}' as image content (image content can be long, but we only need to focus on main subject) with '{text}' as modified text for main subject. Please, keep it short and good for text-image retrieval using clip by remove context, return text only as a query for retrieval."}
    ]
    )
    return completion.choices[0].message.content

def preprocess_image(raw_image):
    return vis_processors["eval"](raw_image).unsqueeze(0).to(device)
def get_caption(image):
    image = preprocess_image(image)
    caption = model.generate({"image": image})[0]
    return caption
def get_composed_caption(image, text, api_key):
    image = preprocess_image(image)
    caption = model.generate({"image": image, "text": text})[0]
    composed_text = get_composed(caption, text, api_key=api_key)
    return composed_text
