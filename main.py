import clip
import torch
import numpy as np
from PIL import Image as ImagePIL
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import faiss
from faiss import read_index
import os
from datasets import Dataset, Image, load_dataset
from utils.representation import image_to_tensor, image_to_features, text_to_tensor, text_to_features, feature_retrieval, index_to_images, index_to_image_path
from utils.composed import get_composed_caption, get_caption, get_composed# Load the openAI model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
index = read_index("model\image_net_val_index.index")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origins you want to allow, or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/search/image")
async def retrieval_by_image(
    k: int = Form(10),
    probe: int = Form(3),
    image: UploadFile = File(...)
):
    index.nprobe = probe
    image = ImagePIL.open(image.file)
    image = image_to_tensor(image, preprocess, device)
    image_features = image_to_features(image, model)
    retrieval_list = feature_retrieval(image_features, index, k)
    path_image = index_to_image_path(retrieval_list)
    return path_image

@app.post("/search/text")
async def retrieval_by_text(
    k: int = Form(10),
    probe: int = Form(3),
    query: str = Form(...)
):
    index.nprobe = probe
    query = text_to_tensor(query, device)
    query_features = text_to_features(query, model)
    retrieval_list = feature_retrieval(query_features, index, k)
    path_image = index_to_image_path(retrieval_list)
    return path_image

@app.post("/search/composed")
async def retrieval_by_composed(
    k: int = Form(10),
    probe: int = Form(3),
    query: str = Form(...),
    api_key: str = Form(...),
    image: UploadFile = File(...)
):
    index.nprobe = probe
    image = ImagePIL.open(image.file)
    text_caption = get_composed_caption(image, query, api_key)
    query = text_to_tensor(text_caption, device)
    query_features = text_to_features(query, model)
    retrieval_list = feature_retrieval(query_features, index, k)
    path_image = index_to_image_path(retrieval_list)
    return path_image