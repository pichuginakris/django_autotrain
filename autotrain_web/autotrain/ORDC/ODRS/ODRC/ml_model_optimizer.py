import os

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from yaml import load
from yaml import FullLoader
from .data_utils.dataset_info import dataset_info
import warnings


def load_config(config_file):
    with open(config_file) as f:
        return load(f, Loader=FullLoader)


def min_max_scaler(features):
    scaler = MinMaxScaler()
    features_normalized = np.exp(scaler.fit_transform(features))
    features_normalized /= np.sum(features_normalized, axis=0)
    return features_normalized

def get_average_fps(df, column, part_num):
    sorted_fps = np.sort(df[column])  
    num_parts = 5
    part_size = len(sorted_fps) // num_parts

    if part_num < 1 or part_num > num_parts:
        return None  

    start_idx = (num_parts - part_num) * part_size
    end_idx = (num_parts - part_num + 1) * part_size

    selected_values = sorted_fps[start_idx:end_idx]

    average_fps = np.mean(selected_values)

    return average_fps


def get_average_mAP50(df, column, part_num):
    sorted_mAP50 = np.sort(df[column])
    num_parts = 10
    part_size = len(sorted_mAP50) // num_parts

    if part_num < 1 or part_num > num_parts:
        return None

    start_idx = (part_num - 1) * part_size
    end_idx = part_num * part_size if part_num < num_parts else len(sorted_mAP50)
    selected_values = sorted_mAP50[start_idx:end_idx]
    average_mAP50 = np.mean(selected_values)
    return average_mAP50

def getting_config(path_config):
    config = load_config(path_config)
    mode = config['GPU']
    classes_path = config['classes_path']
    dataset_path = config['dataset_path']
    speed = config['speed']
    accuracy = config['accuracy']
    model_array = config['models_array']
    return mode, classes_path, dataset_path, speed, accuracy, model_array
    
    
    

def main():
    
    mode, classes_path, dataset_path, speed, accuracy, model_array = getting_config( os.path.join(os.getcwd(), 'autotrain', 'ORDC', 'ODRS', 'ODRC', 'ml_config.yaml'))
    dataset_data = dataset_info(dataset_path, classes_path)

    returned_data = dataset_data

    # Загрузка данных из CSV файла
    data = pd.read_csv(os.path.join(os.getcwd(), 'autotrain', 'ORDC', 'ODRS', 'ODRC','model_cs.csv'), delimiter=';')
    data = data.iloc[:,0:9]

    # Удаление запятых из числовых столбцов
    numeric_columns = ['FPS_GPU', 'FPS_CPU']
    data[numeric_columns] = data[numeric_columns].replace(',', '', regex=True)

    if mode:
        data = data.drop('FPS_CPU', axis=1)
        data = data.rename(columns={'FPS_GPU': 'FPS'})
    else:
        data = data.drop('FPS_GPU', axis=1)
        data = data.rename(columns={'FPS_CPU': 'FPS'})

    data = data.astype(float)


    speed = get_average_fps(data, 'FPS', speed)
    #print(speed)
    accuracy = get_average_mAP50(data, 'mAP50', accuracy)
    if accuracy is None or speed is None:
         print("Invalid part number!")
    else:
        dataset_data.append(speed)
        dataset_data.append(accuracy)

        #dataset_data = min_max_scaler([dataset_data])
        data_add = data.iloc[:,0:7]

        #print(data_add.head())
        #print(dataset_data)
        warnings.filterwarnings("ignore")
        data_add = data_add.append(pd.Series(dataset_data, index=data_add.columns), ignore_index=True)


        features = data_add[data_add.columns[0:7]].values

        labels = data['Model'].values

        features_normalized = min_max_scaler(features)

        dataset_data = features_normalized[-1]
        features_normalized = features_normalized[:-1]


        #model = RandomForestClassifier()
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(features_normalized, labels)

        probabilities = model.predict_proba([dataset_data])
        #print(probabilities)

        top_3_models = np.argsort(probabilities, axis=1)[:, ::-1][:, :3]
        #print(top_3_models)


        #print("Данные:", row[:-1].values)
        print("Top models for training:")
        returned_dict = {}
        for num_model in range(len(top_3_models[0])):
            returned_dict.update({num_model+1: model_array[top_3_models[0][int(num_model)]] })
            print(f'{num_model+1}) {model_array[top_3_models[0][int(num_model)]]}')
        return returned_data, returned_dict
            
if __name__ == "__main__":
    main()
    

