from config import Config
from model_base import Code2VecModelBase
from build_vectors import VectorBuilder
import pandas as pd


def load_model_dynamically(config: Config) -> Code2VecModelBase:
    assert config.DL_FRAMEWORK in {'tensorflow', 'keras'}
    if config.DL_FRAMEWORK == 'tensorflow':
        from tensorflow_model import Code2VecModel
    elif config.DL_FRAMEWORK == 'keras':
        from keras_model import Code2VecModel
    return Code2VecModel(config)


def define_columns(vector_column_names):
    default_vector_name = "vec_comp_"
    for x in range(384):
        vector_column_names.append(default_vector_name + str(x))
    return vector_column_names



config = Config(set_defaults=True, load_from_args=True, verify=True)
config.EXPORT_CODE_VECTORS = True
model = load_model_dynamically(config)
config.log("Model loaded")
#columns = ['project_name', 'method_name']
columns = []
columns = define_columns(columns)

#project_path = "E:\\Program Files\\commons-lang-master\\src"
# project_test_path = "E:\\Program Files\\commons-lang-master\\src\\main\\java\\org\\apache\\commons\\lang3\\text"
project_small_test_path = "E:\\Program Files\\commons-lang-master\\src\\main\\java\\org\\apache\\commons\\lang3"
predictor = VectorBuilder(config, model)
full_list = predictor.iterate_over_directory(project_small_test_path, "apache_commons")
df = pd.DataFrame(data=full_list, columns=columns)
df.to_csv(path_or_buf="apache_df.csv")
print(len(full_list))

