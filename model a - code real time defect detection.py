import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define constants
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 32
NUM_CLASSES = 2  # Defect and No Defect

# Load and prepare the dataset (assume you have a function for this)
train_data, val_data = load_and_prepare_dataset()

# Data Augmentation
data_augmentation = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

# Build the model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=INPUT_SHAPE)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
output = Dense(NUM_CLASSES, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=output)

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    data_augmentation.flow(train_data[0], train_data[1], batch_size=BATCH_SIZE),
    steps_per_epoch=len(train_data[0]) // BATCH_SIZE,
    epochs=20,
    validation_data=val_data
)

# Fine-tune the model
for layer in model.layers[-20:]:
    layer.trainable = True

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history_fine = model.fit(
    data_augmentation.flow(train_data[0], train_data[1], batch_size=BATCH_SIZE),
    steps_per_epoch=len(train_data[0]) // BATCH_SIZE,
    epochs=10,
    validation_data=val_data
)

# Save the model
model.save('advanced_defect_detection_model.h5')

# Real-time defect detection
def detect_defects(frame, model, confidence_threshold=0.7):
    # Preprocess the frame
    resized_frame = cv2.resize(frame, (INPUT_SHAPE[0], INPUT_SHAPE[1]))
    input_tensor = preprocess_input(np.expand_dims(resized_frame, axis=0))

    # Perform defect detection
    predictions = model.predict(input_tensor)
    defect_probability = predictions[0][1]  # Assuming class 1 is defect

    # Apply confidence thresholding
    if defect_probability > confidence_threshold:
        return True, defect_probability
    else:
        return False, defect_probability

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect defects
    has_defect, prob = detect_defects(frame, model)

    # Draw results on the frame
    result_text = f"Defect Probability: {prob:.2f}"
    cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if has_defect:
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 3)

    # Display the frame
    cv2.imshow('Advanced Defect Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
