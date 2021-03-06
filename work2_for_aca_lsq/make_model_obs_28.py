from __future__ import print_function
from __future__ import division
from cctbx.array_family import flex
import glob
from six.moves import cPickle as pickle
from six.moves import range

class GM (object):
 def generate_millers(self):
  #globv = "../work/dataX0[0-1].pickle" #test
  globv = "dataX*.pickle" # production
  self.asu = {}
  self.icount = 0
  self.images_all = 0
  self.images_strong = {}
  self.images_Gi = {}
  for filen in glob.glob(globv):

   with open(filen,"rb") as V:
    while 1:
     try:
      image = pickle.load(V)

      self.images_all+=1
      highcc = flex.double(image["cc"]) > 0.80 #was 0.7 and minimum 4
      if highcc.count(True)<3: continue
      imdict = dict()
      self.images_strong[image["image"]]=imdict
      for i in range(len(image["cc"])):
        if image["cc"][i]<0.8: continue
        self.icount+=1
        imdict[image["asu_idx_C2_setting"][i]]=dict(model=image["model"][i],
          obs=flex.double(image["obs"][i]),
          cc=image["cc"][i], simtbx_intensity=image["simtbx_intensity"][i],
          simtbx_miller=image["simtbx_millers"][i],orig_index=image["orig_idx_C2_setting"][i],
          simtbx_miller_DIALS_setting=image["simtbx_millers_DIALS_setting"][i],
        )
        print (filen,self.icount,"CC>70%%: %20s %5.2f"%(image["asu_idx_C2_setting"][i],image["cc"][i]))
        #from matplotlib import pyplot as plt
        #model = image["model"][i]
        #obs = image["obs"][i]
        #plt.plot(range(len(model)),model,"k-")
        #plt.plot(range(len(obs)),1.E10*flex.double(obs),"r-")
        #plt.show()
        self.asu[image["asu_idx_C2_setting"][i]]=1

        yield image["asu_idx_C2_setting"][i]

     except EOFError:
      break

if __name__=="__main__":
  M = flex.miller_index()
  G = GM()
  for i in G.generate_millers():
    M.append(i)
  print ("%d Bragg spots measured"%len(M))

  print ("%d Unique Miller indices"%(len(G.asu)))
  with open("make_model_obs_28.pickle","wb") as VVV:
    pickle.dump(G,VVV,pickle.HIGHEST_PROTOCOL)
