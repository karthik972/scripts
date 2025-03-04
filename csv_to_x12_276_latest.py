import csv
from jinja2 import Template

# Constants for missing values
DEFAULT_GROUP_POLICY_NUM = "00000001"
DEFAULT_PATIENT_CONTROL_NUM = "UNKNOWN"
DEFAULT_RELATIONSHIP_CD = "18"
DEFAULT_PROVIDER_ID_TYPE_XX = "UNKNOWN"
DEFAULT_PROVIDER_ID_TYPE_EI = "UNKNOWN"
DEFAULT_SENDER_ID = "ABC123456"
DEFAULT_RECEIVER_ID = "XYZ789012"

# Jinja template for X12 276 output
X12_276_TEMPLATE = """
ISA*00*          *00*          *ZZ*{{ sender_id }}       *ZZ*{{ receiver_id }}     *{{ service_from_dt.replace('/', '') }}*1234*U*00401*000000001*0*P*:~
GS*HN*ABC123456*XYZ789012*{{ service_from_dt.replace('/', '') }}*1234*1*X*005010X212~
BHT*0010*13*{{ in_trace_id1 }}*{{ service_from_dt.replace('/', '') }}*1234~
HL*1**20*1~
NM1*PR*2*HealthPlan*****PI*123456.0~
HL*2*1*21*1~
NM1*41*2*{{ last_nm }}*****46*{{ provider_id_type_ei }}.0~
HL*3*2*19*1~
NM1*IL*1*{{ patient_last_nm }}*{{ patient_first_nm }}****MI*{{ subscriber_member_id }}~
HL*4*3*22*0~
TRN*1*TR{{ in_trace_id1 }}~
REF*D9*CLM{{ patient_control_num }}~
DTP*472*D8*{{ service_from_dt.replace('/', '') }}.0~
SE*8*1~
GE*1*1~
IEA*1*000000001~
"""

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    records = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append({
                "sender_id": row.get("sender_id", DEFAULT_SENDER_ID),
                "receiver_id": row.get("receiver_id", DEFAULT_RECEIVER_ID),
                "in_trace_id1": row.get("in_trace_id1", ""),
                "payer_id": row.get("payer_id", ""),
                "service_from_dt": row.get("service_from_dt", ""),
                "service_to_dt": row.get("service_to_dt", ""),
                "subscriber_member_id": row.get("subscriber_member_id", ""),
                "subscriber_first_nm": row.get("subscriber_first_nm", ""),
                "subscriber_last_nm": row.get("subscriber_last_nm", ""),
                "group_policy_num": row.get("group_policy_num", DEFAULT_GROUP_POLICY_NUM),
                "patient_control_num": row.get("patient_control_num", DEFAULT_PATIENT_CONTROL_NUM),
                "patient_last_nm": row.get("patient_last_nm", ""),
                "patient_first_nm": row.get("patient_first_nm", ""),
                "patient_dob": row.get("patient_dob", ""),
                "relationship_cd": row.get("relationship_cd", DEFAULT_RELATIONSHIP_CD),
                "last_nm": row.get("last_nm", ""),
                "provider_id_type_xx": row.get("provider_id_type_xx", DEFAULT_PROVIDER_ID_TYPE_XX),
                "provider_id_type_ei": row.get("provider_id_type_ei", DEFAULT_PROVIDER_ID_TYPE_EI),
                "transaction_set_submitter_id": row.get("transaction_set_submitter_id", ""),
                "info_source_last_nm": row.get("info_source_last_nm", "")
            })
    return records

def generate_x12_276(records, output_file):
    template = Template(X12_276_TEMPLATE)
    with open(output_file, mode='w', encoding='utf-8') as file:
        for record in records:
            file.write(template.render(record))
            file.write('\n')

def main():
    input_csv = "input_csv/claims-1.csv"
    output_x12_276 = "output_x12/output.x12"
    records = read_csv(input_csv)
    generate_x12_276(records, output_x12_276)
    print(f"X12 276 file generated: {output_x12_276}")

if __name__ == "__main__":
    main()
