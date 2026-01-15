import argparse
import json

from naive_bayes import train_naive_bayes
from data_preprocessing import load_csv


def main():
    parser = argparse.ArgumentParser(description="Train a naive Bayes classifier")
    parser.add_argument("--input", required=True, help="CSV dataset")
    parser.add_argument("--model", required=True, help="Output model path")
    args = parser.parse_args()

    texts, labels = load_csv(args.input)
    model = train_naive_bayes(texts, labels)

    with open(args.model, "w", encoding="utf-8") as handle:
        json.dump(model, handle, indent=2)

    print(f"Model saved to {args.model}")


if __name__ == "__main__":
    main()
