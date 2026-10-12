# AI News Intelligence — DistilBERT News Classification

An end-to-end machine learning project that classifies news articles using a fine-tuned DistilBERT model. The application also collects news from RSS feeds, stores predictions in a database, and provides an interactive dashboard for exploring the results.

I started this project by comparing traditional machine learning and neural network approaches for text classification. I later extended it into a news intelligence application that can collect, classify, and organise news articles automatically.

## Features

- **News classification:** Classifies headlines and text into World, Sports, Business, and Sci/Tech.
- **DistilBERT model:** Uses a fine-tuned Transformer model trained on the AG News dataset.
- **RSS integration:** Collects recent articles from BBC World, Business, and Technology feeds.
- **Automated pipeline:** Processes collected headlines and predicts their categories.
- **Duplicate prevention:** Skips articles that have already been saved.
- **SQLite database:** Stores headlines, sources, article links, predictions, and confidence scores.
- **Analytics dashboard:** Displays category distribution, article counts, filters, and prediction scores.
- **Manual classification:** Allows users to enter their own news text.
- **News refresh:** Provides a button to collect and classify new articles directly from the dashboard.
- **Hourly scheduler:** Supports automatic news collection at hourly intervals while the scheduler is running.

## Model Development

The project began with experiments using TF-IDF features and traditional machine learning models. I then explored neural networks before fine-tuning DistilBERT.

The dataset used for training and evaluation was **AG News**, which contains four news categories.

### Model Performance

| Model | Validation Accuracy |
|---|---:|
| TF-IDF + Logistic Regression | 91.90% |
| TF-IDF + Neural Network | 92.28% |
| Learned Embedding Neural Network | 92.15% |
| Fine-tuned DistilBERT | 92.10% |

The fine-tuned DistilBERT model achieved **91.49% accuracy on the official AG News test set of 7,600 articles**.

The learned embedding neural network achieved 91.75% test accuracy. Although DistilBERT did not outperform that model in this experiment, it provided an opportunity to work with Transformer fine-tuning, tokenisation, PyTorch inference, and model integration.

## Technologies Used

| Area | Technologies |
|---|---|
| Programming | Python |
| Machine Learning | Scikit-learn, PyTorch |
| NLP | Hugging Face Transformers, DistilBERT |
| Data Processing | Pandas |
| News Collection | Feedparser, BBC RSS |
| Database | SQLite |
| Web Application | Streamlit |
| Scheduling | APScheduler |
| Version Control | Git, GitHub |

## How the Application Works

The application has two main sections.

### 1. News Classifier

Users can enter a news headline or article into the application.

The text is processed by the fine-tuned DistilBERT model, which predicts one of four news categories and returns a probability score for each category.

### 2. News Analytics Dashboard

The dashboard displays news articles collected from BBC RSS feeds.

Users can:

- View the number of saved articles.
- Explore the distribution of predicted categories.
- Filter articles by category.
- Review model prediction scores.
- Open original news articles.
- Refresh the news collection manually.

The application also includes a separate scheduler that can run the collection pipeline every hour.

### News Processing Pipeline

1. Retrieve articles from the configured RSS feeds.
2. Check for duplicate article links.
3. Skip articles already stored in SQLite.
4. Classify new headlines using DistilBERT.
5. Save predictions and article information.
6. Display the saved results in Streamlit.

This approach avoids repeatedly classifying articles that have already been processed.

## Project Structure

```text
ai-text-classifier/
├── app.py
├── src/
│   ├── predict.py
│   ├── news_collector.py
│   ├── news_pipeline.py
│   ├── database.py
│   └── scheduler.py
├── models/
│   └── distilbert_agnews/
├── data/
│   └── news.db
├── requirements.txt
├── .gitignore
└── README.md
```

The structure above highlights the main application components. The repository also contains code used during model development and experimentation.

The trained model files and local SQLite database are excluded from GitHub.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Zobair2345/ai-text-classifier.git
cd ai-text-classifier
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Set up the trained model

The application currently expects the fine-tuned model and tokenizer files inside:

```text
models/distilbert_agnews/
```

These files are not included in the GitHub repository, so they must be provided separately before running inference.

### 5. Start the web application

```bash
python -m streamlit run app.py
```

Open the local address shown in the terminal, usually:

```text
http://localhost:8501
```

### 6. Run the news collection pipeline

```bash
python -m src.news_pipeline
```

This collects recent RSS articles, classifies new headlines, and stores their results in SQLite.

### 7. Start hourly collection

```bash
python -m src.scheduler
```

The scheduler runs an initial collection and then checks for new articles every hour.

The terminal must remain running, and the computer must stay awake for scheduled jobs to execute.

**Note:** On some macOS installations, HTTPS certificate configuration may be required to access RSS feeds.

## Current Limitations

The project is currently designed to run locally.

- The trained model weights are not yet hosted publicly.
- The SQLite database is stored locally.
- The scheduler only runs while its Python process is active.
- News classification is based on RSS headlines rather than full article content.
- Model confidence scores do not represent verified classification accuracy or news credibility.
- The model was evaluated on AG News, so performance on current BBC headlines may differ.

## Future Improvements

The next stage is to make the application accessible online.

Planned improvements include:

- Hosting the trained DistilBERT model on Hugging Face Hub.
- Deploying the Streamlit application.
- Adding persistent cloud database storage.
- Running news collection through a cloud-based scheduled job.
- Expanding the number of news sources.
- Improving dashboard visualisations and historical trends.
- Exploring article summarisation and more advanced NLP features.

## What I Learned

This project helped me understand how a machine learning model can become part of a complete application rather than remaining inside a notebook.

I gained practical experience with text preprocessing, model comparison, Transformer fine-tuning, inference pipelines, external data collection, database integration, automation, and interactive visualisation.

It also helped me understand that a more complex model does not automatically guarantee better performance, which became clear when comparing DistilBERT against the simpler embedding-based neural network.

## Author

**Zobair Abdullah**

Bachelor of Computer Science — Big Data and AI

GitHub: https://github.com/Zobair2345