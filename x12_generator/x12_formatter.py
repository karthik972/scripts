from jinja2 import Template
from datetime import datetime

# Constants
DEFAULT_SENDER_ID = "AV09311993"
DEFAULT_RECEIVER_ID = "030240928"

# Interchange segment header template
ISA_TEMPLATE = """ISA*00*          *00*          *ZZ*{{ sender_id }}       *ZZ*{{ receiver_id }}     *{{ now.strftime('%y%m%d') }}*{{ now.strftime('%H%M')}}*^*00501*{{ interchange_control_number }}*0*P*:~"""

# Functional group segment header template
GS_TEMPLATE = """GS*HN*{{ sender_id }}*{{ receiver_id }}*{{ now.strftime('%Y%m%d') }}*{{ now.strftime('%H%M') }}*1*X*005010X212~"""

# Transaction set segment
ST_TEMPLATE = """ST*276*{{ transaction_control_number }}*005010X212~
BHT*0010*13*{{ transaction_control_number }}*{{ service_from_dt.replace('/', '') }}*1234~
HL*1**20*1~
NM1*PR*2*TDB*****PI*{{ info_source_last_nm }}~
HL*2*1*21*1~
NM1*41*2*{{ info_source_last_nm }}*****46*{{ transaction_set_submitter_id }}~
HL*3*2*19*1~
NM1*1P*2*{{ last_nm }}*****FI*{{ provider_id_type_xx }}~
NM1*1P*2*{{ last_nm }}*****XX*{{ provider_id_type_ei }}~
HL*4*3*22*0~
DMG*D8*{{ patient_dob }}*TBD~
NM1*IL*1*{{ patient_last_nm }}*{{ patient_first_nm }}****MI*{{ subscriber_member_id }}~
TRN*1*{{ in_trace_id1 }}~
REF*EJ*{{ patient_control_num }}~
AMT*T3*TBD~
DTP*472*RDB*{{ service_from_dt.replace('/', '') }}-{{ service_to_dt.replace('/', '') }}~
SE*17*{{ transaction_control_number }}~"""

# Group segment footer template
GE_TEMPLATE = """GE*{{ num_st_segments }}*1~"""

# Interchange segment footer template
IEA_TEMPLATE = """IEA*1*{{ interchange_control_number }}~"""

def generate_x12_276(records, created_time, interchange_control_number):
    """Generates an X12 276 content with a single ISA, GS, and multiple ST segments per batch."""

    # Create ISA segment
    isa_template = Template(ISA_TEMPLATE)
    isa_segment = isa_template.render(sender_id=DEFAULT_SENDER_ID, receiver_id=DEFAULT_RECEIVER_ID, now=created_time, interchange_control_number=interchange_control_number)

    # Create GS segment
    gs_template = Template(GS_TEMPLATE)
    gs_segment = gs_template.render(sender_id=DEFAULT_SENDER_ID, receiver_id=DEFAULT_RECEIVER_ID, now=created_time)

    # Create st_segment for each row
    st_template = Template(ST_TEMPLATE)
    st_segments = []
    for i, record in enumerate(records, start=1):
        record["transaction_control_number"] = i  # Assign unique ST number
        st_segments.append(st_template.render(record))
    
    # create ge segment
    st_count = len(st_segments)
    ge_template = Template(GE_TEMPLATE)
    ge_segment = ge_template.render(num_st_segments=st_count)

    # create iea segment
    iea_template = Template(IEA_TEMPLATE)
    iea_segment = iea_template.render(interchange_control_number=interchange_control_number)

    return f"{isa_segment}\n{gs_segment}\n\n" + "\n\n".join(st_segments) + f"\n\n{ge_segment}\n{iea_segment}\n"