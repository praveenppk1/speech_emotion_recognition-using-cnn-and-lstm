# -*- coding: utf-8 -*-
"""predict.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ocIxi2Og3t2Q-2YjZuYdSK2YsIjPjvO5
"""

pip install keras_self_attention

from keras.models import load_model
from keras_self_attention import SeqSelfAttention
import numpy as np
import os
import librosa
# Load the saved model
saved_model = load_model('best_model.h5', custom_objects={'SeqSelfAttention': SeqSelfAttention})

def normalize(s):
    # RMS normalization
    new_s = s / np.sqrt(np.sum(np.square((np.abs(s)))) / len(s))
    return new_s

# Load the input audio file
input_file_path = '/content/drive/MyDrive/Emo-db/wav/03a01Fa.wav'
signal, sr = librosa.load(input_file_path, sr=16000)

# Normalize the signal
data = normalize(signal)
seg_len = 16000
seg_ov = int(seg_len * 0.5)
input_length = len(data)
max_input_length = seg_len  # Assuming seg_len is the maximum input length expected by the model
if input_length > max_input_length:
    print("Warning: Input length exceeds maximum length. Truncating or processing in segments may be required.")

# Pad or truncate the data to match the model's input shape
if input_length < max_input_length:
    pad_length = max_input_length - input_length
    data = np.pad(data, (0, pad_length), mode='constant', constant_values=0)
elif input_length > max_input_length:
    data = data[:max_input_length]

# Reshape the data for the model
x_input = data.reshape(-1, max_input_length, 1)

# Make predictions using the loaded model
predictions = saved_model.predict(x_input)

# Decode the predictions to get the emotion labels
emotions = ['W', 'L', 'E', 'A', 'F', 'T', 'N']
emotion_mapping = {
    'W': 'Anger',
    'L': 'Boredom',
    'E': 'Disgust',
    'A': 'Anxiety',
    'F': 'Happiness',
    'T': 'Sadness',
    'N': 'Neutral'
} # Assuming these are the emotion labels
predicted_emotions = [emotions[np.argmax(pred)] for pred in predictions]
predicted_emotions_names = [emotion_mapping[emotion] for emotion in predicted_emotions]
# Display the predicted emotions
for i, emotion_name in enumerate(predicted_emotions_names):
    print(f"Segment {i+1}: Predicted Emotion - {emotion_name}")