import os
import socket
import struct
import sys
import time
from time import *
from time import time

import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

global noOfResponses
import openpyxl
from openpyxl.styles import PatternFill
from Cryptodome.Cipher import AES

global noOfResponses
from datetime import datetime
import simplefix
import warnings

warnings.filterwarnings("ignore")
noOfResponses = int(2)
parser = simplefix.FixParser()
Env = sys.argv[1]
current_dir = os.getcwd()
#var2 = "\\Order_DQ_NFR"
#var2 = "\\ETI_UAT_Algo_10002.xlsx"
#var2 = "\\ETI_UAT_Algo_10004RND.xlsx"
#var2 = "\\new_Uat_file.xlsx"
var2 = "\\ETI_UAT_Algo_10003.xlsx"
File_path = r"{}{}".format(current_dir, var2)

if Env.upper() == "MAT" or Env.upper() == "MATA":
    print("MAT Env selected")
    ip_CG = '192.168.189.35'
    port_CG = 19106
    ip_SL = '192.168.189.35'
    port_SL = 19106
    MasterData_Path = File_path
    # password_key = b'Test@123450000000000000000000000'
    # password_iv = b'Test@1234500'
elif Env.upper() == "UAT":
    print("UAT Env selected")
    ip_CG = '192.168.190.40'
    port_CG = 19306
    ip_SL = '192.168.190.40'
    port_SL = 19306
    #MasterData_Path = File_path
elif Env.upper() == "NFR" or Env.upper() == "NFRA":
    print("NFR Env selected")
    ip_CG = '192.168.80.48'
    port_CG = 19006
    ip_SL = '192.168.80.48'
    port_SL = 19006
    MasterData_Path = File_path
    #password_key = b'Test@123450000000000000000000000'
    #password_iv = b'Test@1234500'

elif Env.upper() == "UAT2" or Env.upper() == "UAT2A":
    print("UAT Env selected")
    ip_CG = '192.168.190.201'
    port_CG = 19406
    ip_SL = '192.168.190.201'
    port_SL = 19406
    #MasterData_Path = r"C:\Users\ext-moinsh\Desktop\ETI_UAT_Algo_10004_AN.xlsx"
    MasterData_Path = File_path
    password_key = b'Mcx@5432100000000000000000000000'
    password_iv = b'Mcx@54321000'

elif Env.upper() == "MOCKDR" or Env.upper() == "MOCKDRA":
    print("MOCk Env selected")
    ip_CG = '192.168.73.48'
    port_CG = 19106
    ip_SL = '192.168.73.48'
    port_SL = 19106
   # MasterData_Path = File_path
elif Env.upper() == "MOCKDC" or Env.upper() == "MOCKDCA":
    print("MOCk Env selected")
    ip_CG = '192.168.63.48'
    port_CG = 19106
    ip_SL = '192.168.63.48'
    port_SL = 19106
# MasterData_Path = r"\\172.22.0.14\ext-home$\ext-ganeshko\Desktop\MAT Data\imp working with UAT-10002.xlsx"

sheetName_CG = 'All_login'  # GatewayConnection
sheetRow_CG = 1

sheetName_SL = 'All_login'  # SessionLogon
sheetRow_SL = 3

sheetName_UL = 'All_login'  # UserLogon
sheetRow_UL = 5

sheetName_Sub = 'All_login'  # Subscription
sheetRow_Sub = 7
sheetRow_Sub2 = 8
sheetRow_Sub3 = 9

sheetName_ULT = 'All_login'  # UserLogout
sheetRow_ULT = 11

sheetName_SLT = 'All_login'  # SessionLogout
sheetRow_SLT = 13

sheetName_hearbeat = 'All_login'  # heartbeat
sheetRow_heartbeat = 15


sheetName_Orderdata = 'Order_data'
sheetRow_orderdata = 0




"""--------Reading Data from CSV-------"""
# Reading Session Gateway Connection Data
df_CG = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_CG, engine='openpyxl')
rqstFields_CG = df_CG.loc[sheetRow_CG].iloc[2:14]
print(rqstFields_CG)

# Reading Session Logon Data
df_SL = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_SL, engine='openpyxl')
rqstFields_SL = df_SL.loc[sheetRow_SL].iloc[8:24]
rqstFields_SL_header = df_SL.loc[sheetRow_SL].iloc[2:8]
# Reading User Logon Data
df_UL = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_UL, engine='openpyxl')
rqstFields_UL = df_UL.loc[sheetRow_UL].iloc[8:12]
rqstFields_UL_header = df_UL.loc[sheetRow_UL].iloc[2:8]
# Reading Subscription Data
df_Sub = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Sub, engine='openpyxl')
rqstFields_sub_header= df_Sub.loc[sheetRow_Sub].iloc[2:8]
rqstFields_Sub = df_Sub.loc[sheetRow_Sub].iloc[8:11]

rqstFields_sub_header2= df_Sub.loc[sheetRow_Sub2].iloc[2:8]
rqstFields_Sub2 = df_Sub.loc[sheetRow_Sub2].iloc[8:11]

rqstFields_sub_header3= df_Sub.loc[sheetRow_Sub3].iloc[2:8]
rqstFields_Sub3 = df_Sub.loc[sheetRow_Sub3].iloc[8:11]


# Reading User Logout Data
df_ULT = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_ULT, engine='openpyxl')
rqstFields_ULT = df_ULT.loc[sheetRow_ULT].iloc[2:10]

# Reading Session Logout Data
df_SLT = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_SLT, engine='openpyxl')
rqstFields_SLT = df_SLT.loc[sheetRow_SLT].iloc[2:8]

# Reading Other API to be tested
df_OtherAPI = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Orderdata, engine='openpyxl')
rqstFields_OtherAPI = df_OtherAPI.loc[sheetRow_orderdata]

order_count =len(rqstFields_OtherAPI)

# Reading pack/unpack format data
# The index values other than for _OtherAPI here should not change as long as sequence in "sheetName_Format" and "sheetName_RespFields" do not change.
'''df_format = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name = sheetName_Format, engine = 'openpyxl')'''

format_Req_CG = "IH8s2sIII30s2sI32s344s"  # df_format.loc[0][0]
format_resp_CG = "IH2sQQI4sIIIIBB6s"  # df_format.loc[0][1]

format_session_login_header="IH8s2sII"
format_Req_SL = "III30s32sccc30s30s30s30s30s30s344s7s"  # df_format.loc[1][0]
format_resp_SL = "IH2sQQI4sqQIIIIIBBBB30s2s"  # df_format.loc[1][1]


format_user_login_header="IH8s2sII"
format_Req_UL = "II32s344s"  # df_format.loc[2][0]
format_resp_UL = "QQI4sQII"  # df_format.loc[2][1]

format_subscribe_header="IH8s2sII"
format_Req_Sub = "IB3s"  # df_format.loc[3][0] IH8s2sIIIB3s
format_resp_Sub = "IH2sQQI4sI4s"  # df_format.loc[3][1]

format_Req_ULT = "IH8s2sIII4s"  # df_format.loc[4][0]
format_resp_ULT = "IH2sQQI4s"  # df_format.loc[4][1]

format_Req_SLT = "IH8s2sII"  # df_format.loc[5][0]
format_resp_SLT = "IH2sQQI4s"  # df_format.loc[5][1]

format_Req_heartbeat = "IH8s2s"
format_resp_heartbeat = "IH2sQH6s40s"

new_order_qty = []
Modify_order_qty = []

new_order_header="IH8s2sII"
neworder_formattype_message = "qqQQQQQQIiqqIiIIH5s7s9sBBBBBBBBBBB2sc2s1s20s12s12s12s"
neworder_response_formattype = "IH2sQQQQQQIHB16sBQQQQQQQQQQIIHccHBB"


modify_order_header="IH8s2sII"
modifyorder_formattype = "QQQqqQQQQIiqqQQIiIIIH5s7s9sBBBBBBBBBB1s2s1s2s1s20s12s12s12s4s"
modifyorder_response_formattype = "IH2sQQQQQQIHB16sBQQQqQQqqQQQqqqIH1s1sHBB4s"

cancle_order_header="IH8s2sII"
cancleorder_formattype = "QQQQQQiiIII4s"
cancelorder_response_formattype = "QQQQQQIHB16sBQQQqQqq1s1sHB3s"

current_dir = os.getcwd()
now = datetime.now()
var2 = "_Report.xlsx"
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
excel_Report_Path = "{}\\Report\\{}{}".format(current_dir, dt_string, var2)

global z
z = 6
global yescount
yescount = 0
No_of_Res = 0
Order_Number = 0
neworderdata = []
modifyorderdata = [0] * 50
cancelorderdata = [0] * 50
multiorderresponse = []
orderno = []
Act_Response = []
non_persistent_orderno = []
user_id = []
templete_id_response = []
message_seq_no = []
TestCase_name_final = []
unique_ref_id=[]
all_response=[]


def excel_report2():
    print("inside report generation")
    wb_obj = openpyxl.load_workbook(excel_Report_Path)
    sheet_obj = wb_obj["Report"]
    print(len(non_persistent_orderno))
    for i in range(1, len(non_persistent_orderno)):
        userid = sheet_obj.cell(row=i + 1, column=1)
        orderno = sheet_obj.cell(row=i + 1, column=2)
        mesgseqno = sheet_obj.cell(row=i + 1, column=3)
        template_id = sheet_obj.cell(row=i + 1, column=4)
        userid.value = user_id[i]
        orderno.value = non_persistent_orderno[i]
        mesgseqno.value = message_seq_no[i]
        template_id.value = templete_id_response[i]
    wb_obj.save(excel_Report_Path)
    print("report ended")


def excel_report():
    print("inside report generation")
    wb_obj = openpyxl.Workbook(excel_Report_Path)
    wb_obj.save(excel_Report_Path)
    wb_obj = openpyxl.load_workbook(excel_Report_Path)
    sheet_obj = wb_obj.active
    wb_obj.create_sheet(index=0, title="Report")
    sheet_obj = wb_obj.active
    a, b, c = 0, 1, 2
    resp_dict = {}
    Order_num = list(set(non_persistent_orderno))
    #print(" len(non_persistent_orderno) -",len(non_persistent_orderno))
    conut = 0
    print(Act_Response)
    for i in range(0, len(Order_num)):
        ord = 0
        rep = []
        cmnt = []
        #print("template id responses count ",len(templete_id_response))

        for j in range(0, len(templete_id_response)-1 ):
            temp = Act_Response[j].split("-")
            if (temp[1] == str(Order_num[i])):
                ord = temp[1]
                rep.append(str(temp[0]))
                cmnt.append(str(temp[2]))
            #print("all comments ",cmnt)
        resp_dict[str(Order_num[i])] = rep
        test_case_name3 = sheet_obj.cell(row=i + 2, column=1)
        test_case_name4 = sheet_obj.cell(row=i + 2, column=2)
        userid = sheet_obj.cell(row=i + 2, column=3)
        # mesgseqno = sheet_obj.cell(row = i+2, column = 4)
        orderno = sheet_obj.cell(row=i + 2, column=4)
        template_id = sheet_obj.cell(row=i + 2, column=5)
        Comment = sheet_obj.cell(row=i + 2, column=6)
        print(len(TestCase_name_final), " - testcase length")
        test_case_name3.value = str(i + 1)
        test_case_name4.value = str(TestCase_name_final[i])#changed
        userid.value = str(user_id[i])#changes
        # mesgseqno.value =str(ord) #message_seq_no[i])
        orderno.value = str(Order_num[i])
        template_id.value = str(rep)
        Comment.value = str(cmnt)
        header1 = sheet_obj.cell(row=1, column=1)
        header2 = sheet_obj.cell(row=1, column=2)
        header3 = sheet_obj.cell(row=1, column=3)
        header4 = sheet_obj.cell(row=1, column=4)
        header5 = sheet_obj.cell(row=1, column=5)
        header6 = sheet_obj.cell(row=1, column=6)
        header7 = sheet_obj.cell(row=1, column=7)
        header8 = sheet_obj.cell(row=1, column=8)
        header9 = sheet_obj.cell(row=1, column=9)
        colour1 = PatternFill(patternType='solid', fgColor='00FFFFCC')
        header1.fill = colour1
        header2.fill = colour1
        header3.fill = colour1
        header4.fill = colour1
        header5.fill = colour1
        header6.fill = colour1
        header7.fill = colour1
        header8.fill = colour1
        header9.fill = colour1
        header1.value = "Sr_No"
        header2.value = "TestCase_name"
        header3.value = "userid"
        # header4.value = "mesgseqno"
        header4.value = "orderno"
        header5.value = "Responses"
        header6.value = "Comment"
    wb_obj.save(excel_Report_Path)
    print("report generated at path = ", excel_Report_Path)


def compare(a, b):
    if a.upper() == b.upper():
        result = "PASS"
    else:
        result = "Fail"
    return result


def CreatePayload(rqstFields_CP, format_CP):
    #print(rqstFields_CP)
    len_CP = len(rqstFields_CP)
    list_CP = []
    for i in range(len_CP):
        if (type(rqstFields_CP[i]) == str):
            temp = rqstFields_CP[i].replace("\\0", "\0")
            list_CP.append(temp.encode("utf-8"))
        else:
            list_CP.append(rqstFields_CP[i])
    bytestream_CP = struct.pack(format_CP, *list_CP)
    return bytestream_CP




def encryption(header ,message_body,key,iv):


    # Create AES-GCM cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

    # Encrypt the plaintext
    encrypted_text = cipher.encrypt(message_body)

    # Print the ciphertext
    #print("encrypted_text:", encrypted_text)

    byte_array = bytearray(encrypted_text)
    #print("Byte array:", byte_array)

    # Convert byte array to list of integers (byte values)
    byte_list = list(byte_array)
    #print("List of integers of encrypted msg:", byte_list)

    ciphertext_array = bytearray(encrypted_text)
    #print("List of integers of encrypted msg :",ciphertext_array)
    final_session_login_request = header + ciphertext_array

    return final_session_login_request

    # plaintext = bytes(byte_list)

def decryption(encryption_data,key,iv):

    encrypted_msg = encryption_data[0:]
    # Create an AES-GCM cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

    # Decrypt and authenticate the message
    decrypted_msg = cipher.decrypt(encrypted_msg)
    #print("Decrypted message:", decrypted_msg)

    return decrypted_msg





def Read_Response(sock ,key,iv):
    actul = " "
    Comment = " "
    heartbeat_counter = 0
    global noOfResponses
    global z
    Cncl_Ord = 0
    Ord_No = 0
    ij = 0
    NP_Ord = ""
    all_response1 = []
    #print("--------------------------------Response--------------------------------------")
    while ij != 5:
        try:
            #print("--------------------------------Response--------------------------------------")

            resp_OtherAPI2 = sock.recv(1024)
            sock.settimeout(0.01)
            #print(type(resp_OtherAPI2))
            #print("response recived length ",len(resp_OtherAPI2))
            all_response1.extend(resp_OtherAPI2)
            ij += 1
        except socket.timeout:
            #print("Socket timed out. Connection or data transfer took too long.")
            ij += 1


    #print("Total number of responses ", len(all_response1))

    byte_array = bytearray(all_response1)

    w = 0
    k = len(all_response1)
    while k>0:
        #print("1st value of w ",w)
        #print("------------------------------------------------------------------------------------")
        resp_OtherAPI = byte_array[w:w+8]
        #print("after add w ",w)
        resp_OtherAPI_Temp = struct.unpack_from("IH2s", resp_OtherAPI)
        print(resp_OtherAPI_Temp)
        #print("value of w ",w+8,"template size ",resp_OtherAPI_Temp[0])
        resp_OtherAPI2 = byte_array[w+8:w+resp_OtherAPI_Temp[0]]
        #print(len(resp_OtherAPI2))
        templete_id_response.append(resp_OtherAPI_Temp[1])
        decode_response(resp_OtherAPI_Temp[1],resp_OtherAPI2)
        #print(" secnd add w ",w)
        w = w+resp_OtherAPI_Temp[0]
        k = k-(resp_OtherAPI_Temp[0]+8)
        print("------------------------------------------------------------------------------------")

        #decode_response()

    '''for res in all_response1:
        print("___________________________________________________________________________________________________")

        resp_OtherAPI = res[0:8]
        resp_OtherAPI_Temp = struct.unpack_from("IH2s", resp_OtherAPI)
        print(resp_OtherAPI_Temp)
        resp_OtherAPI2= res[8:resp_OtherAPI_Temp[0]]
        decode_response(resp_OtherAPI_Temp[1], resp_OtherAPI2)
        try:
            print("--------------------------------Another response-----------------------------------------------------")
            resp_OtherAPI_Temp = res[resp_OtherAPI_Temp[0]:resp_OtherAPI_Temp[0]+8]
            resp_OtherAPI_Temp = struct.unpack_from("IH2s", resp_OtherAPI_Temp)
            print("another response ", resp_OtherAPI_Temp)

            print("bodylength ",resp_OtherAPI_Temp[0])
            resp_OtherAPI2 = res[resp_OtherAPI_Temp[0]+8:]
            decode_response(resp_OtherAPI_Temp[1],resp_OtherAPI2)
            #print("-----------------------------------------------------------------------------------------------------")





        except:
            print("Exception !!!!!!")


    '''

        #respdata.append(resp_OtherAPI_Temp[1])



def decode_response(resp_OtherAPI_Temp,resp_OtherAPI2):
    #print("length inside decode ",len(resp_OtherAPI2))
    Comment=""
    NP_Ord=""
    if (resp_OtherAPI_Temp == 10010):
        byte_string = bytes(resp_OtherAPI2)  # iv
        #print("byte string of iV ", byte_string)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 64), decryption_message)
        print("order reject response ", resp_Sub[13])
        NP_Ord = str("0000")
        Comment = str(resp_Sub[13])
    elif resp_OtherAPI_Temp == 10101:
        byte_string = bytes(resp_OtherAPI2)  # iv
        #print("byte string of iV ", byte_string)
        byte_array = bytearray(byte_string)

        byte_list = list(byte_array)
        #print("List of integers:", byte_list)
        encrypted_msg = bytes(byte_list)
        decryption_message = decryptor.update(encrypted_msg)
        #print("decryption_message ",decryption_message)
        resp_Sub = struct.unpack_from('QQQQQQIHB16sBQQQQQQQQQQIIHccHBB', decryption_message)
        #print("order no :", resp_Sub)
        print("new order Placed")
        print("Order number is = ", resp_Sub[11])
        actul = "New"
        #print("-------------------------------------------------------------------------------")
        NP_Ord = str(resp_Sub[11])
        non_persistent_orderno.append(str(resp_Sub[11]))
        Comment = str("New Order ")

    elif resp_OtherAPI_Temp == 10102:
        # resp_OtherAPI = struct.unpack_from('Q', resp_OtherAPI2[8:][56:64])  # 'IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI)-72)
        # print(resp_OtherAPI)
        #decryption_message = decryption(resp_OtherAPI2)
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_OtherAPI = struct.unpack_from('Q', decryption_message[56:64])

        # NP_Ord = str(resp_OtherAPI[0])
        #print("Order number is = ", resp_OtherAPI[0])
        #NP_Ord = str(resp_OtherAPI[0])
        #Comment = str("order rejected")
        #non_persistent_orderno.append(str(resp_OtherAPI[0]))


        print("Order number is = ", resp_OtherAPI[0])
        NP_Ord = str(resp_OtherAPI[0])
        Comment = str("new order placed")
        non_persistent_orderno.append(str(resp_OtherAPI[0]))

    elif resp_OtherAPI_Temp == 10103:
        #decryption_message = decryption(resp_OtherAPI2)
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_OtherAPI = struct.unpack_from('QQQIQQIHB16sBQQQQHBBB3s', decryption_message)
        Ord_No = str(resp_OtherAPI[11])
        NP_Ord = str(resp_OtherAPI[11])
        Comment = str("Immediate Execution")
        print("Immediate Execution order no ", str(resp_OtherAPI[11]))
        non_persistent_orderno.append(str(resp_OtherAPI[11]))
        #print("-------------------------------------------------------------------------------")
    elif (resp_OtherAPI_Temp == 10500):
        # trade_data1 = struct.unpack_from('QQIiBB7sqqqqqqqqqqqqqiIIIIIIQQii4s4s', resp_OtherAPI2)
        #decryption_message = decryption(resp_OtherAPI2)c

        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        trade_data1 = struct.unpack_from('QQIiBB7sqqqqqqqqqqqqqiIIIIIIQQii4s4s', decryption_message)
        #print("trade data ", trade_data1)
        print("Trade no = ", trade_data1[30])
        print("order no = ", trade_data1[14])
        print("Trade Price = ", trade_data1[8] / 100000000)
        print("Trade executed qty =", trade_data1[26] / 10000)
        print("Trade pending qty =", trade_data1[27])
        NP_Ord = str(trade_data1[14])
        Comment = str(" Trade Notification => trade no. " + str(trade_data1[30]) + " Trade executed qty => " + str(trade_data1[26] / 10000) + " Trade pending qty =>  "+ str(trade_data1[27]))
    elif resp_OtherAPI_Temp == 10104:
        # resp_OtherAPI = struct.unpack_from('IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI2) - 72),resp_OtherAPI2)
        # print("Traded with = ", resp_OtherAPI[8])
        #print("-------------------------------------------------------------------------------")
        #decrypted_msg = decryption(resp_OtherAPI2)
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('QQQIQQIB3sQQIIBB6s', decryption_message)
        actul = "Traded"
        NP_Ord = str("order executed ")
        Comment = str("Book Order Execution")
        print("Book Order Execution !!!!!")
        #non_persistent_orderno.append(str("000000"))
    elif resp_OtherAPI_Temp == 10117:



        byte_string = bytes(resp_OtherAPI2)  # iv
        byte_array = bytearray(byte_string)

        byte_list = list(byte_array)
        #print("List of integers:", byte_list)
        encrypted_msg = bytes(byte_list)
        #print(encrypted_msg)
        decryption_message = decryptor.update(encrypted_msg)
        #print("decryption_message ",decryption_message)
        resp_OtherAPI = struct.unpack_from('IQIH16sBBB7sQQQQQQQQQQQQQQQQQQQQQQQIIIIIIIHHBBBccBBBBBBBBB2sB5s7s9s2sB20s12s12s12sBBB2s',decryption_message)
        #print("decrypted msg ", resp_OtherAPI)

        NP_Ord = str(resp_OtherAPI[9])
        Cncl_Ord = str(resp_OtherAPI[9])
        Ord_stats = str(resp_OtherAPI[44])
        ordres = str(resp_OtherAPI[45])
        print(Ord_stats)
        print("order number ",NP_Ord)
        if (Ord_stats == "b'0'"):
            print("Order status = New Order ")
        elif (Ord_stats == "b'1'"):
            print("Order status =  Partially filled ")
        elif (Ord_stats == "b'2'"):
            print("Order status =  Filled ")
        elif (Ord_stats == "b'4'"):
            print("Order status = Cancelled ")
            Cncl_Ord = str(resp_OtherAPI[9])
            '''if (Ord_No != Cncl_Ord):
                print("Cancel Order number is = ", resp_OtherAPI[9])
            if (Ord_No == Cncl_Ord):
                print("Active SMPF = ", resp_OtherAPI[9])
            elif (Ord_No != Cncl_Ord):
                print("Passive SMPF = ", resp_OtherAPI[9])'''
        elif (Ord_stats == "b'6'"):
            print("Order status = Pending Cancel ")
        elif (Ord_stats == "b'7'"):
            print("Order status =  RRM Suspended ")
        elif (Ord_stats == "b'8'"):
            print("Order status =   SquareOff Suspended ")
        elif (Ord_stats == "b'9'"):
            print("Order status =  Suspended ")
        # ordres = str(resp_OtherAPI[37])
        print(ordres)
        if (ordres == "b'0'"):
            print("Order Execution type = New Order ")
        elif (ordres == "b'4'"):
            print("Order Execution type = Cancelled ")
        elif (ordres == "b'5'"):
            print("Order Execution type =  Replaced ")
            Comment = str("Order Modified")
        elif (ordres == "b'D'"):
            print("Order Execution type = Restated ")
        elif (ordres == "b'L'"):
            print("Order Execution type = Triggered ")
        elif (ordres == "b'F'"):
            print("Order Execution type = Traded ")
        if ((Ord_stats == "b'0'") and (ordres == "b'0'")):
            print("Extended Information of order => New Order ")
            actul = "New"
            Comment = str("New Order")
        elif ((Ord_stats == "b'4'") and (ordres == "b'4'")):
            print("Extended Information of order => Order Cancelled ")
            actul = "Cancelled"
            '''if (Ord_No == Cncl_Ord):
                print("Active SMPF = ", resp_OtherAPI[9])
                Comment = str("Active SMPF => Cancel Order number is " + str(resp_OtherAPI[9]))
            elif (Ord_No != Cncl_Ord):
                print("Passive SMPF = ", resp_OtherAPI[9])
                Comment = str("Passive SMPF => Cancel Order number is " + str(resp_OtherAPI[9]))'''
        elif ((Ord_stats == "b'1'") and (ordres == "b'F'")):
            print("Extended Information of order => Partially Traded")
            actul = "Partially Traded"
            Comment = str("Partially Traded")
        elif ((Ord_stats == "b'1'") and (ordres == "b'0'")):
            print("Extended Information of order => Partially Traded")
            actul = "Partially Traded"
            Comment = str("Partially Traded")
        elif ((Ord_stats == "b'2'") and (ordres == "b'F'")):
            print("Extended Information of order => Fully Traded ")
            actul = "Fully Traded"
            Comment = str("Fully Traded")
        elif ((Ord_stats == "b'8'") and (ordres == "b'0'")):
            print("Extended Information of order => New order Suspended due to SquareOff")
            actul = "New order Suspended due to SquareOff"
            Comment = str("New order Suspended due to SquareOff")
        elif ((Ord_stats == "b'4'") and (ordres == "b'F'")):
            print("Extended Information of order => Partially Traded and Cancelled due to Active SMPF")
            actul = "Partially Traded and Active SMPF"
            '''if (Ord_No == Cncl_Ord):
                print("Active SMPF = ", resp_OtherAPI[9])
                Comment = str("Active SMPF => Cancel Order number is " + str(resp_OtherAPI[9]))
            elif (Ord_No != Cncl_Ord):
                print("Passive SMPF = ", resp_OtherAPI[9])
                Comment = str("Passive SMPF => Cancel Order number is " + str(resp_OtherAPI[9]))'''
        #print("-------------------------------------------------------------------------------")
    elif resp_OtherAPI_Temp == 10122:
        # resp_OtherAPI = struct.unpack_from('IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI2) - 72),resp_OtherAPI2)
        # print(resp_OtherAPI)
        #decrypted_msg = decryption(resp_OtherAPI2)
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('QQQIQQIB3sQQIIBB{}s'.format(len(decryption_message) - 64), decryption_message)
        Comment = str("Delete All Order Broadcast")
        print("Delete All Order Broadcast")
    elif resp_OtherAPI_Temp == 10003:
        # resp_OtherAPI = struct.unpack_from('IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI2) - 72),resp_OtherAPI2)
        # print(resp_OtherAPI)

        #decrypted_msg = decryption(resp_OtherAPI2)

        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from('QQQIQQIB3sQQIIBB{}s'.format(len(decryption_message) - 64), decryption_message)
        Comment = str("Session Logout Response")
        print("Session Logout Response")

    elif resp_OtherAPI_Temp == 10107:
        #decryption_message = decryption(resp_OtherAPI2)

        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from('QQQQQQIHB16sBQQQQQQQQQQIIHccHBB', decryption_message)
        # print("order modification sucess!!!", resp_Sub[11])
        print("persistent order modify sucess", resp_Sub[11])
        NP_Ord = str(resp_Sub[11])
        Comment = str("Order Modified")
    elif resp_OtherAPI_Temp == 10110:
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from(cancelorder_response_formattype, decryption_message)
        print("order cancle sucess!!!", resp_Sub[11])
        print("persistent order Cancel sucess")
        Ord_No = str(resp_Sub[11])
        NP_Ord = str(resp_Sub[11])
        Comment = str("Order Cancel")
    elif resp_OtherAPI_Temp == 10031:
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('QQIHBBB7sQH256s6s{}s'.format(len(decryption_message) - 306), decryption_message)
        Comment = str("News")
        print("news response ", resp_Sub)
        print("header ", resp_Sub[10])
        print("message_Text ", resp_Sub[12])
    elif resp_OtherAPI_Temp == 10108:
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('Q', decryption_message[64:72])
        print("non-persistence order Modify success")
        #Comment = str("Order Modified")

        NP_Ord = str(int(non_persistent_orderno[len(non_persistent_orderno) - 1]))
        Comment = str("Order Modified")

    elif resp_OtherAPI_Temp == 10111:
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        print(encrypted_msg)
        decryption_message = decryptor.update(encrypted_msg)
        print(decryption_message)
        resp_OtherAPI = struct.unpack_from('Q', decryption_message[64:72])
        print(resp_OtherAPI)
        print("non-persistence order cancel success")
        #Comment = str("Order Cancel")

        NP_Ord = str(int(non_persistent_orderno[len(non_persistent_orderno) - 1]))
        Comment = str("Order Cancel")
    elif resp_OtherAPI_Temp == 10024:
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from('QQQIQQIB3sQQIIBB{}s'.format(len(decryption_message) - 64), decryption_message)
        Comment = str("User Logout Response", resp_Sub)
    elif resp_OtherAPI_Temp == 10112:
        #decrypted_msg = decryption(resp_OtherAPI2)

        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from('QQQQQIHB16sBQQQqQqq1s1sHB3s', decryption_message)
        Comment = str("User Logout Response")
        print("order cancle notification sucess ")
    elif resp_OtherAPI_Temp == 0:
        resp_OtherAPI = struct.unpack_from('IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI2) - 72),
                                           resp_OtherAPI2)
        print(resp_OtherAPI)
        Comment = str("Unknown Response")
    elif resp_OtherAPI_Temp == 10012:
        # resp_OtherAPI = struct.unpack_from('IH2sQH6s{}s'.format(len(resp_OtherAPI2) - 72), resp_OtherAPI2)
        # print(resp_OtherAPI)
        #decrypted_msg = decryption(resp_OtherAPI2)

        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)

        resp_Sub = struct.unpack_from('QH6s{}s'.format(len(decryption_message) - 64), decryption_message)
        print("Session Logout Notification ", resp_Sub)
        Comment = str("Session Logout Notification")
    elif resp_OtherAPI_Temp == 1215:
        # resp_OtherAPI = struct.unpack_from('IH8s2sQQQIQQIB3sQQIIBB6s'.format(len(resp_OtherAPI2) - 72),resp_OtherAPI2)
        # print(resp_OtherAPI)
        #decrypted_msg = decryption(resp_OtherAPI2)
        byte_string = bytes(resp_OtherAPI2)
        byte_array = bytearray(byte_string)
        encrypted_msg = byte_array
        decryption_message = decryptor.update(encrypted_msg)
        resp_Sub = struct.unpack_from('QQQIQQIB3sQQIIBB{}s'.format(len(decryption_message) - 64), decryption_message)
        Comment = str("Unknown Response ", resp_Sub)
    elif resp_OtherAPI_Temp == 65535:
        Comment = str("Unknown Response")
    Act_Response.append(str(resp_OtherAPI_Temp) + "-" + str(NP_Ord) + "-" + str(Comment))
    resp_OtherAPI2.clear()



def sendOrder(sock,key,iv):
    #print("total no of orders available - ", order_count)
    config_data = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name="Configuration", engine='openpyxl')
    print("total no of orders available - ",len(config_data))
    for i in range(0,len(config_data)):
        print("-----------------------------------Sending Order------------------------------------")

        config_data_read = config_data.loc[i]
        # print("Order Data - " , config_data_read)
        order_type = config_data_read.loc["order_type"]
        testcase = config_data_read.loc["Test_case_name"]
        status = str(config_data_read.loc["status"])
        order_row_number = config_data_read.loc["Order_no(Row_number)"]
        #print("Order_no(Row_number)" ,order_row_number)
        if status.upper() == "Y":
            # exp_resp.append(config_data_read.loc["Expected_Response"])
            testcase = config_data_read.loc["Test_case_name"]
            TestCase_name_final.append(testcase)
            if order_type.upper() == "NEW":
                df_orderdata = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Orderdata,engine='openpyxl')
                config_data_read = df_orderdata.loc[order_row_number]
                #print("new order data template", config_data_read[1])
                user_id.append(config_data_read[5])
                message_seq_no.append(config_data_read[4])
                print("order Type is ", order_type, " & order no is ", i + 1, " & Message seq num is ", config_data_read[4])
                rqstFields_header = config_data_read.loc["BodyLen":"Price"].iloc[0:6]
                rqstFields_message = config_data_read.loc["Price":"FreeText3"]
                # print(rqstFields_header[4])

                rqstFields_header[4] = config_data_read[4]

                new_order_header_stream = CreatePayload(rqstFields_header, new_order_header)
                bytestream_new_order = CreatePayload(rqstFields_message, neworder_formattype_message)
                ########################################################################

                encrypted_text = encryptor.update(bytestream_new_order)
                encrypted_text1 = new_order_header_stream + encrypted_text

                sock.sendall(encrypted_text1)

                #encrypted_text = encryption(new_order_header_stream, bytestream_new_order,key,iv)
                #print("Order enc text: ",encrypted_text)
                #sock.sendall(encrypted_text)

            elif order_type.upper() == "MODIFY":
                df_orderdata = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Orderdata,engine='openpyxl')
                config_data_read = df_orderdata.loc[order_row_number]
                rqstFields_header = config_data_read.loc["MBodyLen":"SenderSubID"]
                rqstFields_message = config_data_read.loc["MOrderID":"MPad4"]

                print(non_persistent_orderno)
                rqstFields_message[0] = int(non_persistent_orderno[int(order_row_number)])
                print("old order no ",int(non_persistent_orderno[int(order_row_number)]))
                user_id.append(config_data_read[5])

                modifiy_order_header_stream = CreatePayload(rqstFields_header, modify_order_header)
                bytestream_modified_order = CreatePayload(rqstFields_message, modifyorder_formattype)
                ########################################################################
                #encrypted_text = encryption(modifiy_order_header_stream, bytestream_modified_order,key,iv)

                encrypted_text = encryptor.update(bytestream_modified_order)
                encrypted_text1 = modifiy_order_header_stream + encrypted_text

                sock.sendall(encrypted_text1)

                #sock.sendall(encrypted_text)


            elif order_type.upper() == "CANCEL":
                df_orderdata = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Orderdata,engine='openpyxl')
                config_data_read = df_orderdata.loc[order_row_number]
                rqstFields_header = config_data_read.loc["CBodyLen":"COrderID"].iloc[0:6]
                rqstFields_message = config_data_read.loc["COrderID":"CPad4"]

                rqstFields_message[0] =  int(non_persistent_orderno[int(order_row_number)])
                user_id.append(config_data_read[5])

                cancle_order_header_stream = CreatePayload(rqstFields_header, cancle_order_header)
                bytestream_cancle_order = CreatePayload(rqstFields_message, cancleorder_formattype)
                ########################################################################
                #encrypted_text = encryption(cancle_order_header_stream, bytestream_cancle_order,key,iv)
                #print("Order enc text: ",encrypted_text,"\n length :", len(encrypted_text))
                #sock.sendall(encrypted_text)

                encrypted_text = encryptor.update(bytestream_cancle_order)
                encrypted_text1 = cancle_order_header_stream + encrypted_text

                sock.sendall(encrypted_text1)

        Read_Response(sock,key,iv)

        sleep(1)

def tc_validation():
    # config_data = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name="Configuration", engine='openpyxl')
    print(Act_Response)
    expected_response = ['10101', '10117', '10107', '10117', '10110', '10112'] # expected response for 1 TC
    test_case_size = len(expected_response) # 6
    # # split response to extract codes from Act_Response
    actual_response_codes = [entry.split('-', 1)[0] for entry in Act_Response if '-' in entry]
    # Validate each test case chunk
    total_test_cases = len(actual_response_codes) // test_case_size  # eg: 18/6 = 3 TCs
    for i in range(total_test_cases):
        start = i * test_case_size
        end = start + test_case_size
        tc_codes = actual_response_codes[start:end]
        if tc_codes == expected_response:
            print(f"TC{i + 1}: PASS")
        else:
            print(f"TC{i + 1}: FAIL")
            print(f"  Expected: {expected_response}")
            print(f"  Actual:   {tc_codes}")

# Gateway Session Connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_SL, port_SL))
    print("-----------------------------------------------------------------------")
    print("Gateway Logon Request")
    print(rqstFields_CG)
    bytestream_SL = CreatePayload(rqstFields_CG, format_Req_CG)
    sock.sendall(bytestream_SL)
    resp_SL = sock.recv(8)
    resp_SL_Temp = struct.unpack_from("IH2s", resp_SL)
    print(resp_SL, resp_SL_Temp)

    resp_SL1 = sock.recv(1024)


    if (resp_SL_Temp[1] == 10010):
        # resp_OtherAPI = struct.unpack(format_resp_OtherAPI, resp_OtherAPI)
        resp_SL = struct.unpack_from('IH2sQQQQQQIB3sIHB1s{}s'.format(len(resp_SL1) - 72),
                                     resp_SL1)  # IH2sQQQQQQIB3sIHB1s96s
        print("Reject Response\n", resp_SL[16], "\n\n")
        print("Getway log out from method (if)")
        sys.exit()
    else:
        #print("-----------------------------------------------------------------------")
        byte_array = bytearray(resp_SL1)
        key = password_key
        iv = password_iv
        encrypted_msg = byte_array
        # byte_array = bytearray(byte_string)
        print("Byte array:", encrypted_msg)

        # Convert byte array to list of integers (byte values)
        byte_list = list(encrypted_msg)
        #print("List of integers:", byte_list)

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        # Decrypt and authenticate the message
        decrypted_msg = cipher.decrypt(encrypted_msg)
        server_key1 = struct.unpack_from('32s', decrypted_msg[48:81])
        server_iv1 = struct.unpack_from('12s', decrypted_msg[81:94])
        final_key = server_key1[0]
        final_iv = server_iv1[0]

        print("Gateway log out from method (else)")

    # Session Logon Request/Response
    sock.close()
    #time.sleep(35)
    #print("-----------------------------------------------------------------------")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip_SL, port_SL))
        '''print("Session Logon Request")
        session_header_stream = CreatePayload(rqstFields_SL_header, format_session_login_header)
        bytestream_SL = CreatePayload(rqstFields_SL, format_Req_SL)
        ########################################################################

        encrypted_text = encryption(session_header_stream, bytestream_SL,final_key,final_iv)
        sock.sendall(encrypted_text)
        resp_SL = sock.recv(8)
        resp_SL_Temp = struct.unpack_from("IH2s", resp_SL)
        print("decoded server response header ",resp_SL_Temp)
        resp_SL1 = sock.recv(1024)

        #resp_SL_Temp = struct.unpack_from("IH", resp_SL)
        if (resp_SL_Temp[1] == 10010):
            decrypted_msg = decryption(resp_SL1,final_key,final_iv)
            resp_SL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decrypted_msg) - 64),decrypted_msg)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_SL[13], "\n\n")
        else:
            decryption_message = decryption(resp_SL1,final_key,final_iv)
            print("session login sucess!!!!!!")'''

        ############################################################

        session_header_stream = CreatePayload(rqstFields_SL_header, format_session_login_header)
        bytestream_SL = CreatePayload(rqstFields_SL, format_Req_SL)
        ########################################################################

        #final_session_login_request = session_header_stream + bytestream_SL

        print("final key in session ",final_key ," ",final_iv)
        key = server_key1[0] # Replace this with the actual key used for encryption
        iv = server_iv1[0]

        #cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()

        encrypted_text = encryptor.update(bytestream_SL)

        ciphertext_array = bytearray(encrypted_text)
        final_session_login_request = session_header_stream + ciphertext_array

        sock.sendall(final_session_login_request)
        resp_SL = sock.recv(8)

        resp_SL_Temp = struct.unpack_from("IH2s", resp_SL)
        print("session login server response ",resp_SL_Temp)
        resp_SL1 = sock.recv(1024)

        print("received length in session login resp ", len(resp_SL1))
        #print("session logon response ", resp_SL1)
        if (resp_SL_Temp[1] == 10010):
            #decryption_message = decryption(resp_SL1)
            byte_string = bytes(resp_SL1)  # iv
            byte_array = bytearray(byte_string)
            encrypted_msg = byte_array
            decryption_message = decryptor.update(encrypted_msg)
            resp_SL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 64),decryption_message)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_SL[13], "\n\n")
            #print("decryption_message ", resp_SL[13])

            sys.exit()

        else:
            #decryption_message = decryption(resp_SL1)
            byte_string = bytes(resp_SL1)  # iv
            byte_array = bytearray(byte_string)
            encrypted_msg = byte_array
            decryption_message = decryptor.update(encrypted_msg)
            decryption_data = struct.unpack_from("QQI4sIIIIBB6s",decryption_message)
            #print("decryption_message ",decryption_data)

            print("session login sucess!!!!!!")


        ##########################################################




        # User Logon Request/Response
        #print("-----------------------------------------------------------------------")
        print("User Logon Request")

        userlogin_header_stream = CreatePayload(rqstFields_UL_header, format_user_login_header)
        bytestream_UL = CreatePayload(rqstFields_UL, format_Req_UL)
        ########################################################################

        encrypted_text = encryptor.update(bytestream_UL)
        encrypted_text = userlogin_header_stream + encrypted_text

        sock.sendall(encrypted_text)

        resp_UL = sock.recv(8)

        resp_UL_Temp = struct.unpack_from("IH2s", resp_UL)
        print("decoded server response header ", resp_UL_Temp)

        resp_UL1 = sock.recv(1024)

        print("received length in user login resp ", len(resp_UL1))

        if (resp_UL_Temp[1] == 10010):

            byte_string = bytes(resp_UL1)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            resp_UL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 72),
                                         decryption_message)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_UL, "\n\n")
        else:
            #resp_UL = struct.unpack_from(format_resp_UL, resp_UL)
            byte_string = bytes(resp_UL1)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            print("User Logon sucess!!!!\n")


        print("Subscription Request - 1")
        #print("subscribe data ")
        subscribe_header_stream = CreatePayload(rqstFields_sub_header, format_subscribe_header)
        bytestream_sub = CreatePayload(rqstFields_Sub, format_Req_Sub)
        ########################################################################
        #encrypted_text = encryption(subscribe_header_stream, bytestream_sub,final_key,final_iv)
        #sock.sendall(encrypted_text)

        encrypted_text = encryptor.update(bytestream_sub)
        encrypted_text = subscribe_header_stream + encrypted_text

        sock.sendall(encrypted_text)


        #print(rqstFields_Sub)

        resp_Sub = sock.recv(8)
        resp_Sub_Temp = struct.unpack_from("IH2s", resp_Sub)
        print("decoded server response Subscription header ", resp_Sub_Temp)
        resp_Sub = sock.recv(1024)

        if (resp_UL_Temp[1] == 10010):
            byte_string = bytes(resp_Sub)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            resp_UL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 72),
                                         decryption_message)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_UL, "\n\n")
        else:
            byte_string = bytes(resp_Sub)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            #decryption_message = decryption(resp_Sub,final_key,final_iv)
            resp_Sub1 = struct.unpack_from('QQI4sI4s', decryption_message)
            print("sub response 1 ", resp_Sub1)
            unique_ref_id.append(resp_Sub1[4])

        # Subscription Request/Response - 2
        #print("-----------------------------------------------------------------------")
        print("Subscription Request - 2 ")

        #print(rqstFields_Sub2)
        subscribe_header_stream = CreatePayload(rqstFields_sub_header2, format_subscribe_header)
        bytestream_sub1 = CreatePayload(rqstFields_Sub2, format_Req_Sub)
        ########################################################################
        #encrypted_text = encryption(subscribe_header_stream, bytestream_sub,final_key,final_iv)
        #sock.sendall(encrypted_text)


        encrypted_text = encryptor.update(bytestream_sub1)
        encrypted_text = subscribe_header_stream + encrypted_text

        sock.sendall(encrypted_text)

        resp_Sub = sock.recv(8)
        resp_Sub_Temp = struct.unpack_from("IH2s", resp_Sub)
        print("decoded server response Subscription header ", resp_Sub_Temp)
        resp_Sub11 = sock.recv(1024)

        if (resp_UL_Temp[1] == 10010):
            byte_string = bytes(resp_Sub11)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            resp_UL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 72),
                                         decryption_message)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_UL, "\n\n")
        else:
            byte_string = bytes(resp_Sub11)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            #decryption_message = decryption(resp_Sub,final_key,final_iv)
            resp_Sub1 = struct.unpack_from('QQI4sI4s', decryption_message)
            print("sub response 2 ", resp_Sub1)
            unique_ref_id.append(resp_Sub1[4])

        # Subscription Request/Response - 3
        #print("-----------------------------------------------------------------------")
        print("Subscription Request - 3")

        subscribe_header_stream = CreatePayload(rqstFields_sub_header3, format_subscribe_header)
        bytestream_sub3 = CreatePayload(rqstFields_Sub3, format_Req_Sub)
        ########################################################################
        #encrypted_text = encryption(subscribe_header_stream, bytestream_sub,final_key,final_iv)
        #sock.sendall(encrypted_text)


        encrypted_text = encryptor.update(bytestream_sub3)
        encrypted_text = subscribe_header_stream + encrypted_text

        sock.sendall(encrypted_text)

        resp_Sub = sock.recv(8)
        resp_Sub_Temp = struct.unpack_from("IH2s", resp_Sub)
        print("decoded server response Subscription header ", resp_Sub_Temp)
        resp_Sub = sock.recv(1024)
        if (resp_UL_Temp[1] == 10010):
            byte_string = bytes(resp_Sub)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            resp_UL = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 72),
                                         decryption_message)  # IH2sQQQQQQIB3sIHB1s96s
            print("Reject Response\n", resp_UL, "\n\n")
        else:
            byte_string = bytes(resp_Sub)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)
            # decryption_message = decryption(resp_Sub,final_key,final_iv)
            resp_Sub1 = struct.unpack_from('QQI4sI4s', decryption_message)
            print("sub response 3 ", resp_Sub1)
            unique_ref_id.append(resp_Sub1[4])

        act_resp = []
        exp_resp = []
        respdata = []
        cmnt = []

        ##########################

        '''df_orderdata = pd.read_excel(open(MasterData_Path, 'rb'), sheet_name=sheetName_Orderdata, engine='openpyxl')
        config_data_read = df_orderdata.loc[0]
        # print("new order data template", config_data_read[1])
        user_id.append(config_data_read[5])
        message_seq_no.append(config_data_read[4])
        #print("order Type is ", order_type, " & order no is ", i + 1, " & Message seq num is ", config_data_read[4])
        rqstFields_header = config_data_read.loc["BodyLen":"Price"].iloc[0:6]
        rqstFields_message = config_data_read.loc["Price":"FreeText3"]
        # print(rqstFields_header)

        rqstFields_header[4] = config_data_read[4]

        new_order_header_stream = CreatePayload(rqstFields_header, new_order_header)
        bytestream_new_order = CreatePayload(rqstFields_message, neworder_formattype_message)
        ########################################################################

        encrypted_text = encryptor.update(bytestream_new_order)
        encrypted_text1 = new_order_header_stream + encrypted_text

        sock.sendall(encrypted_text1)
        ###########################

        resp_Sub = sock.recv(8)
        resp_Sub_Temp = struct.unpack_from("IH2s", resp_Sub)
        print("order reject response ", resp_Sub_Temp)
        resp_Sub111 = sock.recv(1024)

        print("received length in order  resp ", len(resp_Sub111))



        byte_string = bytes(resp_Sub111)  # iv
        encrypted_msg = bytearray(byte_string)
        byte_list = list(encrypted_msg)

        print("order bytearray ",byte_list)

        if (resp_Sub_Temp[1] == 10010):

            byte_string = bytes(resp_Sub111)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)

            resp_Sub = struct.unpack_from('QQQQQQIB3sIHB1s{}s'.format(len(decryption_message) - 64), decryption_message)
            printable_part = re.findall(b'[ -~]+', resp_Sub[13])
            plaintext = b''.join(printable_part).decode('utf-8')
            print("order reject response ", resp_Sub)
            NP_Ord = str("0000")
            Comment = str(plaintext)
        elif (resp_Sub_Temp[1] == 10101) :
            #decryption_message = decryption(resp_OtherAPI2, key, iv)
            byte_string = bytes(resp_Sub111)  # iv
            encrypted_msg = bytearray(byte_string)
            decryption_message = decryptor.update(encrypted_msg)


            resp_Sub = struct.unpack_from('QQQQQQIHB16sBQQQQQQQQQQIIHccHBB', decryption_message)

            price = struct.unpack_from('Q', decryption_message[80:88])

            # print("order no :", resp_Sub[11])
            print("new order Placed")
            print("Order number is = ", resp_Sub[11])'''
        try:
            sendOrder(sock,final_key,final_iv)
            print("order sending completed going to write the result data in excel file")
            excel_report()
        except Exception as exc1:
            print(exc1)
            print("exception occured going to write the result data in excel file")
            excel_report()
        tc_validation()



        print("-----------------------------END---------------------------------------")









