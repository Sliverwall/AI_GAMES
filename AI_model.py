import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Generate synthetic data with sequences
def generate_data_with_sequences(n_samples=1000, sequence_length=5):
    moves = ['R', 'P', 'S']
    data = []
    results = []
    
    for _ in range(n_samples):
        player_moves = np.random.choice(moves, size=sequence_length)
        bot_moves = np.random.choice(moves, size=sequence_length)
        
        player_sequence = ''.join(player_moves)
        bot_sequence = ''.join(bot_moves)
        
        player_last_move = player_moves[-1]
        bot_last_move = bot_moves[-1]
        
        if player_last_move == bot_last_move:
            result = 0  # draw
        elif (player_last_move == 'R' and bot_last_move == 'S') or \
             (player_last_move == 'P' and bot_last_move == 'R') or \
             (player_last_move == 'S' and bot_last_move == 'P'):
            result = 2  # user wins
        else:
            result = 1  # user loses
        
        data.append([player_sequence, bot_sequence])
        results.append(result)
    
    return np.array(data), np.array(results)

# Convert sequences to numeric values
def convert_to_numeric(data):
    numeric_data = []
    moves_map = {'R': 0, 'P': 1, 'S': 2}
    
    for sequence in data:
        numeric_sequence = [moves_map[move] for move in sequence]
        numeric_data.append(numeric_sequence)
    
    return np.array(numeric_data)

# Prepare the data
X, y = generate_data_with_sequences(5000)

print(X[0:5])
print(y[0:5])


# # Convert sequences to numeric values
# X_player = convert_to_numeric(X[:, 0])
# X_bot = convert_to_numeric(X[:, 1])

# # Reshape data for CNN input
# X_player_reshaped = X_player.reshape((X_player.shape[0], X_player.shape[1], 1))
# X_bot_reshaped = X_bot.reshape((X_bot.shape[0], X_bot.shape[1], 1))
# X_reshaped = np.concatenate((X_player_reshaped, X_bot_reshaped), axis=-1)  # Combine player and bot moves

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.2, random_state=42)

# # Build the CNN model
# model = tf.keras.Sequential([
#     tf.keras.layers.Conv1D(32, kernel_size=2, activation='relu', input_shape=(5, 2)),
#     tf.keras.layers.MaxPooling1D(pool_size=1),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(3, activation='softmax')
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# # Save the model weights
# model.save_weights('model_weights.weights.h5')

# # Evaluate the model
# loss, accuracy = model.evaluate(X_test, y_test)
# print(f'Test accuracy: {accuracy}')
