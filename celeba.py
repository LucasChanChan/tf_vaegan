from dataset.datasets import CelebA
from models.vaegan import VAEGAN
from dataset.utils import batchify
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--arch', dest='arch', help='Path of the architecture file', required=True)
parser.add_argument('--tb_id', dest='tb_id', help='Tensorboard log id and model id to save to storege/id', required=True)
parser.add_argument('--n_jobs', dest='n_jobs', default=128, help='Jobs to run in parallel for reading the dataset', type=int)
FLAGS = parser.parse_args()

arch_json = json.load(open(FLAGS.arch))

print("Loading dataset")
celeba = CelebA(path=None)
X = celeba.load_dataset(FLAGS.n_jobs)

model = VAEGAN([64, 64, 64, 3], arch_json, FLAGS.tb_id)
model.compile()

for e in range(500):
  print("Epoch", e+1)
  for x_b in batchify(X, 64):
    enc_loss, dec_loss, dis_loss = model.fit(x_b)
  model.save('storage/{}'.format(FLAGS.tb_id))