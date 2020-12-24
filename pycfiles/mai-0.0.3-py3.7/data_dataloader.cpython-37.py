# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\code\dataloader\data_dataloader.py
# Compiled at: 2020-03-09 21:59:41
# Size of source mod 2**32: 1252 bytes
"""
数据输入：numpy
类型：
默认值：

数据输出：Tensor
类型：
默认值：
"""
train_data_transform = transforms.Compose([
 transforms.ToTensor(),
 transforms.Normalize([0.5], [0.5])])
val_transform = transforms.Compose([
 transforms.ToTensor(),
 transforms.Normalize([0.5], [0.5])])
test_transform = transforms.Compose([
 transforms.ToTensor(),
 transforms.Normalize([0.5], [0.5])])
train_batch_size = 256
val_batch_size = 256
test_batch_size = 256
train_dataset = torch.utils.data.TensorDataset(torch.from_numpy(train_data), train_target)
val_dataset = torch.utils.data.TensorDataset(torch.from_numpy(val_data), val_target)
test_dataset = torch.utils.data.TensorDataset(torch.from_numpy(test_data), test_target)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=train_batch_size, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=val_batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=test_batch_size, shuffle=False)