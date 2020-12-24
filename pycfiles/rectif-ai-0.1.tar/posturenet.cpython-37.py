# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/train/posturenet.py
# Compiled at: 2019-09-17 15:56:39
# Size of source mod 2**32: 2289 bytes
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchsummary import summary
from rectifai.models.posturenet import PostureNetwork
from rectifai.settings import *
from rectifai.models.posturenet.config import *
from rectifai.data.dataset.posturenet import PostureDataset
model = PostureNetwork().to(device)
summary(model, (1, input_size))
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam((model.parameters()), lr=learning_rate)
data_loaders = {mode:DataLoader(dataset=(PostureDataset(mode)), batch_size=batch_size, shuffle=True) for mode in ('train',
                                                                                                                  'val',
                                                                                                                  'test')}
print(len(data_loaders['train']) * batch_size, ':', len(data_loaders['val']) * batch_size)

def train():
    for epoch in range(num_epochs):
        for i, (pose_coordinates, labels) in enumerate(data_loaders['train']):
            pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
            labels = labels.to(device)
            outputs = model(pose_coordinates)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, i + 1, len(data_loaders['train']), loss.item()))

        with torch.no_grad():
            correct, total = (0, 0)
            for pose_coordinates, labels in data_loaders['val']:
                pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
                labels = labels.to(device)
                outputs = model(pose_coordinates)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            print('Accuracy of the network on the test dataset: {} %'.format(100 * correct / total))


train()
torch.save(model.state_dict(), 'model.pth')