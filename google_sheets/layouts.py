from dataclasses import dataclass
from typing import Dict


@dataclass
class SheetLayout():
    sheet_name: str
    cell_addresses: Dict[str, str]


amazon_layout = SheetLayout(
    sheet_name='amz_advertising_access',
    cell_addresses={
        'AmzAccount_ID_Internal': 'B1:1',
        'AmzAccount_Name': 'B2:2',
        'AmzAccount_Group': 'B3:3',
        'AmzDeveloper_ClientID': 'B4:4',
        'AmzDeveloper_ClientSecret': 'B5:5',
        'AmzAccount_API_Advert_RefreshToken': 'B6:6',
        'ReportType': 'B7:7',
        'CountryCode': 'B8:8',
        'ReportStartDate': 'B9:9',
        'ReportEndDate': 'B10:10',
    }
)

db_layout = SheetLayout(
    sheet_name='db_access',
    cell_addresses={
        'server': 'B1',
        'database': 'B2',
        'user': 'B3',
        'password': 'B4',
        'use_trusted_connection': 'B5',
    }
)
