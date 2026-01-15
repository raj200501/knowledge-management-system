import argparse
import json

from naive_bayes import predict_naive_bayes


def main():
    parser = argparse.ArgumentParser(description="Run text classification")
    parser.add_argument("--model", required=True, help="Model JSON path")
    parser.add_argument("--text", required=True, help="Text to classify")
    args = parser.parse_args()

    with open(args.model, "r", encoding="utf-8") as handle:
        model = json.load(handle)

    label = predict_naive_bayes(model, args.text)
    print(json.dumps({"label": label, "text": args.text}, indent=2))


if __name__ == "__main__":
    main()
