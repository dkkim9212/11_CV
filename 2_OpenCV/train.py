import torch
from torchvision import datasets, transforms
from torchvision.models import resnet18, ResNet18_Weights

model = resnet18(
    weights=ResNet18_Weights.DEFAULT
)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

dataset_path = "dataset"

dataset = datasets.ImageFolder(
    dataset_path,
    transform=transform
)

print("클래스 이름 :", dataset.classes)
print("클래스 번호 :", dataset.class_to_idx)
print("전체 이미지 :", len(dataset))