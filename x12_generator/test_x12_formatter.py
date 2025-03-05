import unittest
from datetime import datetime
from x12_formatter import generate_x12_276

class TestGenerateX12276(unittest.TestCase):
    def setUp(self):
        self.created_time = datetime(2025, 3, 5, 12, 30)
        self.interchange_control_number = "000000001"
        self.records_with_one_ST = [
            {
                "service_from_dt": "2025/03/01",
                "service_to_dt": "2025/03/01",
                "info_source_last_nm": "INSURANCE",
                "transaction_set_submitter_id": "SUB12345",
                "last_nm": "PROVIDER",
                "provider_id_type_xx": "1234567890",
                "provider_id_type_ei": "0987654321",
                "patient_dob": "19800101",
                "patient_last_nm": "DOE",
                "patient_first_nm": "JOHN",
                "subscriber_member_id": "A123456789",
                "in_trace_id1": "TR12345678",
                "patient_control_num": "PC987654321"
            }
        ]
        self.records_with_two_ST = [
            {
                "service_from_dt": "2025/03/01",
                "service_to_dt": "2025/03/01",
                "info_source_last_nm": "INSURANCE",
                "transaction_set_submitter_id": "SUB12345",
                "last_nm": "PROVIDER",
                "provider_id_type_xx": "1234567890",
                "provider_id_type_ei": "0987654321",
                "patient_dob": "19800101",
                "patient_last_nm": "DOE",
                "patient_first_nm": "JOHN",
                "subscriber_member_id": "A123456789",
                "in_trace_id1": "TR12345678",
                "patient_control_num": "PC987654321"
            },
            {
                "service_from_dt": "2025/03/01",
                "service_to_dt": "2025/03/01",
                "info_source_last_nm": "INSURANCE",
                "transaction_set_submitter_id": "SUB12345",
                "last_nm": "PROVIDER",
                "provider_id_type_xx": "1234567890",
                "provider_id_type_ei": "0987654321",
                "patient_dob": "19800101",
                "patient_last_nm": "DOE",
                "patient_first_nm": "JOHN",
                "subscriber_member_id": "A123456789",
                "in_trace_id1": "TR12345678",
                "patient_control_num": "PC987654321"
            }
        ]
    
    def test_generate_x12_276_for_1_ST(self):
        # from x12_generator import generate_x12_276
        
        x12_output = generate_x12_276(self.records_with_one_ST, self.created_time, self.interchange_control_number)
        
        # Check presence of key segments
        self.assertIn("ISA*00*", x12_output)
        self.assertIn("GS*HN*", x12_output)
        self.assertIn("ST*276*1*005010X212~", x12_output)  # Ensuring transaction control number starts from 1
        self.assertIn("GE*1*1~", x12_output)  # Ensuring 1 segment
        self.assertIn("IEA*1*000000001~", x12_output)  # Ensuring correct interchange control number
        
        # Check dynamic date values
        self.assertIn("250305", x12_output)  # '250305' corresponds to '2025-03-05' in %y%m%d format
        self.assertIn("1230", x12_output)  # '12:30' in %H%M format
        
        print("Generated X12 276 Output:\n", x12_output)

    def test_generate_x12_276_for_1_ST(self):
        # from x12_generator import generate_x12_276
        
        x12_output = generate_x12_276(self.records_with_two_ST, self.created_time, self.interchange_control_number)
        
        # Check presence of key segments
        self.assertIn("ISA*00*", x12_output)
        self.assertIn("GS*HN*", x12_output)
        self.assertIn("ST*276*1*005010X212~", x12_output)  # Ensuring transaction control number starts from 1
        self.assertIn("ST*276*1*005010X212~", x12_output)  # Ensuring second transaction set is present
        self.assertIn("GE*2*1~", x12_output)  # Ensuring 2 ST segments
        self.assertIn("IEA*1*000000001~", x12_output)  # Ensuring correct interchange control number
        
        # Check dynamic date values
        self.assertIn("250305", x12_output)  # '250305' corresponds to '2025-03-05' in %y%m%d format
        self.assertIn("1230", x12_output)  # '12:30' in %H%M format
        
        print("Generated X12 276 Output:\n", x12_output)

if __name__ == "__main__":
    unittest.main()
