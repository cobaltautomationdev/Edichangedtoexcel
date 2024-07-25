import streamlit as st

def parse_edi_file_sln(section):
    lines = section.split('\n')
    slns = []
    current_pid_list = []
    prev_sln = None

    beg_info = {}
    ref_info = {}
    ctp_info = {}
    dtm_info = []
    n1_info = []
    po1_info = {}
    po4_info = {}
    po4_info_list=[]
    current_sln={}
    
    for line in lines:
        segments = line.strip().split('*')
        if segments[0] == 'BEG':
            beg_info = {'BEG': {'PO#': segments[3]}}
            if prev_sln:
                prev_sln['PID']=current_pid_list.copy()
            prev_sln = None
    
        elif segments[0] == 'REF':
            ref_info = {'REF': {'REF': segments[2]}}

        elif segments[0] == 'CTP':
            ctp_info = {'CTP': {'RES': segments[3]}}
            if prev_sln:
                prev_sln.update(ctp_info)
            
        elif segments[0] == 'DTM':
            dtm_info.append({'DTM': {'Date': segments[2]}})
        
        elif segments[0] == 'N1':
            n1_info.append({'N1': {'Name': segments[2]}})
            
        elif segments[0] == 'PO1':
            po1_info={'Cases_per_Prepack': segments[2],
                        'MASTER_UPC': segments[7], }
            
        elif segments[0] == 'PO4':
            po4_info={'Qty(UOM)per_1_inner_pack': segments[1],
                        'Pack_Qty(UOM)per_carton': "", }
            po4_info_list.append(po4_info)
            
        elif segments[0] == 'SLN':
            if dtm_info: 
                dtm_dates = [dct['DTM']['Date'] for dct in dtm_info]
                # start_date, end_date = [dct['DTM']['Date'] for dct in dtm_info]
                start_date, end_date = (dtm_dates[0], dtm_dates[1]) if len(dtm_dates) >= 2 else (None, None)
                dtm_dict = {'Start_Date': start_date, 'End_Date': end_date}
            if n1_info:
                MF,MP=[dct['N1']['Name'] for dct in n1_info]
                n1_dict = {'Vendor_Name': MF, 'Factory_Name':MP}
                
            po_line_num = segments[1]
            quantity = segments[4]
            unit_price = segments[6]
            upc = segments[10]
            style = segments[12]
            NRF_Color_Code = segments[16]
            NRF_Size_Code = segments[18]
            Class_Number = segments[14][3:5]
            Subclass_Number = segments[14][5:7]
            
            current_sln = {
                **beg_info,
                **ref_info,
                **dtm_dict,
                **n1_dict,
                **po1_info,
                # **po4_info,
                'SLN': {
                    'line_number': po_line_num,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'upc': upc,
                    'style': style,
                    'NRF_Color_Code': NRF_Color_Code,
                    'NRF_Size_Code': NRF_Size_Code,
                    'Class_Number': Class_Number,
                    'Subclass_Number': Subclass_Number,
                },
                'PID': [], 
            }
            
            slns.append(current_sln)
            
            beg_info = {}
            ref_info = {}
            # ctp_info = {}
            dtm_info = []
            n1_info = []
            po1_info = {}
            # po4_info = {}

            if prev_sln:
                prev_sln['PID']=current_pid_list.copy()
                current_pid_list=[]
            
        elif segments[0] == 'PID':
            pid = segments[5]
            if '-' not in pid:
                current_pid_list.append({'PID': pid}) 
        
        prev_sln = current_sln  
        if prev_sln:
                prev_sln['PID']=current_pid_list.copy()    
    for i, po4_info in enumerate(po4_info_list):
        if i < len(slns):
            slns[i].update(po4_info)            
    return slns              


def parse_edi_file_no_sln(section):
    lines = section.split('\n')
    slns = []
    current_pid_list = []
    prev_sln = None

    beg_info = {}
    ref_info = {}
    ctp_info = {}
    dtm_info = []
    n1_info = []
    po1_info = {}
    po4_info = {}
    po4_info_list = []
    current_sln={}
    
    for line in lines:
        segments = line.strip().split('*')
        if segments[0] == 'BEG':
            beg_info = {'BEG': {'PO#': segments[3]}}
            if prev_sln:
                prev_sln['PID']=current_pid_list.copy()
            prev_sln = None
    
        elif segments[0] == 'REF':
            ref_info = {'REF': {'REF': segments[2]}}

        elif segments[0] == 'CTP':
            ctp_info = {'CTP': {'RES': segments[3]}}
            if prev_sln:
                prev_sln.update(ctp_info)
            
        elif segments[0] == 'DTM':
            dtm_info.append({'DTM': {'Date': segments[2]}})
        
        elif segments[0] == 'N1':
            n1_info.append({'N1': {'Name': segments[2]}})
            
        elif segments[0] == 'PO4':
            po4_info={'Qty(UOM)per_1_inner_pack': segments[1],
                        'Pack_Qty(UOM)per_carton': segments[2], }
            po4_info_list.append(po4_info)

        elif segments[0] == 'PO1':
            if dtm_info:
                dtm_dates = [dct['DTM']['Date'] for dct in dtm_info]
                start_date, end_date = (dtm_dates[0], dtm_dates[1]) if len(dtm_dates) >= 2 else (None, None)
                # start_date, end_date = [dct['DTM']['Date'] for dct in dtm_info]
                dtm_dict = {'Start_Date': start_date, 'End_Date': end_date}
            if n1_info:
                MF,MP=[dct['N1']['Name'] for dct in n1_info]
                n1_dict = {'Vendor_Name': MF, 'Factory_Name':MP}

            po_line_num = segments[1]
            quantity = segments[2]
            unit_price = segments[4]
            upc = segments[7]
            style = segments[9]
            NRF_Color_Code = segments[13]
            NRF_Size_Code = segments[15]
            Class_Number = segments[11][3:5]
            Subclass_Number = segments[11][5:7]
            
            current_sln = {
                **beg_info,
                **ref_info,
                **dtm_dict,
                **n1_dict,
                **po1_info,
                # **po4_info,
                'SLN': {
                    'line_number': po_line_num,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'upc': upc,
                    'style': style,
                    'NRF_Color_Code': NRF_Color_Code,
                    'NRF_Size_Code': NRF_Size_Code,
                    'Class_Number': Class_Number,
                    'Subclass_Number': Subclass_Number,
                },
                'PID': [], 
            }
            
            slns.append(current_sln)
            beg_info = {}
            ref_info = {}
            dtm_info = []
            n1_info = []
            po1_info = {}
            # po4_info = {}

            if prev_sln:
                prev_sln['PID']=current_pid_list.copy()
                current_pid_list=[]
            
        elif segments[0] == 'PID':
            pid = segments[5]
            if '-' not in pid:
                current_pid_list.append({'PID': pid}) 
        
        prev_sln = current_sln  
        if prev_sln:
                prev_sln['PID']=current_pid_list.copy()  
        
    for i, po4_info in enumerate(po4_info_list):
        if i < len(slns):
            slns[i].update(po4_info)   
    return slns              

import pandas as pd
def edi_file_to_df(slns,has_sln:bool):
    rows = []
    for sln_dict in slns:
        row_data = {}
        # 获取非SLN信息
        row_data['BEG_PO#'] = sln_dict.get('BEG', {}).get('PO#')
        row_data['REF_REF'] = sln_dict.get('REF', {}).get('REF')
        row_data['CTP_RES'] = sln_dict.get('CTP', {}).get('RES')
        # row_data['DTM_Date'] = sln_dict.get('DTM', {}).get('Date')
        row_data['Start_Date'] = sln_dict.get('Start_Date')
        row_data['End_Date'] = sln_dict.get('End_Date')
        row_data['Vendor_Name'] = sln_dict.get('Vendor_Name')
        row_data['Factory_Name'] = sln_dict.get('Factory_Name')
        
        row_data['N1_Name'] = sln_dict.get('N1', {}).get('Name')
        
        # if not has_sln:
        row_data['PO1_Cases_per_Prepack'] = sln_dict.get('Cases_per_Prepack')
        row_data['PO1_MASTER_UPC'] = sln_dict.get('MASTER_UPC')
        row_data['PO4_Qty(UOM)per_1_inner_pack'] = sln_dict.get('Qty(UOM)per_1_inner_pack')
        row_data['PO4_Pack_Qty(UOM)per_carton'] = sln_dict.get('Pack_Qty(UOM)per_carton')
        # else:
        #     row_data['PO1_Cases_per_Prepack'] = sln_dict.get('Cases_per_Prepack')
        #     row_data['PO1_MASTER_UPC'] = sln_dict.get('MASTER_UPC')

        # 获取SLN信息
        sln = sln_dict['SLN']
        row_data['SLN_line_number'] = sln['line_number']
        row_data['SLN_quantity'] = sln['quantity']
        row_data['SLN_unit_price'] = sln['unit_price']
        row_data['SLN_upc'] = sln['upc']
        row_data['SLN_style'] = sln['style']
        row_data['SLN_NRF_Color_Code'] = sln['NRF_Color_Code']
        row_data['SLN_NRF_Size_Code'] = sln['NRF_Size_Code']
        row_data['SLN_Class_Number'] = sln['Class_Number']
        row_data['SLN_Subclass_Number'] = sln['Subclass_Number']

        # 获取PID信息
        pid_list = sln_dict.get('PID', [])
        for i, pid_dict in enumerate(pid_list):
            pid_key = f'PID_PID_{i+1}'
            row_data[pid_key] = pid_dict['PID']

        rows.append(row_data)

    max_pids = max(len(pid_list) for sln_dict in slns for pid_list in [sln_dict.get('PID', [])])

    column_names = ['BEG_PO#', 'REF_REF','CTP_RES', 'Start_Date','End_Date','Vendor_Name', 'Factory_Name','PO1_Cases_per_Prepack', 'PO1_MASTER_UPC',
                    'PO4_Qty(UOM)per_1_inner_pack','PO4_Pack_Qty(UOM)per_carton','SLN_line_number', 'SLN_quantity', 'SLN_unit_price', 'SLN_upc', 'SLN_style', 
                    'SLN_NRF_Color_Code', 'SLN_NRF_Size_Code','SLN_Class_Number', 'SLN_Subclass_Number']
         
    for i in range(1, max_pids + 1):
        column_names.append(f"PID_PID_{i}")
        df = pd.DataFrame(rows, columns=column_names)
    return df


def extract_isase_sections(lines):
    sections = []
    current_section = []
    for line in lines:
        line = line.strip()
        if line.startswith('ISA'):
            if current_section: 
                sections.append('\n'.join(current_section))
            current_section = [line]
        elif line.startswith('SE'):
            current_section.append(line)
            sections.append('\n'.join(current_section))
            current_section = []
        else:
            current_section.append(line)
    if current_section:
        sections.append('\n'.join(current_section))
    return sections

def has_line_startswith_sln(section):
    lines = section.split('\n')
    for line in lines:
        if line.startswith('SLN'):
            return True
    return False


from tqdm import tqdm
import io
import zipfile

st.set_page_config(page_title="EDI to XLSX", layout="wide",page_icon="icon\cobalt_logo.png") 
st.sidebar.header("EDI transfer to XLSX")
    
with st.sidebar.form("TextSelectForm",clear_on_submit=True):
    uploaded_files  = st.file_uploader("Choose EDI file(s)",accept_multiple_files=True, type="txt")
    submit_button = st.form_submit_button("Text file to XLSX")


if submit_button and uploaded_files:
    excel_streams = []
    for uploaded_file in tqdm(uploaded_files):
        file_name = uploaded_file.name
        file_name = file_name.rsplit(".")[0]
        lines = [line.decode('utf-8') for line in uploaded_file.readlines()]
        sections = extract_isase_sections(lines)
        for idx, setcion in enumerate(sections):
            has_sln = has_line_startswith_sln(setcion) 
            if has_sln:
                slns = parse_edi_file_sln(setcion)
                df = edi_file_to_df(slns,has_sln)
                df.ffill(inplace=True)
                df['PO1_Cases_per_Prepack'] = df['PO1_Cases_per_Prepack'].astype(int)
                df['SLN_quantity'] = df['SLN_quantity'].astype(int)
                df['Order Qty'] = df['PO1_Cases_per_Prepack'] * df['SLN_quantity']  
            else:
                slns = parse_edi_file_no_sln(setcion)
                df = edi_file_to_df(slns,has_sln)
                df.ffill(inplace=True)
                df['Order Qty'] = df['SLN_quantity']
            po_no = df['BEG_PO#'].iloc[0]
            style_no = df['SLN_style'].iloc[0]
            
            outputxlsx = io.BytesIO()
            df.to_excel(outputxlsx, index=False)
            outputxlsx.seek(0)
            excel_streams.append((f'{file_name}_output_{po_no}_{style_no}_{idx+1}.xlsx', outputxlsx))   
                 
    outputzip = io.BytesIO()
    with zipfile.ZipFile(outputzip, mode='w') as zf:
         for filename, stream in excel_streams:
            zf.writestr(filename, stream.getvalue())
    outputzip.seek(0)
    st.download_button(label='Download ZIP File', data=outputzip, file_name=f'{file_name}.zip', mime='application/zip')
    
