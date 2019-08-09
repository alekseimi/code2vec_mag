from common import common
from extractor import Extractor
import os
import csv

SHOW_TOP_CONTEXTS = 2
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


# 1. Pridobi vektor in ime metode
# raw_prediction, method_prediction_results
# raw_prediction.original__name
# 2. Ime metode oblike x|y|z pretvori
class VectorBuilder:
    #
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

    def iterate_over_directory(self, rootdir, project_name):
        dir_list = []
        full_list = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                # print os.path.join(subdir, file)
                filepath = subdir + os.sep + file
                if filepath.endswith(".java"):
                    generated_list = self.generate_code_vectors(filepath, project_name)
                    if generated_list is None:
                        continue
                    print(filepath + "list size: " + str(len(generated_list)))
                    full_list.extend(generated_list)
                    dir_list.append(filepath)

        self.dump_dirlist_to_csv(dir_list, project_name)
        return full_list

    def dump_dirlist_to_csv(self, dirlist, project_name):
        with open(project_name+'.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(dirlist)
            return True
        return False

    def generate_code_vectors(self, filename, project_name):
        try:
            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(filename)
        except ValueError as e:
            return None
        raw_prediction_results = self.model.predict(predict_lines)
        method_prediction_results = common.parse_prediction_results(
            raw_prediction_results, hash_to_string_dict,
            self.model.vocabs.target_vocab.special_words, topk=SHOW_TOP_CONTEXTS)
        item_list = []
        for raw_prediction, method_prediction in zip(raw_prediction_results, method_prediction_results):
            #values_list = [project_name, raw_prediction.original_name]
            #full_values = values_list + raw_prediction.code_vector.tolist()
            #item_list.append(full_values)
            item_list.append(raw_prediction.code_vector.tolist())
        return item_list
