import sys, os, math, time, random, subprocess
import numpy as np
import bpy

class DatasetRender:

  def __init__(self, dataset_dir, staging_dir, write_dir):
    self.dataset_dir = dataset_dir
    self.staging_dir = staging_dir
    self.write_dir = write_dir
    for dir in [write_dir, staging_dir]:
      if not os.path.exists(dir):
        subprocess.call(['mkdir', dir])


  #### Loading
  def load(self, category, name='shape'):
    if category == 'random':
      category = self.__getSubdirectories(self.dataset_dir)
    category_dir = os.path.join(self.dataset_dir, category)
    imported = False
    while not imported:
      subprocess.call(['mkdir', self.staging_dir])
      shape = self.__choose(category_dir)
      self.__copy( category_dir, shape, self.staging_dir )
      self.__import( os.path.join(self.staging_dir, shape, 'model.obj') )
      imported = self.__join() ## returns True only if join was successful
      subprocess.call(['rm', '-r', self.staging_dir])
    self.__subsurf()
    self.__rename('shape', name)
    print('DONE RENAMING')

  def __rename(self, old, new):
    # for obj in bpy.data.objects:
    # print(obj.name)
    bpy.data.objects[old].name = new

  def __getSubdirectories(self, base):
    return [folder for folder in os.listdir(base) if os.path.isdir(os.path.join(base, folder))]

  ## category is absolute path to dataset class
  def __choose(self, category):
    models = self.__getSubdirectories(category)
    selection = random.choice(models)
    print(os.path.join(self.dataset_dir, selection, 'model.obj'))
    return selection if os.path.exists(os.path.join(category, selection, 'model.obj')) else self.__choose(category)

  def __copy(self, category_dir, shape, newPath):
    print('COPING NEWPATH')
    # print(oldPath)
    print(newPath)
    subprocess.call(['cp', '-r', os.path.join(category_dir, shape), newPath])
    textures = [i for i in os.listdir(os.path.join(newPath, shape)) if '.mtl' in i]
    print(newPath)
    for tex in textures:
      print('MOVING ', tex)
      subprocess.call(['mv', os.path.join(newPath, shape, tex), os.path.join(newPath, shape, tex.split('_tmp')[0])])

  def __import(self, path):
    bpy.ops.import_scene.obj(filepath = path)

  def __subsurf(self):
    self.__select(lambda x: x.name == 'shape')
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.data.objects['shape'].modifiers['Subsurf'].levels = 1
    bpy.data.objects['shape'].modifiers['Subsurf'].render_levels = 1
    bpy.data.objects['shape'].modifiers['Subsurf'].subdivision_type = 'SIMPLE'

  def __select(self, function):
    for obj in bpy.data.objects:
      if function(obj):
        obj.select = True
      else:
        obj.select = False


  #### Modifying
  def __join(self):
    for obj in bpy.data.objects:
      if 'mesh' in obj.name or 'Mesh' in obj.name:
        obj.select = True
        bpy.context.scene.objects.active = obj
        obj.name = 'mesh'
      else:
        obj.select = False
    try:
      bpy.ops.object.join()
      bpy.data.objects['mesh'].name = 'shape'
      return True
    except RuntimeError:
      return False

  def __orient(self, size, coords, rotation):
    obj = bpy.data.objects['shape']
    largest_dim = max(obj.dimensions)
    scale = size / largest_dim
    for dim in range(3):
      obj.scale[dim] = scale
      obj.location[dim] = coords[dim]
      obj.rotation_euler[dim] = toRadians(rotation[dim])

  def __validate(self, scale, coords, rotation):
    for obj in bpy.data.objects:
      if 'mesh' in obj.name:
        for dim in range(3):
          if obj.dimensions[dim] > 1:
            __orient(scale / obj.dimensions[dim], coords, rotation)

  #### Deleting
  def __deleteSubShapes(self):
    for obj in bpy.data.objects:
      if 'mesh' in obj.name or 'Mesh' in obj.name:
        # if random.random() < 0.25:
        obj.select = True
        bpy.context.scene.objects.active = obj
        obj.name = 'mesh'
      else:
        obj.select = False