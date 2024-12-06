import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score

# Signal Processing Utilities
def generate_dvb_s2x_waveforms(modulation_type, num_samples):
    """
    Generate DVB-S2X waveforms for given modulation type.
    modulation_type: 'QPSK', '16APSK'
    """
    if modulation_type == 'QPSK':
        symbols = np.array([1+1j, 1-1j, -1+1j, -1-1j])
    elif modulation_type == '16APSK':
        symbols = np.exp(1j * np.pi / 8 * np.arange(16))  # Placeholder for APSK
    else:
        raise ValueError("Unknown modulation type")

    signal = np.random.choice(symbols, num_samples)
    return signal

def add_noise(signal, snr_db):
    """
    Add white Gaussian noise to the signal based on the specified SNR (dB).
    """
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = signal_power / (10 ** (snr_db / 10))
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    return signal + noise

# Feature Extraction Utilities
def extract_features(signal):
    """
    Extract features like power, phase, and amplitude from the signal.
    """
    features = []
    amplitude = np.abs(signal)
    phase = np.angle(signal)
    features.append(np.mean(amplitude))  # Mean amplitude
    features.append(np.var(amplitude))   # Amplitude variance
    features.append(np.mean(phase))      # Mean phase
    features.append(np.var(phase))       # Phase variance
    return features

# Data Preparation
def prepare_dataset(num_samples_per_class, snr_db=20):
    modulations = ['QPSK', '16APSK']
    X, y = [], []

    for mod in modulations:
        for _ in range(num_samples_per_class):
            signal = generate_dvb_s2x_waveforms(mod, 1000)  # Generate signal
            noisy_signal = add_noise(signal, snr_db)        # Add noise
            features = extract_features(noisy_signal)       # Extract features
            X.append(features)
            y.append(mod)

    return np.array(X), np.array(y)

# Neural Network Model for AMR
def build_amr_model(input_shape):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(input_shape,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Binary classification (QPSK or APSK)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Training and Testing
def train_amr_model():
    # Generate dataset
    X, y = prepare_dataset(1000, snr_db=20)

    # Encode labels to binary (QPSK: 0, APSK: 1)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Build and train the AMR model
    model = build_amr_model(X_train.shape[1])
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

    # Predict on test set
    y_pred = model.predict(X_test)
    y_pred = (y_pred > 0.5).astype(int).flatten()

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

    return model

if __name__ == "__main__":
    model = train_amr_model()
