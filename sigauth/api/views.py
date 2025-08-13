from rest_framework.decorators import api_view,permission_classes
from rest_framework.serializers import Serializer, ImageField
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from rest_framework.permissions import IsAuthenticated
class SignatureImageSerializer(Serializer):
    image_1 = ImageField()
    image_2 = ImageField()
class SiameseResNet(nn.Module):
    def __init__(self):
        super(SiameseResNet, self).__init__()
        base_model = models.resnet18(weights=None)
        base_model.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        num_ftrs = base_model.fc.in_features
        base_model.fc = nn.Identity()
        self.base_model = base_model
        self.embedding = nn.Sequential(
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )
    def forward_once(self, x):
        x = self.base_model(x)
        x = self.embedding(x)
        return x
    def forward(self, img1, img2):
        out1 = self.forward_once(img1)
        out2 = self.forward_once(img2)
        return out1, out2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request):
    try:
        serializer = SignatureImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_1 = serializer.validated_data['image_1']
        image_2 = serializer.validated_data['image_2']
        parameter_file_path = "api/siamese_resnet_18.pth"
        model = SiameseResNet()
        model.load_state_dict(torch.load(parameter_file_path, map_location="cpu"))
        model.eval()
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        img1_tensor = transform(Image.open(image_1).convert("RGB")).unsqueeze(0)
        img2_tensor = transform(Image.open(image_2).convert("RGB")).unsqueeze(0)
        with torch.no_grad():
            out1, out2 = model(img1_tensor, img2_tensor)
            distance = torch.nn.functional.pairwise_distance(out1, out2).item()
        match = distance < 0.4275
        return Response(
            {
                "Status": "Signature Verification Process Completed Successfully",
                "Result": match
            }, status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "Status": "Signature Verification Process Failed",
                "Error": str(e)
            }, status=HTTP_400_BAD_REQUEST
        )
