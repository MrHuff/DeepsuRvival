from utils.plot_utils import *
from utils.dataloaders import *
from debug_run import datasets


dstr = datasets[6]
seed = 123
model = load_best_model(dstr,seed)
dl = get_dataloader(dstr,100,seed)
dl.dataset.set('test')
max_time = 1.0

# X,y,delta=next(iter(dl))

X = torch.Tensor([[0.1],[0.4]])
plot_survival(X,model,max_time,'test.png',1000)


