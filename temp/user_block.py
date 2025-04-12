# -*- coding: utf-8 -*-

def tree_build(file_path, **kwargs):
  tree = [
    {"id": ["Параметры ML модели"],
      "children": [
        {"id": ["Параметры ML модели", "x"],
         "readonly": False,
         'value': 'Число входных параметров',
         'units': ', шт',
         "type": "IntScalar"},
          {"id": ["Параметры ML модели", "y"],
           "readonly": False,
           'value': 'Число выходных параметров',
           'units': ', шт',
           "type": "IntScalar"},
          {"id": ["Параметры ML модели", "metric"],
           "readonly": False,
           'value': 'Метрика ML модели для валидации на тестовой выборке',
           'units': '',
           "type": "StringScalar"},
          {"id": ["Параметры ML модели", "degree"],
           "readonly": False,
           'value': 'Степень полинома',
           'units': ', шт',
           "type": "IntScalar"},
          {"id": ["Параметры ML модели", "percent_train"],
           "readonly": False,
           'value': 'Объем тренировочной выборки',
           'units': ', %',
           "type": "IntScalar"},
          {"id": ["Параметры ML модели", "random_seed"],
           "readonly": False,
           'value': 'Псевдослучайное число',
           'units': '',
           "type": "IntScalar"},
          # {"id": ["Параметры ML модели", "folder_path"],
           # "readonly": False,
           # 'value': 'Путь до папки, где будут создаваться файлы результатов',
           # 'units': '',
           # "type": "StringScalar"},
        {"id": ["Параметры ML модели", "go"],
         "readonly": True,
         'value': 'подсказка',
         "type": "BoolScalar"}
      ]
    }
  ]

  exec_file_path = kwargs.get("exec_file_path", "")
  metadata = {}
  return tree, metadata


def step(api, file_path, inputs, outputs, metadata, **kwargs):
  import threading
  import logging
  import json
  import os
  import time
  pseven_info = {
      'data_path' : file_path,
                 }
  for key, value in inputs.items():  # chitaem vhodnoy potok dannyh
      pseven_info[key] = api.input_read(key)
      union = file_path.split('\\')
      union = '\\'.join([union[i] for i in range(0, len(union)) if i != len(union) - 1])
      pseven_info['folder_path'] = union

  with open("{folder_path}\\PSEVEN_INFO.json".format(folder_path=pseven_info['folder_path']), 'w') as file:
      json.dump(pseven_info, file, ensure_ascii=False, indent=4)


  log = logging.getLogger("UserBlock")
  log.info('inputs')
  log.info(inputs)
  log.info('outputs')
  log.info(outputs)


  if os.path.exists("{folder_path}\\bool.txt".format(folder_path=pseven_info['folder_path'])):
      os.remove("{folder_path}\\bool.txt".format(folder_path=pseven_info['folder_path']))
  #os.startfile("{folder_path}\\start.exe".format(folder_path=pseven_info['folder_path']))
  os.startfile("{folder_path}\\start.exe".format(folder_path=pseven_info['folder_path']))
  def search_result_file():
      while True:
          if not os.path.exists("{folder_path}\\bool.txt".format(folder_path=pseven_info['folder_path'])):
              time.sleep(5)
          else:
              break
  t_temp = threading.Thread(target=search_result_file)
  t_temp.start()
  t_temp.join()

  for key, value in outputs.items():
      api.output_write(key, True)



  # Get the path specified by the Executable file path option. The user
  # should set this option, if the block starts an external process at
  # the run-time.
  exec_file_path = kwargs.get("exec_file_path", "")

  # Send a True value to all outputs. Note that output_write() converts
  # the value argument to the output port's data type.


  # Remove this exception to test the example block run-time.

  # python.exe scripts\create_block.py JSON --description "This block downloads a json file and extracts its contents."
  # --icon "C:\Users\barha\Downloads\JSON.svg" --block-group "Motyanskiy"