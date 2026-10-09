# AI News Classification System

This project is a news classification system that I built to explore different approaches to Natural Language Processing (NLP), starting with traditional machine learning and gradually moving towards neural networks and Transformer models.

The system classifies news articles into four categories:

- World
- Sports
- Business
- Sci/Tech

I used the AG News dataset for training and evaluation. The final version of the application uses a fine-tuned DistilBERT model and includes a simple Streamlit interface where users can enter their own news text and get a prediction.

---

## About the Project

I built this project step by step rather than starting directly with a Transformer model.

I first created a baseline using TF-IDF and Logistic Regression. I then experimented with neural networks using both TF-IDF features and learned word embeddings.

Finally, I moved to a pretrained Transformer and fine-tuned DistilBERT for the same classification task.

The project currently includes:

1. TF-IDF + Logistic Regression
2. TF-IDF + Neural Network
3. Word Embeddings + Neural Network
4. Fine-tuned DistilBERT
5. Streamlit web application

This allowed me to compare traditional NLP techniques with modern transfer-learning approaches while understanding how each model processes text differently.

---

## Models and Results

### TF-IDF + Logistic Regression

The first model uses TF-IDF to convert the news text into numerical features and Logistic Regression for classification.

Validation accuracy: **91.90%**

This provided a strong baseline despite being the simplest model in the project.

### TF-IDF + Neural Network

I then used the same TF-IDF features as input to a feed-forward neural network.

Validation accuracy: **92.28%**

This slightly improved the validation performance compared with Logistic Regression.

### Word Embeddings + Neural Network

For the next version, I moved away from manually generated TF-IDF features.

The model learns 64-dimensional word embeddings during training and uses global average pooling to create an article representation before classification.

Validation accuracy: **92.15%**

Official test accuracy: **91.75%**

This experiment helped me understand how learned word representations differ from TF-IDF features.

### Fine-Tuned DistilBERT

The final model uses DistilBERT, a pretrained Transformer model.

Instead of training a language model from scratch, I fine-tuned the pretrained model using a balanced sample of 8,000 AG News articles.

Validation accuracy: **92.10%**

Official test accuracy: **91.49%**

Official test loss: **0.2523**

Although DistilBERT did not produce the highest accuracy in this experiment, it achieved competitive performance using only 8,000 fine-tuning examples.

This was also an important part of the project because it introduced transfer learning and contextual word representations.

---

## DistilBERT Test Analysis

I evaluated the fine-tuned DistilBERT model on the official AG News test set containing 7,600 unseen articles.

| Category | Correct Predictions | Class Accuracy |
|---|---:|---:|
| World | 1,719 / 1,900 | 90.47% |
| Sports | 1,856 / 1,900 | 97.68% |
| Business | 1,684 / 1,900 | 88.63% |
| Sci/Tech | 1,694 / 1,900 | 89.16% |

Sports was the easiest category for the model to identify, with an accuracy of 97.68%.

The largest source of error was between Business and Sci/Tech. The model classified 158 Business articles as Sci/Tech and 160 Sci/Tech articles as Business.

This makes sense because these categories often overlap. For example, an article about a technology company launching a new product could contain both business and technology-related language.

---

## Web Application

After training and evaluating the models, I created a Streamlit application so that the classifier could be used outside of a Jupyter Notebook.

Users can enter a news headline or article, and the application:

- processes the text using the DistilBERT tokenizer
- sends the tokens through the fine-tuned model
- predicts one of the four news categories
- displays the confidence score for each category

For example:

**Input**

> Apple announced a new artificial intelligence platform for its devices.

**Prediction**

> Sci/Tech

The confidence values shown by the application are model outputs and should not be interpreted as fact-checking probabilities. The application classifies the topic of the text; it does not determine whether a news story is true or false.

---

## Technologies Used

The project uses:

- Python
- PyTorch
- Hugging Face Transformers
- TensorFlow / Keras
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Streamlit
- Jupyter Notebook
- Git and GitHub

---

## Project Structure

```text
ai-text-classifier/
│
├── app.py
│
├── notebooks/
│   ├── 01_tfidf_classification.ipynb
│   ├── 02_embedding_classification.ipynb
│   └── 03_bert_classification.ipynb
│
├── src/
│   └── predict.py
│
├── models/
│   └── distilbert_agnews/
│
├── data/
├── requirements.txt
├── .gitignore
└── README.md
```

The trained model files are currently excluded from the Git repository because of their size.

---

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/Zobair2345/ai-text-classifier.git
cd ai-text-classifier
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python -m streamlit run app.py
```

The fine-tuned DistilBERT weights are currently stored locally and are not included in the GitHub repository, so the application requires the trained model files to run.

---

## What I Learned

This project gave me practical experience with several stages of an NLP workflow.

I worked with TF-IDF, Logistic Regression, neural networks, word embeddings and Transformer models rather than focusing on only one approach.

Some of the main areas I worked with include:

- text preprocessing
- TF-IDF feature extraction
- multiclass classification
- neural networks for text classification
- learned word embeddings
- training and validation workflows
- overfitting and early stopping
- Transformer tokenization
- contextual embeddings
- transfer learning
- DistilBERT fine-tuning
- PyTorch inference
- model evaluation
- confusion matrices
- building reusable prediction code
- creating a simple ML application with Streamlit

One of the main things I learned from the project is that a more complex model does not automatically produce better results. Model performance also depends on the amount of training data, the task, computational requirements and how the model is trained.

---

## Next Steps

There are several areas I would like to explore further:

- fine-tuning DistilBERT using more of the AG News training dataset
- comparing other pretrained Transformer models
- improving confidence calibration
- deploying the Streamlit application online
- supporting batch classification
- creating an API for the classifier

---

## Author

**Zobair Abduallah**

Computer Science graduate, majoring in Big Data and Artificial Intelligence.

Currently continuing to build practical projects in machine learning, NLP, AI and LLM-based systems.