import pandas as pd

def generate_x12_276(csv_file, output_x12_file):
    # Read CSV file
    df = pd.read_csv(csv_file)

    # Open output file for writing
    with open(output_x12_file, "w") as f:
        for _, row in df.iterrows():
            isa_segment = f"ISA*00*          *00*          *ZZ*{row['sender_id']}       *ZZ*{row['receiver_id']}     *240101*1234*U*00401*000000001*0*P*:~"
            gs_segment = f"GS*HN*{row['sender_id']}*{row['receiver_id']}*20240101*1234*1*X*005010X212~"
            bht_segment = "BHT*0010*13*10001234*20240101*1234~"

            hl1 = "HL*1**20*1~"  # Information Source (Payer)
            nm1_payer = f"NM1*PR*2*{row['payer_name']}*****PI*{row['payer_id']}~"

            hl2 = "HL*2*1*21*1~"  # Information Receiver (Provider)
            nm1_provider = f"NM1*41*2*{row['provider_name']}*****46*{row['provider_id']}~"

            hl3 = "HL*3*2*19*1~"  # Subscriber
            nm1_subscriber = f"NM1*IL*1*{row['subscriber_last']}*{row['subscriber_first']}****MI*{row['subscriber_id']}~"

            hl4 = "HL*4*3*22*0~"  # Claim Level
            trn = f"TRN*1*{row['trace_number']}~"
            ref = f"REF*D9*{row['claim_number']}~"
            dtp = f"DTP*472*D8*{row['service_date']}~" #should this segment have start date and end date or only one data?? 

            se_segment = f"SE*{8}*1~"  # Is the segment number 8 fixed?
            ge_segment = "GE*1*1~"
            iea_segment = "IEA*1*000000001~"

            x12_content = f"{isa_segment}{gs_segment}{bht_segment}{hl1}{nm1_payer}{hl2}{nm1_provider}{hl3}{nm1_subscriber}{hl4}{trn}{ref}{dtp}{se_segment}{ge_segment}{iea_segment}\n"

            f.write(x12_content)

    print(f"X12 276 file generated: {output_x12_file}")

# Example usage
generate_x12_276("input_csv/claims.csv", "output_x12/output_276.x12")
