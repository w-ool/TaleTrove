import torch
from torch.utils.data import DataLoader
from torchvision.models.efficientnet import efficientnet_b0
from torchvision.models.resnet import resnet18
from torchvision.models.mobilenetv2 import mobilenet_v2
from torchvision.models.efficientnet import efficientnet_v2_s
from torchvision.transforms import transforms
import torch.optim as optim
import torch.nn as nn
import matplotlib.pyplot as plt
from webtoon_custom_dataset import CustomDataset
from tqdm import tqdm
import pandas as pd
import argparse

class Webtoon_Classifier:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.train_losses = []
        self.train_accs = []
        self.val_losses = []
        self.val_accs = []

    def train(self, train_loader, val_loader, epochs, optimizer, criterion, start_epoch=0):
        best_val_acc = 0
        print('Train.............')

        for epoch in range(start_epoch, epochs):
            train_loss = 0.0
            train_acc = 0.0
            val_loss = 0.0
            val_acc = 0.0

            self.model.train()
            train_loader_iter = tqdm(train_loader, desc=(f'Epoch: {epoch + 1}/{epochs}'), leave=False)

            for i, (img, label) in enumerate(train_loader_iter):
                img, label = img.float().to(self.device), label.to(self.device)
                optimizer.zero_grad()
                output = self.model(img)
                loss = criterion(output, label)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()

                _, pred = torch.max(output, 1)
                train_acc += (pred == label).sum().item()

                train_loader_iter.set_postfix({'Loss': loss.item()})

            train_loss /= len(train_loader)
            train_acc /= len(train_loader.dataset)

            #eval
            self.model.eval()
            with torch.no_grad():
                for img, label in val_loader:
                    img, label = img.float().to(self.device), label.to(self.device)
                    output = self.model(img)
                    _, pred = torch.max(output, 1)
                    val_acc += (pred == label).sum().item()
                    # pred = output.argmax(dim=1, keepdim=True)
                    # val_acc += pred.eq(label.view_as(pred)).sum().item()
                    val_loss += criterion(output, label).item()

                val_loss /= len(val_loader)
                val_acc /= len(val_loader.dataset)

                print(f'Epoch [{epoch + 1} / {epochs}], Train loss [{train_loss:.4f}], Train acc [{train_acc:.4f}],'
                      f'Val loss [{val_loss:.4f}], Val acc[{val_acc:.4f}]')

            self.train_losses.append(train_loss)
            self.train_accs.append(train_acc)
            self.val_losses.append(val_loss)
            self.val_accs.append(val_acc)

            if val_acc > best_val_acc:
                torch.save(self.model.state_dict(), './best_model/webtoon_best.pt')
                best_val_acc = val_acc

            torch.save({
                'epoch': epoch+1,
                'model_state_dict': self.model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_losses': self.train_losses,
                'train_accs': self.train_accs,
                'val_losses': self.val_losses,
                'val_accs': self.val_accs
            }, './checkpoints/webtoon_data_checkpoint.pt')

        self.save_result_to_csv()
        self.plot_loss()
        self.plot_accuracy()

    def save_result_to_csv(self):
        df = pd.DataFrame({
            'Train Loss': self.train_losses,
            'Train Acc': self.train_accs,
            'Validation Loss': self.val_losses,
            'Validation Acc': self.val_accs
        })
        df.to_csv('./loss_acc_result/webtoon_train_val_result.csv', index=False)

    def plot_loss(self):
        plt.figure()
        plt.plot(self.train_losses, label='Train loss')
        plt.plot(self.val_losses, label='Val loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig('./loss_acc_result/webtoon_loss_plot.png')

    def plot_accuracy(self):
        plt.figure()
        plt.plot(self.train_accs, label='Train loss')
        plt.plot(self.val_accs, label='Val loss')
        plt.xlabel('Epoch')
        plt.ylabel('Acc')
        plt.legend()
        plt.savefig('./loss_acc_result/webtoon_acc_plot.png')

    def run(self,args):
        # efficientnet_b0 모델
        self.model = efficientnet_b0(pretrained=True)
        self.model.classifier[1] = nn.Linear(1280, out_features=10)

        # resnet18 모델
        # self.model = resnet18(pretrained=True)
        # num_features = self.model.fc.in_features
        # self.model.fc = nn.Linear(num_features, 10)

        # mobilenet 모델
        # self.model = mobilenet_v2(pretrained=True)
        # in_features = 1280
        # self.model.classifier[1] = nn.Linear(in_features, 10)

        # efficientnet_v2_s 모델
        # self.model = efficientnet_v2_s(pretrained=True)
        # in_features = 1280
        # self.model.classifier[1] = nn.Linear(in_features, 10)

        self.model.to(self.device)

        train_transform = transforms.Compose([
            transforms.Resize((255, 255)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.ToTensor()
        ])
        val_transform = transforms.Compose([
            transforms.Resize((255, 255)),
            transforms.ToTensor()
        ])

        train_dataset = CustomDataset('./data/img_data/train', transform=train_transform)
        val_dataset = CustomDataset('./data/img_data/test', transform=val_transform)
        train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=args.batch_size)

        epochs = args.epochs    
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(self.model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
        start_epoch = 0

        if args.resume_training:
            checkpoint=torch.load(args.checkpoint_dir)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.train_losses = checkpoint['train_losses']
            self.train_accs = checkpoint['train_accs']
            self.val_losses = checkpoint['val_losses']
            self.val_accs = checkpoint['val_accs']
            start_epoch = checkpoint['epoch']

        self.train(train_loader, val_loader, epochs, optimizer, criterion, start_epoch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', type=str, default='./data/img_data/train',
                        help='directory path to training data')
    parser.add_argument('--val_dir', type=str, default='./data/img_data/test',
                        help='directory path to validation data')
    parser.add_argument('--epochs', type=int, default=20, help='num of epochs for training')
    parser.add_argument('--batch_size', type=int, default=100, help='batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='learning rate for optimizer')
    parser.add_argument('--weight_decay', type=float, default=1e-2, help='weight decay for optimizer')
    parser.add_argument('--resume_training', action='store_true', help='resume training from the last checkpoint')
    parser.add_argument('--checkpoint_dir', type=str, default='./checkpoints/webtoon_data_checkpoint.pt',
                        help='path to the checkpoint file')

    args = parser.parse_args()

    classifier = Webtoon_Classifier()
    classifier.run(args)

    # resume = python webtoon
    # _data_train.py --resume