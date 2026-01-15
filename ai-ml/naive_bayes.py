import math
from collections import Counter, defaultdict


def tokenize(text):
    return [token.lower() for token in text.split() if token.strip()]


def train_naive_bayes(texts, labels):
    class_counts = Counter(labels)
    word_counts = defaultdict(Counter)
    vocabulary = set()

    for text, label in zip(texts, labels):
        tokens = tokenize(text)
        vocabulary.update(tokens)
        word_counts[label].update(tokens)

    vocabulary = sorted(vocabulary)
    model = {
        "class_counts": {str(label): count for label, count in class_counts.items()},
        "word_counts": {str(label): dict(counter) for label, counter in word_counts.items()},
        "vocab": vocabulary,
        "total_docs": len(labels),
    }
    return model


def predict_naive_bayes(model, text):
    tokens = tokenize(text)
    classes = [int(label) for label in model["class_counts"].keys()]
    vocab = set(model["vocab"])
    word_counts = {int(label): Counter(model["word_counts"][str(label)]) for label in model["word_counts"]}

    scores = {}
    for label in classes:
        class_count = model["class_counts"][str(label)]
        log_prob = math.log(class_count / model["total_docs"])
        total_words = sum(word_counts[label].values())
        for token in tokens:
            if token not in vocab:
                continue
            token_count = word_counts[label].get(token, 0)
            log_prob += math.log((token_count + 1) / (total_words + len(vocab)))
        scores[label] = log_prob

    return max(scores, key=scores.get)
