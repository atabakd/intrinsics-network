import sys, fnmatch, os, random

sys.path.append(".")
import config

sys.path.append(config.include)
from dataset import DatasetRender


class ShapeNetRender(DatasetRender):
  
  def __init__(self, ycb_models_dir, staging_dir, write_dir):
    super().__init__(dataset_dir=ycb_models_dir,
                     staging_dir=staging_dir,
                     write_dir=write_dir)
  
  def load(self, category, name='shape'):
    if category == 'random':
      category = self.__get_possible_objs(self.dataset_dir)
    else:
      category = [os.path.join(self.dataset_dir,
                              category,
                              "textured.obj")]
    imported = False
    while not imported:
      if not os.path.exists(self.staging_dir):
        os.makedirs(self.staging_dir)
      
      shape = random.choice(category)
      
      
  
  @staticmethod
  def __get_possible_objs(base):
    objs = list()
    for root, _, filenames in os.walk(base):  # _ is 'dirnames'
      for filename in fnmatch.filter(filenames, 'textured.obj'):
        objs.append(os.path.join(root, filename))
    
    return objs
