import pathlib
import os
os.environ['KAGGLE_USERNAME'] = "constantinwerner"
os.environ['KAGGLE_KEY'] = "43199dd2a65321cdd12a6074144b8911"

DIR = pathlib.Path.cwd()

import kaggle


kaggle.api.authenticate()

kaggle.api.dataset_download_files('yingwurenjian/chicago-divvy-bicycle-sharing-data', path=DIR, unzip=True)