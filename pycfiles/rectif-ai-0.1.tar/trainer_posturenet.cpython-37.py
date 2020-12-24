# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/train/trainer_posturenet.py
# Compiled at: 2019-09-17 14:25:24
# Size of source mod 2**32: 1873 bytes
import torch
import torch.nn as nn
from rectifai.models.posturenet import PostureNetwork
from rectifai.settings import *
from rectifai.models.posturenet.config import *
from rectifai.data.dataloaders.posturenet import train_loader, test_loader
model = PostureNetwork().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam((model.parameters()), lr=learning_rate)
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, (pose_coordinates, labels) in enumerate(train_loader):
        pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
        labels = labels.to(device)
        outputs = model(pose_coordinates)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

    with torch.no_grad():
        correct = 0
        total = 0
        for pose_coordinates, labels in test_loader:
            pose_coordinates = pose_coordinates.reshape(-1, input_size).to(device)
            labels = labels.to(device)
            outputs = model(pose_coordinates)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print('Accuracy of the network on the 10000 test pose coordinates: {} %'.format(100 * correct / total))

torch.save(model.state_dict(), 'model.ckpt')