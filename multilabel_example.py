# from https://gist.github.com/bartolsthoorn/36c813a4becec1b260392f5353c8b7cc
#
# for testing ML setup in pytorch
#
#
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
from torch.autograd import Variable

# (1, 0) => target labels 0+2
# (0, 1) => target labels 1
# (1, 1) => target labels 3
train = []
labels = []
for i in range(10000):
    category = (np.random.choice([0, 1]), np.random.choice([0, 1]))
    if category == (1, 0):
        train.append([np.random.uniform(0.1, 1), 0])
        labels.append([1, 0, 1])
    if category == (0, 1):
        train.append([0, np.random.uniform(0.1, 1)])
        labels.append([0, 1, 0])
    if category == (0, 0):
        train.append([np.random.uniform(0.1, 1), np.random.uniform(0.1, 1)])
        labels.append([0, 0, 1])

class _classifier(nn.Module):
    def __init__(self, nlabel):
        super(_classifier, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, nlabel),
        )

    def forward(self, input):
        return self.main(input)

nlabel = len(labels[0]) # => 3
classifier = _classifier(nlabel)

optimizer = optim.Adam(classifier.parameters())
criterion = nn.MultiLabelSoftMarginLoss()

epochs = 5
for epoch in range(epochs):
    losses = []
    preds = []
    labs = []
    for i, sample in enumerate(train):
        inputv = Variable(torch.FloatTensor(sample)).view(1, -1)
        labelsv = Variable(torch.FloatTensor(labels[i])).view(1, -1)
        
        output = classifier(inputv)
        loss = criterion(output, labelsv)
        pred = torch.sigmoid(output).data > 0.5

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.data.mean())
        preds.append(torch.squeeze(pred).data.numpy())
        labs.append(torch.squeeze(labelsv).data.numpy())
    print('[%d/%d] Loss: %.3f' % (epoch+1, epochs, np.mean(losses)))
    preds_np = np.array(preds)
    labs_np = np.array(labs)

    acc_0 = np.mean(preds_np == labs_np, axis=0) # cross all cols
    print('acc for col=0 {}'.format(acc_0))
