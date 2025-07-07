import os
import pickle

def load_encodings(encodings_dir):
    encodings = []
    names = []

    for file in os.listdir(encodings_dir):
        if file.endswith('.pkl'):
            with open(os.path.join(encodings_dir, file), 'rb') as f:
                data = pickle.load(f)
                encodings.append(data['encoding'])
                names.append(data['name'])
    return encodings, names
