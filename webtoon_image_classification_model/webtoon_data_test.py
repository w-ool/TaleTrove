import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional
from torch.utils.data import DataLoader
from torchvision.models import resnet18
from webtoon_custom_dataset import CustomDataset
import cv2

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = resnet18()
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 4)

    # pt load
    model.load_state_dict(torch.load(f='./best_model/webtoon_best.pt'))

    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    test_dataset = CustomDataset('./data/img_data/test', test_transform)
    test_loader = DataLoader(test_dataset, batch_size=1)

    model.to(device)
    model.eval()

    correct = 0
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    count_7 = 0
    count_8 = 0
    count_9 = 0
    correct_0 = 0
    correct_1 = 0
    correct_2 = 0
    correct_3 = 0
    correct_4 = 0
    correct_5 = 0
    correct_6 = 0
    correct_7 = 0
    correct_8 = 0
    correct_9 = 0

    label_dict = {0: 'BARKHAN', 1: 'lookism', 2: 'naturalbornidiots', 3:'thesoundofyourheart', 4:'beautifulauxiliarypolice', 5:'hellper',
                           6:'nanolist', 7:'noblesse', 8:'viralhit', 9:'GARBAGETIME'}
    with torch.no_grad():
        for img, label, path in test_loader:
            label_ = label.item()
            img, label = img.to(device), label.to(device)
            output = model(img)
            _, pred = torch.max(output, 1)
            correct += (pred == label).sum().item()

            # 라벨별 정확도를 위한 카운팅
            if label == 0:
                count_0 += 1
                correct_0 += (pred == label).sum().item()

            if label == 1:
                count_1 += 1
                correct_1 += (pred == label).sum().item()

            if label == 2:
                count_2 += 1
                correct_2 += (pred == label).sum().item()

            if label == 3:
                count_3 += 1
                correct_3 += (pred == label).sum().item()

            if label == 4:
                count_4 += 1
                correct_4 += (pred == label).sum().item()

            if label == 5:
                count_5 += 1
                correct_5 += (pred == label).sum().item()

            if label == 6:
                count_6 += 1
                correct_7 += (pred == label).sum().item()

            if label == 7:
                count_7 += 1
                correct_7 += (pred == label).sum().item()

            if label == 8:
                count_8 += 1
                correct_8 += (pred == label).sum().item()

            if label == 9:
                count_9 += 1
                correct_9 += (pred == label).sum().item()


            # 모델의 사진별 예측값
            image = cv2.imread(path[0])
            image = cv2.resize(image, (500,500))
            # 예측값 이미지 안에 입력
            target_label = label_dict[label_]
            true_label_text = f'True: {target_label}'
            pred_label = label_dict[pred.item()]
            pred_text = f'pred: {pred_label}'
            image = cv2. rectangle(image, (0,0), (500, 80), (255,255,255), -1)
            image = cv2.putText(image, pred_text, (0, 30), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
            image = cv2.putText(image, true_label_text, (0, 60), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
            # cv2.imshow('test',image)
            # if cv2.waitKey() == ord('q'):
            #     exit()
            # print(image)
            # print(pred.item(), path)

    print('Test set: Acc {}/{} [{:.0f}]%\n'.format(correct, len(test_loader.dataset), 100*correct/len(test_loader.dataset)))
    print('label_0: Acc {}/{} [{:.0f}]%\n'.format(correct_0, count_0, 100*correct_0/count_0))
    print('label_1: Acc {}/{} [{:.0f}]%\n'.format(correct_1, count_1, 100 * correct_1 / count_1))
    print('label_2: Acc {}/{} [{:.0f}]%\n'.format(correct_2, count_2, 100 * correct_2 / count_2))
    print('label_3: Acc {}/{} [{:.0f}]%\n'.format(correct_3, count_3, 100 * correct_3 / count_3))
    print('label_4: Acc {}/{} [{:.0f}]%\n'.format(correct_4, count_4, 100 * correct_4 / count_4))
    print('label_5: Acc {}/{} [{:.0f}]%\n'.format(correct_5, count_5, 100 * correct_5 / count_5))
    print('label_6: Acc {}/{} [{:.0f}]%\n'.format(correct_6, count_6, 100 * correct_6 / count_6))
    print('label_7: Acc {}/{} [{:.0f}]%\n'.format(correct_7, count_7, 100 * correct_7 / count_7))
    print('label_8: Acc {}/{} [{:.0f}]%\n'.format(correct_8, count_8, 100 * correct_8 / count_8))
    print('label_9: Acc {}/{} [{:.0f}]%\n'.format(correct_9, count_9, 100 * correct_9 / count_9))

if __name__ == '__main__':
    main()