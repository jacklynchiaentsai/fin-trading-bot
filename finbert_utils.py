from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple

device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["postitive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors = "pt", padding=True).to(device)
        # logits represent raw scores for each class in the sentiment classification task
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        # convert raw scores into probabilities using softmax
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probabilty = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probabilty, sentiment
    else:
        return 0, labels[-1]

# testing
# checks if python script being run is the main program or if it is being improted as a module to another script
if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(['markets responded negatively to the news!', 'traders were displeased'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())