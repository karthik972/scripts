import argparse
from datetime import datetime
from x12_generator.csv_reader import read_csv
from x12_generator.x12_formatter import generate_x12_276

def main():
    parser = argparse.ArgumentParser(description="Convert CSV to X12 276 format.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_folder", help="Folder the output X12 276 file")
    parser.add_argument("--batch_size", type=int, default=10, help="Number of records per batch")

    args = parser.parse_args()

    batch_number = 1
    for batch in read_csv(args.input_csv, args.batch_size):
        created_time = datetime.now()
        interchange_control_number = int(created_time.timestamp()) % 1000000000 + batch_number
        file_name = f"{args.output_folder}/X12_276_{interchange_control_number}.txt"
        with open(file_name, "w", encoding="utf-8") as out_file:
            x12_data = generate_x12_276(batch, created_time, interchange_control_number)
            out_file.write(x12_data + "\n")
            print(f"Conversion complete. X12 file saved to {out_file}")
        batch_number += 1

if __name__ == "__main__":
    main()