import argparse
import json
import os


def load_csv(path):
    texts = []
    labels = []
    with open(path, "r", encoding="utf-8") as handle:
        header = handle.readline()
        for line in handle:
            if not line.strip():
                continue
            parts = line.strip().split(",", 1)
            if len(parts) != 2:
                continue
            text = parts[0].strip().strip('"')
            label = int(parts[1].strip())
            texts.append(text)
            labels.append(label)
    return texts, labels


def split_data(texts, labels, ratio=0.8):
    split_idx = int(len(texts) * ratio)
    return (
        texts[:split_idx],
        texts[split_idx:],
        labels[:split_idx],
        labels[split_idx:],
    )


def main():
    parser = argparse.ArgumentParser(description="Preprocess CSV data")
    parser.add_argument("--input", required=True, help="CSV input path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    texts, labels = load_csv(args.input)
    x_train, x_test, y_train, y_test = split_data(texts, labels)

    payload = {
        "train": list(zip(x_train, y_train)),
        "test": list(zip(x_test, y_test)),
    }

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(f"Wrote split dataset to {args.output}")


if __name__ == "__main__":
    main()
