import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
import cv2

train_transform = A.Compose([
    A.Resize(width=1024, height=1024),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.Rotate(limit=30, p=0.5),
    #A.RandomBrightnessContrast(p=0.2),
    ToTensorV2(),
])

val_transform = A.Compose([
    A.Resize(width=1024, height=1024),
    ToTensorV2(),
])