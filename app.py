
import streamlit as st
import pandas as pd

from src.predict import predict_news
from src.database import get_articles
from src.news_pipeline import run_pipeline


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI News Intelligence",
    page_icon="📰",
    layout="wide"
)


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

st.sidebar.title("AI News Intelligence")

page = st.sidebar.radio(
    "Navigation",
    ["News Classifier", "News Dashboard"]
)


# --------------------------------------------------
# Page 1: Manual news classification
# --------------------------------------------------

if page == "News Classifier":

    st.title("AI News Classifier")

    st.write(
        "Enter a news headline or article to classify it "
        "as World, Sports, Business, or Sci/Tech."
    )

    st.caption(
        "Powered by a fine-tuned DistilBERT model "
        "trained on the AG News dataset."
    )

    news_text = st.text_area(
        "News text",
        placeholder="Enter a news headline or article...",
        height=180
    )

    if st.button("Classify", type="primary"):

        if news_text.strip():

            with st.spinner("Classifying news..."):
                result = predict_news(news_text)

            st.subheader("Prediction")
            st.success(result["prediction"])

            st.subheader("Category probabilities")

            sorted_probabilities = sorted(
                result["probabilities"].items(),
                key=lambda item: item[1],
                reverse=True
            )

            for category, probability in sorted_probabilities:
                st.write(f"**{category}: {probability:.2%}**")
                st.progress(float(probability))

            st.caption(
                "These scores represent model predictions, "
                "not verification of the news article."
            )

        else:
            st.warning("Please enter some news text.")

    with st.expander("About the model"):

        st.write(
            "This application uses a fine-tuned DistilBERT "
            "Transformer model for news classification."
        )

        st.write(
            "Official AG News test accuracy: **91.49%** "
            "across 7,600 unseen articles."
        )


# --------------------------------------------------
# Page 2: News analytics dashboard
# --------------------------------------------------

elif page == "News Dashboard":

    st.title("News Analytics Dashboard")

    st.write(
        "Explore news articles automatically collected "
        "from RSS feeds and classified using DistilBERT."
    )

    # ------------------------------------------
    # Refresh news button
    # ------------------------------------------

    if st.button("Refresh News", type="primary"):

        with st.spinner(
            "Fetching and classifying the latest news..."
        ):

            try:
                result = run_pipeline(limit=5)

                st.session_state["refresh_result"] = result

                st.rerun()

            except Exception as error:
                st.error(
                    f"News refresh failed: {error}"
                )

    # Show refresh result after rerun
    if "refresh_result" in st.session_state:

        result = st.session_state.pop("refresh_result")

        st.success(
            f"Refresh completed! "
            f"{result['classified']} articles classified, "
            f"{result['saved']} new articles saved."
        )

    # ------------------------------------------
    # Retrieve articles from SQLite
    # ------------------------------------------

    df = get_articles()

    if df.empty:

        st.info(
            "No articles found. Click Refresh News "
            "to collect the latest articles."
        )

    else:

        # ------------------------------------------
        # Category filters
        # ------------------------------------------

        categories = sorted(
            df["predicted_category"].dropna().unique()
        )

        selected_categories = st.multiselect(
            "Filter by predicted category",
            options=categories,
            default=categories
        )

        filtered_df = df[
            df["predicted_category"].isin(
                selected_categories
            )
        ].copy()

        # ------------------------------------------
        # Summary metrics
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total articles",
                len(filtered_df)
            )

        with col2:
            st.metric(
                "Categories",
                filtered_df[
                    "predicted_category"
                ].nunique()
            )

        with col3:

            average_confidence = (
                filtered_df["confidence"].mean()
                if not filtered_df.empty
                else 0
            )

            st.metric(
                "Average model score",
                f"{average_confidence:.2%}"
            )

        st.divider()

        # ------------------------------------------
        # Category distribution chart
        # ------------------------------------------

        st.subheader("News category distribution")

        category_counts = (
            filtered_df["predicted_category"]
            .value_counts()
        )

        if not category_counts.empty:

            st.bar_chart(
                category_counts
            )

        else:

            st.info(
                "No articles match the selected filters."
            )

        st.divider()

        # ------------------------------------------
        # Collected articles table
        # ------------------------------------------

        st.subheader("Collected news articles")

        display_df = filtered_df.copy()

        display_df["confidence"] = (
            display_df["confidence"] * 100
        ).round(2)

        display_df = display_df.rename(
            columns={
                "title": "Title",
                "source": "Source",
                "predicted_category": "Prediction",
                "confidence": "Model Score (%)",
                "published": "Published",
                "collected_at": "Collected At",
                "link": "Article Link"
            }
        )

        st.dataframe(
            display_df[
                [
                    "Title",
                    "Source",
                    "Prediction",
                    "Model Score (%)",
                    "Published",
                    "Article Link"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Article Link": st.column_config.LinkColumn(
                    "Article",
                    display_text="Read Article"
                )
            }
        )

        st.caption(
            "Article categories are predicted by DistilBERT "
            "and may differ from the publishers' categories. "
            "The average model score represents prediction "
            "confidence, not classification accuracy."
        )
