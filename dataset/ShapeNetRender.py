import sys, os, math, time, random, subprocess
import numpy as np
import bpy
sys.path.append(".")
import config
sys.path.append(config.include)
from dataset import DatasetRender

class ShapeNetRender(DatasetRender):

    def __init__(self, shapenet_path, staging_path, write_path, create=False):
        super().__init__(dataset_path = shapenet_path,
                         staging_path = staging_path,
                         write_path = write_path,
                         create = create)
