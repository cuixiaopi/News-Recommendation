import os
import sys
os.chdir('/home/peitian_zhang/Codes/News-Recommendation')
sys.path.append('/home/peitian_zhang/Codes/News-Recommendation')

import torch
from utils.utils import evaluate,train,prepare,load_hparams,test
from models.FIM import FIMModel

if __name__ == "__main__":
    hparams = {
        'name':'fim',
        'dropout_p':0.2,
        'filter_num':150,
        'embedding_dim':300,
    }

    hparams = load_hparams(hparams)
    device = torch.device(hparams['device'])

    vocab, loaders = prepare(hparams)
    fimModel = FIMModel(vocab=vocab,hparams=hparams).to(device)

    if hparams['mode'] == 'dev':
        evaluate(fimModel,hparams,loaders[0],load=True)

    elif hparams['mode'] == 'train':
        train(fimModel, hparams, loaders)

    elif hparams['mode'] == 'test':
        test(fimModel, hparams, loaders[0])