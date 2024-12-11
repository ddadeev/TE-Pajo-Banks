import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    /* Custom color palette */
    :root {
        --primary-color: #3B82F6;
        --secondary-color: #10B981;
        --background-color: #F3F4F6;
        --text-color: #1F2937;
    }

    /* App container styling */
    .main-container {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        padding: 30px;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Custom header styling */
    .title {
        color: var(--primary-color);
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--background-color);
    }

    /* Card styling for predictions */
    .prediction-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Progress bar customization */
    .stProgress > div > div > div {
        background-color: var(--primary-color);
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 10px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: var(--secondary-color);
        transform: scale(1.05);
    }

    /* Image upload styling */
    .uploadedImage {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="Card Recognizer",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Model loading (keep existing implementation)
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        model_path = 'models/card_recognition_model.keras'
        if not os.path.exists('models'):
            os.makedirs('models')

        if not os.path.exists(model_path):
            with st.spinner('Downloading model... Please wait.'):
                model_url = "https://drive.google.com/uc?id=1336Cr4O1bqoz2pOhKwcjTI5MF9-24r2t"
                gdown.download(model_url, output=model_path, quiet=True)

        return tf.keras.models.load_model(model_path)
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Existing class names and class info (from previous code)
class_names = [
    'ace of clubs', 'ace of diamonds', 'ace of hearts', 'ace of spades',
    'eight of clubs', 'eight of diamonds', 'eight of hearts', 'eight of spades',
    'five of clubs', 'five of diamonds', 'five of hearts', 'five of spades',
    'four of clubs', 'four of diamonds', 'four of hearts', 'four of spades',
    'jack of clubs', 'jack of diamonds', 'jack of hearts', 'jack of spades',
    'joker',
    'king of clubs', 'king of diamonds', 'king of hearts', 'king of spades',
    'nine of clubs', 'nine of diamonds', 'nine of hearts', 'nine of spades',
    'queen of clubs', 'queen of diamonds', 'queen of hearts', 'queen of spades',
    'seven of clubs', 'seven of diamonds', 'seven of hearts', 'seven of spades',
    'six of clubs', 'six of diamonds', 'six of hearts', 'six of spades',
    'ten of clubs', 'ten of diamonds', 'ten of hearts', 'ten of spades',
    'three of clubs', 'three of diamonds', 'three of hearts', 'three of spades',
    'two of clubs', 'two of diamonds', 'two of hearts', 'two of spades'
]

class_info = {
    'Ace of Spades': 'The highest-ranking card in the suit of Spades.',
    '2 of Spades': 'A low-ranking card in the suit of Spades.',
    # Add more descriptions as needed
}

# Image preprocessing (keep existing implementation)
def preprocess_image(img):
    img = img.convert("RGB")
    img = np.array(img)
    img = tf.image.resize(img, [224, 224])
    img = img / 255.0
    return np.expand_dims(img, axis=0)

# Prediction function (keep existing implementation)
def predict(model, img):
    prediction = model.predict(img, verbose=0)
    predicted_class_idx = np.argmax(prediction[0])
    confidence = prediction[0][predicted_class_idx]
    return class_names[predicted_class_idx], confidence, prediction[0]

# Main app
def main():
    # Apply custom CSS
    local_css()

    # Main container with custom styling
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Title with custom styling
    st.markdown('<h1 class="title">🃏 Card Recognition AI</h1>', unsafe_allow_html=True)

    # Load the model
    model = load_model()

    if model is None:
        st.error("Failed to load model. Please refresh the page.")
        return

    # Input method selection with improved styling
    col1, col2 = st.columns(2)
    with col1:
        upload_option = st.button("📤 Upload Image", use_container_width=True)
    with col2:
        camera_option = st.button("📷 Use Camera", use_container_width=True)

    # Determine input method
    input_method = "upload" if upload_option else "camera" if camera_option else "initial"

    # Image input based on selection
    if input_method == "upload":
        uploaded_file = st.file_uploader("Upload a playing card image", type=["jpg", "jpeg", "png"])
        image = uploaded_file
    elif input_method == "camera":
        image = st.camera_input("Take a picture")
    else:
        st.info("Select an input method to get started")
        image = None

    # Prediction process
    if image is not None:
        # Open the image
        pil_image = Image.open(image)
        
        # Display image with custom styling
        st.image(pil_image, caption="Uploaded Image", use_column_width=True, 
                 output_format="PNG", 
                 channels="RGB")

        # Preprocess and predict
        processed_img = preprocess_image(pil_image)

        with st.spinner("Analyzing image..."):
            class_name, confidence, all_predictions = predict(model, processed_img)

        # Create columns for results
        col1, col2 = st.columns([2,1])

        with col1:
            # Prediction card with custom styling
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.markdown(f"**Predicted Card:** {class_name.title()}")
            st.markdown(f"**Confidence:** {confidence:.1%}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Card description
            st.markdown("### Card Info")
            st.markdown(class_info.get(class_name.title(), "No description available."))

        # Detailed probabilities with progress bars
        st.markdown("### Probability Breakdown")
        
        # Sort and filter predictions
        predictions_with_names = list(zip(class_names, all_predictions))
        sorted_predictions = sorted(predictions_with_names, key=lambda x: x[1], reverse=True)
        non_zero_predictions = [(name, prob) for name, prob in sorted_predictions if prob > 0.01]

        # Display top predictions
        for name, prob in non_zero_predictions[:5]:  # Show top 5 predictions
            st.progress(float(prob), text=f"{name.title()}: {prob:.1%}")

    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
