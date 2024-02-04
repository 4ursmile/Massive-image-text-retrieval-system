import torch
import numpy as np
from PIL import Image
import faiss
import clip
def normalize_L2(feature: np.array):
    return feature/np.linalg.norm(feature)
def image_to_tensor(image: Image.Image, preprocess, device):
    image = preprocess(image).unsqueeze(0).to(device)
    return image

def image_to_features(image: torch.Tensor, model):
    image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    image_features = image_features.detach().cpu().numpy()
    return image_features
    
def text_to_tensor(text: str, device):
    text = clip.tokenize(text).to(device)
    return text
def text_to_features(text: torch.Tensor, model):
    text_features = model.encode_text(text)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    text_features = text_features.detach().cpu().numpy()
    return text_features

def feature_retrieval(features: np.array, index, number_of_results):
    D, I = index.search(features, number_of_results)
    return I

def index_to_image_path(indexes):
    base_path = "data/images"
    base_name = "ILSVRC2012_val_"
    indexes = np.squeeze(indexes)
    image_paths = [f"{base_path}/{base_name}{index+1:08d}.JPEG" for index in indexes]
    return image_paths
def path_to_images(image_paths):
    images = [Image.open(image_path) for image_path in image_paths]
    return images
def index_to_images(indexes):
    image_paths = index_to_image_path(indexes)
    images = path_to_images(image_paths)
    return images
