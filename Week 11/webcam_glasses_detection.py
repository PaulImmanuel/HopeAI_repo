import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model(
    "glasses_detector.keras"
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    img = cv2.resize(frame, (128,128))

    img = img.astype("float32") / 255.0

    img = np.expand_dims(img, axis=0)

    prediction = model.predict(
        img,
        verbose=0
    )[0][0]

    if prediction < 0.5:
        label = f"GLASSES ({(1-prediction)*100:.1f}%)"
        color = (0,255,0)
    else:
        label = f"NO GLASSES ({prediction*100:.1f}%)"
        color = (0,0,255)

    cv2.putText(
        frame,
        label,
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow(
        "Eyeglass Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()