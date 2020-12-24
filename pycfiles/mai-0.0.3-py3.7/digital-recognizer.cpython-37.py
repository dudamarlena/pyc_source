# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\code\dataprocess\digital-recognizer.py
# Compiled at: 2020-03-09 21:59:41
# Size of source mod 2**32: 1399 bytes
import kaggle, os
traindata = pathlib.Path('data\\digit-recognizer\\train.csv')
testdata = pathlib.Path('data\\digit-recognizer\\test.csv')
sample_subdata = pathlib.Path('data\\digit-recognizer\\knn_benchmark.csv')
digital_train_data = pd.read_csv(traindata, dtype=(np.float32))
digital_test_data = pd.read_csv(testdata, dtype=(np.float32))
targets_np = digital_train_data.label.values
features_np = digital_train_data.loc[:, digital_train_data.columns != 'label'].values / 255
final_test_np = digital_test_data.values / 255
test_tn = torch.from_numpy(final_test_np)
test_target = np.zeros(final_test_np.shape)
test_target = torch.from_numpy(test_target)
features_train, features_val, target_train, target_val = train_test_split(features_np, targets_np, test_size=0.2, random_state=42)
train_data = features_train
train_target = torch.from_numpy(target_train).type(torch.LongTensor)
val_data = features_val
val_target = torch.from_numpy(target_val).type(torch.LongTensor)
test_data = final_test_np
test_target = test_target.type(torch.LongTensor)