import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = "models/distilbert_agnews"

LABELS = [
    "World",
    "Sports",
    "Business",
    "Sci/Tech"
]


# Select the best available device
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


# Load our fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()

def predict_news(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )[0]

    predicted_index = torch.argmax(
        probabilities
    ).item()

    results = {
        label: probability.item()
        for label, probability in zip(
            LABELS,
            probabilities
        )
    }

    return {
        "prediction": LABELS[predicted_index],
        "probabilities": results
    }

if __name__ == "__main__":
    text = "The football team won the championship after scoring two goals."

    result = predict_news(text)

    print(result)