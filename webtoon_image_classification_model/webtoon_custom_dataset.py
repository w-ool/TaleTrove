import os
import cv2
import glob
from torch.utils.data import Dataset
from PIL import Image

class CustomDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        # data_dir = "./data/sound_data/train"
        self.data_dir = glob.glob(os.path.join(data_dir, '*', '*.png'))
        self.transform = transform
        self.label_dict = {'BARKHAN':0, 'lookism':1, 'naturalbornidiots':2, 'thesoundofyourheart':3, 'beautifulauxiliarypolice':4, 'hellper':5,
                           'nanolist':6, 'noblesse':7, 'viralhit':8, 'GARBAGETIME':9}

    def __len__(self):
        return len(self.data_dir)

    def __getitem__(self, item):
        img_path = self.data_dir[item]
        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES =True
        img = Image.open(img_path)
        img = img.convert('RGB')
        label_name =img_path.split('\\')[1]
        label = self.label_dict[label_name]


        if self.transform is not None:
            img = self.transform(img)

        return img, label#, img_path

# test = CustomDataset('./data/img_data/train', transform=None)
# for a,b in test:
#     print(a,b)