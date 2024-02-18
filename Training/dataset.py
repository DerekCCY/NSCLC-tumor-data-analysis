import torch
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
from transform_alb import *
import cv2
import os 
from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt

class FoxP3_Dataset(Dataset):
    def __init__(self, image_dir, label_dir,transform=None):
        
        self.images = sorted(os.listdir(str(image_dir)))
        self.labels = sorted(os.listdir(str(label_dir)))
        assert len(self.images) == len(self.labels)
        self.transform =transform 
        
        self.images_and_label = []
        for i in range(len(self.images)):
            self.images_and_label.append((str(image_dir)+'/'+str(self.images[i]),str(label_dir)+'/'+str(self.labels[i])))

    def __getitem__(self, index):
        
        image_path, label_path = self.images_and_label[index]
        
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        #image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
        cv2.imwrite("image.png", image)
        
        label = cv2.imread(label_path, cv2.IMREAD_COLOR)
        cv2.imwrite("label.png", label)
        
        if self.transform is not None:
            transformed_image = self.transform(image=image, mask=label)
            image = transformed_image['image']
            label = transformed_image['mask']
        return image, label
    
    def __len__(self):
        return len(self.images)
    