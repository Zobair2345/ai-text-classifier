import streamlit as st

from src.predict import predict_news


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI News Classifier",
    page_icon="📰",
    layout="centered"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📰 AI News Classifier")

st.write(
    "Enter a news headline or article and the AI model will "
    "classify it as **World, Sports, Business, or Sci/Tech**."
)

st.caption(
    "Powered by a fine-tuned DistilBERT Transformer • "
    "Trained on the AG News dataset"
)


# --------------------------------------------------
# User input
# --------------------------------------------------

news_text = st.text_area(
    "News text",
    placeholder=(
        "Example: Apple announced a new artificial intelligence "
        "platform for its devices..."
    ),
    height=180
)


# --------------------------------------------------
# Classification
# --------------------------------------------------

if st.button("Classify", type="primary"):

    if news_text.strip():

        # Run our DistilBERT prediction function
        with st.spinner("Analyzing article..."):
            result = predict_news(news_text)

        prediction = result["prediction"]
        probabilities = result["probabilities"]


        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        st.subheader("Prediction")

        st.success(f"Predicted category: **{prediction}**")


        # ------------------------------------------
        # Probabilities
        # ------------------------------------------

        st.subheader("Category probabilities")

        # Sort categories from highest to lowest probability
        sorted_probabilities = sorted(
            probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, probability in sorted_probabilities:

            st.write(
                f"**{category} — {probability:.2%}**"
            )

            st.progress(float(probability))


        # ------------------------------------------
        # Disclaimer
        # ------------------------------------------

        st.divider()

        st.caption(
            "The percentages represent the model's classification "
            "confidence. This application categorizes news content "
            "and does not verify whether the information is true or false."
        )

    else:

        st.warning(
            "Please enter a news headline or article before clicking Classify."
        )


# --------------------------------------------------
# Model information
# --------------------------------------------------

with st.expander("About the model"):

    st.write(
        """
        This application uses **DistilBERT**, a pretrained Transformer
        language model fine-tuned for news classification.

        The model predicts four AG News categories:

        - 🌍 **World**
        - ⚽ **Sports**
        - 💼 **Business**
        - 💻 **Sci/Tech**

        The fine-tuned model achieved **91.49% accuracy** on the
        official AG News test set containing **7,600 unseen articles**.
        """
    )