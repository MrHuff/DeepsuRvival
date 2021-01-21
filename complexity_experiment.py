from hyperopt_class import *
import numpy as np
import torch
import GPUtil
import warnings
import time

warnings.simplefilter("ignore")
datasets = ['support',
            'metabric',
            'gbsg',
            'flchain',
            'kkbox',
            'weibull',
            'checkboard',
            'normal'
            ]
#Uppgrade dataloader rip, probably uses some retarded permutation which is really slow.
#Write serious job script, figure out post processing pipeline...
if __name__ == '__main__':
    hyper_param_space = {
        # torch.nn.functional.elu,torch.nn.functional.relu,
        'bounding_op': [square],  # torch.sigmoid, torch.relu, torch.exp,
        'transformation': [torch.nn.functional.tanh],
        'depth_x': [1],
        'width_x': [32],  # adapt for smaller time net
        'depth_t': [1],
        'width_t': [1],  # ads
        'depth': [1],
        'width': [32],
        'bs': [1000],
        'lr': [1e-2],
        'direct_dif': ['autograd'],
        'dropout': [0.25],
        'eps': [1e-3],
        'weight_decay': [0]
    }
    timings = []
    devices = GPUtil.getAvailable(order='memory', limit=8)
    device = devices[0]
    for i in [0,1,2,3,4,5,6,7]:
        for net in ['benchmark','survival_net_basic']:
            if net=='benchmark':
                hyper_param_space['depth']=[2]
            else:
                hyper_param_space['depth']=[1]
            for f in [0,1,2,3,4]:
                job_params = {
                    'd_out': 1,
                    'dataset_string': datasets[i],
                    'seed': 1337,#,np.random.randint(0,9999),
                    'eval_metric': 'train',
                    'total_epochs': 1,
                    'device': device,
                    'patience': 50,
                    'hyperits': 1,
                    'selection_criteria':'ibs',
                    'grid_size':100,
                    'test_grid_size':100,
                    'validation_interval':10,
                    'net_type':net,
                    'objective': 'S_mean',
                    'fold_idx':f,
                    'savedir':'complexity_test'

                }
                training_obj = hyperopt_training(job_param=job_params,hyper_param_space=hyper_param_space)
                training_obj.run()
                timing = training_obj.complexity_test(100)
                timings.append([i,net,f,timing])

    df = pd.DataFrame(timings,columns=['dataset','net','fold','time'])
    df.to_csv('raw_timings_new_redo.csv')
