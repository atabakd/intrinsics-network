import sys, fnmatch, os, random

sys.path.append(".")
import config
sys.path.append(config.include)
from dataset import DatasetRender

class ShapeNetRender(DatasetRender):

  def __init__(self, ycb_models_path, staging_path, write_path):
    super().__init__(dataset_path = ycb_models_path,
                     staging_path = staging_path,
                     write_path = write_path)


  def load(self, category, name='shape'):
    if category == 'random':
      category = self.__get_possible_objs(self.dataset_path)


  @staticmethod
  def __get_possible_objs(base):
    objs = list()
    for root, _, filenames in os.walk(base):  # _ is 'dirnames'
      for filename in fnmatch.filter(filenames, 'textured.obj'):
        objs.append(os.path.join(root, filename))

    return objs




