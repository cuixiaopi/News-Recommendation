import os
import sys
os.chdir('/home/peitian_zhang/Codes/News-Recommendation')
sys.path.append('/home/peitian_zhang/Codes/News-Recommendation')

from utils.utils import prepare,load_hparams,tune,generate_hparams
from configs.sfi_fim import config

if __name__ == "__main__":
    hparams = {
        'name':'sfi-fim',
        'dropout_p':0.2,
        'embedding_dim':300,
        'filter_num':150,
    }
    hparams = load_hparams(hparams)

    best_auc = 0

    for hparam in generate_hparams(hparams, config):
        if hparam['his_size'] == 50 and hparam['k'] == 10:
            continue
        vocab, loaders = prepare(hparams)

        if hparams['select'] == 'unified':
            hparams['name'] = hparams['name'] + '-unified'
            from models.SFI_FIM import SFIModel_unified
            sfiModel = SFIModel_unified(vocab=vocab,hparams=hparams).to(hparams['device'])
        
        elif hparams['select'] == 'pipeline1':
            hparams['name'] = hparams['name'] + '-pipeline1'
            from models.SFI_FIM import SFIModel_pipeline1
            sfiModel = SFIModel_pipeline1(vocab=vocab,hparams=hparams).to(hparams['device'])

        elif hparams['select'] == 'pipeline2':
            hparams['name'] = hparams['name'] + '-pipeline2'
            from models.SFI_FIM import SFIModel_pipeline2
            sfiModel = SFIModel_pipeline2(vocab=vocab,hparams=hparams).to(hparams['device'])
        
        elif hparams['select'] == 'gating':
            hparams['name'] = hparams['name'] + '-gating'
            from models.SFI_FIM import SFIModel_gating
            sfiModel = SFIModel_gating(vocab=vocab,hparams=hparams).to(hparams['device'])

        best_auc_sub = tune(sfiModel, hparam, loaders, best_auc=best_auc)
        
        if best_auc_sub > best_auc:
            best_auc = best_auc_sub
    
    print(best_auc)