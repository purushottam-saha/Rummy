# This is the code used to run the large_Scale simulations.

import random
import pandas as pd
import multiprocessing
from rummy import RummyGame
from rummy import RandomAgent, DefeatHeur, MinscoreAgent, MindistAgent, MindistscoreAgent, MindistOpp2Agent 
from time import time

def worker(see,p1,p2,quantity=5): # 13 card desc
    random.seed(see)
    data = pd.DataFrame(columns=['sc1','sc2','winnerid','numrounds','pseqc','iseqc','setc'])
    i = 0
    t1=time()
    while (i < quantity):
        p1.reset()
        p2.reset()
        game = RummyGame([p1,p2],1,1,13,log=False)
        out = game.playgame()
        data.loc[i] = [out['sc1'],out['sc2'],out['winner'],out['numrounds'],out['pseqc'],out['iseqc'],out['setc']]
        i+=1
    print(f'rummy13.game.{p1}.vs.{p2}.joker.seed.{see} done, {time()-t1} seconds in')
    data.to_csv(f'Outputs/games/rummy13.game.{p1}.vs.{p2}.seed.{see}.csv')
  
class Process_(multiprocessing.Process): 
    def __init__(self, id, seed, work, p1, p2, quantity=5): 
        super(Process_, self).__init__() 
        self.id = id
        self.seed = seed
        self.work = work # 1 or 2
        self.p1=p1
        self.p2=p2
        if isinstance(self.p1,MinscoreAgent):
            if work==1:
                self.p1.firstfold=50
            else:
                self.p1.firstfold=80
        if isinstance(self.p2,MinscoreAgent):
            if work==1:
                self.p2.firstfold=50
            else:
                self.p2.firstfold=80
        self.quantity = quantity
                 
    def run(self): 
        t11 = time()
        worker(self.seed,self.p1,self.p2,quantity=self.quantity)
        print(f"Process {self.id}: Game {self.work} between {self.p1} and {self.p2} finished for seed {self.seed} {time()-t11}")



def main(seed=15512,drop=True,numgames=5):
    players1 = [
        RandomAgent('Random1',drop=drop),
        DefeatHeur('Defeat1',drop=drop),
        MindistAgent('Mindist1',4,drop=drop),
        MinscoreAgent('Minscore1',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore1',4,drop=drop),
        MindistOpp2Agent('MindistOpp1',4,drop=drop)
    ]
    players2 = [
        RandomAgent('Random2',drop=drop),
        DefeatHeur('Defeat2',drop=drop),
        MindistAgent('Mindist2',4,drop=drop),
        MinscoreAgent('Minscore2',80,piletake=3,drop=drop),
        MindistscoreAgent('Mindistscore2',4,drop=drop),
        MindistOpp2Agent('MindistOpp2',4,drop=drop)
    ]
    pool = [Process_(j-1+10*players1.index(p1)+100*players2.index(p2),seed,j,p1,p2,numgames) for p1 in players1 for p2 in players2 for j in [2,]]
    for p in pool:
        p.start()
    print("Games Started") 
    for p in pool:
        p.join()



if __name__=="__main__":
    seed = 15512
    t10 = time()
    main(seed,drop=True,numgames=1000)
    t20 = time()
    print(t20-t10,'seconds taken for the games to run')




