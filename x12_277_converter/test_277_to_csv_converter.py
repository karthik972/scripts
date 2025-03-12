import unittest
from unittest.mock import mock_open, patch
from x12_277_to_csvconverter import parse_277_file

class TestX12277Parser(unittest.TestCase):

    # def setUp(self):
#         # Sample 277 response file content
#         self.sample_277_content = """NM1*PR*2*InsuranceCompanyName~  
# NM1*41*2*SubmitterName*****46*123456789~  
# NM1*1P*2*ProviderName*****XX*9876543210~  
# NM1*IL*1*Doe*John****MI*123456789~  
# TRN*1*000123456~  
# STC*E0:33*20250307**100*0~  
# REF*EJ*ABC123456~  
# DTP*472*D8*20250307~  
# SE*9*0001~"""

    sample_277_response =  """
    ISA*00*          *00*          *01*030240928      *ZZ*AV09311993     *250307*1445*^*00501*013724300*0*T*:~
    GS*HN*030240928*AV01101957*20250307*1445*560440*X*005010X212~
    ST*277*1001*005010X212~
    BHT*0010*08*000000001*20250307*1439442*DG~
    HL*1**20*1~
    NM1*PR*2*BCBSMN*****PI*725~
    PER*IC**TE*8006762583~
    HL*2*1*21*1~
    NM1*41*2*OFFICEALLY*****46*HDF3F0313~
    HL*3*2*19*1~
    NM1*1P*2*DAIYA HEALTHCARE PLLC*****XX*1477027381~
    HL*4*3*22*0~
    NM1*IL*1*BRUNNER*****MI*19535060~
    TRN*2*3745448723~
    STC*E0:33*20250307**100*0~
    REF*EJ*11481741~
    DTP*472*RD8*20250210-20250210~
    SE*16*1001~
    GE*1*560440~
    IEA*1*013724300~"""
    
    @patch("builtins.open", new_callable=mock_open, read_data=sample_277_response)
    def test_parse_277_file(self, mock_file):
        result = parse_277_file("fake_path.277")

        expected_result = [{'payer_name': 'BCBSMN',
                            'payer_contact': '8006762583',
                            'submitter_name': 'OFFICEALLY',
                            'submitter_id': 'HDF3F0313',
                            'provider_name': 'DAIYA HEALTHCARE PLLC',
                            'provider_npi': '1477027381',
                            'patient_last_name': 'BRUNNER',
                            'patient_first_name': '',
                            'member_id': '19535060',
                            'claim_id': '3745448723',
                            'status_code': 'E0:33',
                            'status_description': 'Claim_Rejected',
                            'status_date': '20250307',
                            'claim_amount': '100',
                            'paid_amount': '0',
                            'reference_number': '11481741',
                            'service_from_date': '20250210',
                            'service_to_date': '20250210'}]

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
