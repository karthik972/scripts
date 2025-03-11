import os
import csv
import argparse
import datetime

def parse_277_file(file_path):
    """Parses a 277 response file and extracts detailed claim information."""
    claims = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    current_claim = {}
    
    for line in lines:
        segments = line.strip().split("*")
        segment_id = segments[0]

        if segment_id == "NM1":
            entity_type = segments[1]
            if entity_type == "PR":
                current_claim["payer_name"] = segments[3] if len(segments) > 3 else ""
            elif entity_type == "41":
                current_claim["submitter_name"] = segments[3] if len(segments) > 3 else ""
                current_claim["submitter_id"] = segments[9] if len(segments) > 9 else ""
            elif entity_type == "1P":
                current_claim["provider_name"] = segments[3] if len(segments) > 3 else ""
                current_claim["provider_npi"] = segments[9] if len(segments) > 9 else ""
            elif entity_type == "IL":
                current_claim["patient_last_name"] = segments[3] if len(segments) > 3 else ""
                current_claim["patient_first_name"] = segments[4] if len(segments) > 4 else ""
                current_claim["member_id"] = segments[9] if len(segments) > 9 else ""

        elif segment_id == "TRN":
            current_claim["claim_id"] = segments[2]

        elif segment_id == "STC":
            current_claim["status_code"] = segments[1]
            current_claim["status_date"] = segments[2] if len(segments) > 2 else ""
            current_claim["claim_amount"] = segments[3] if len(segments) > 3 else ""
            current_claim["paid_amount"] = segments[4] if len(segments) > 4 else ""

        elif segment_id == "REF" and segments[1] == "EJ":
            current_claim["reference_number"] = segments[2]

        elif segment_id == "DTP" and segments[1] == "472":
            current_claim["service_from_date"] = segments[3] if len(segments) > 3 else ""
            current_claim["service_to_date"] = segments[4] if len(segments) > 4 else ""

        elif segment_id == "PER":
            current_claim["payer_contact"] = segments[4] if len(segments) > 4 else ""

        # When all required data is collected, save it and start a new claim
        if "status_code" in current_claim:
            claims.append(current_claim)
            current_claim = {}

    return claims

def write_csv(claims, output_folder):
    """Writes the extracted claims to a CSV file with a unique timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f"claim_status_{timestamp}.csv")

    os.makedirs(output_folder, exist_ok=True)

    fieldnames = [
        "claim_id", "payer_name", "payer_contact", "submitter_name", "submitter_id",
        "provider_name", "provider_npi", "patient_last_name", "patient_first_name",
        "member_id", "reference_number", "service_from_date", "service_to_date", "status_code", "status_date",
        "claim_amount", "paid_amount"
    ]

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(claims)

    print(f"CSV file saved: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert 277 response files to CSV.")
    parser.add_argument("input_files", nargs="+", help="List of 277 response files")
    parser.add_argument("output_folder", help="Output folder to store CSV files")

    args = parser.parse_args()

    all_claims = []
    for file_path in args.input_files:
        if os.path.exists(file_path):
            claims = parse_277_file(file_path)
            all_claims.extend(claims)
        else:
            print(f"Warning: File not found - {file_path}")

    if all_claims:
        write_csv(all_claims, args.output_folder)
    else:
        print("No valid claims found.")

if __name__ == "__main__":
    main()
