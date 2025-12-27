from flask import Flask, render_template,request, jsonify
import json
import requests
from requests.auth import HTTPBasicAuth
# app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0   
SAP_URL_TEMPLATE = "http://192.168.1.49:8000/sap/opu/odata/sap/YJSRB_ATM_DATA_SRV/Atm_dataSet('{}')?$format=json"
USERNAME = "Trainee3"
PASSWORD = "Incresol@789"


@app.route("/Atmcard")
def Atmcard():
    account = request.args.get("account")
    sap_data = None

    if account:
        url = SAP_URL_TEMPLATE.format(account)
        try:
            response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            if response.status_code == 200:
                sap_data = response.json()["d"]
            else:
                sap_data = {"error": f"Failed to fetch data ({response.status_code})"}
        except Exception as e:
            sap_data = {"error": str(e)}
  

#     # print()     # "export parameters are stored in results as json format"
#    # Extract EX_JSON dictionary
    
    
     #Expiry date formatted
    exp_date = sap_data["AtmExpDate"]  # e.g., "20301003"
    timestamp_erdat = int(exp_date[7:19])/ 1000 
    dt = datetime.fromtimestamp(timestamp_erdat)
    formatted_date = dt.strftime('%Y-%m-%d')
    exp_formatted = str(formatted_date[5:7]) + '/' +   str(formatted_date[2:4])  # 10/30
    #ATM  number formatted ex 1111 2222 3333 4444
    Atm_no = " ".join( sap_data["AtmNumber"][i:i+4] for i in range(0, len( sap_data["AtmNumber"]), 4))
    Atm_digit =  sap_data["AtmDigits"]
    h_name =  sap_data["AccHolderName"]
    Atm_cvv =  sap_data["AtmCvv"]
    Atm_ref =  sap_data["AtmRef"]
    
    Final_data= {"Hname": h_name ,"AtmNo": Atm_no,"AtmDgt": Atm_digit,"ExpDt": exp_formatted,"AtmCvv": Atm_cvv,"AtmRef": Atm_ref }  
    return render_template("index.html",data=Final_data)#, card_no=c_no,data=d, exp=exp_formatted)
   
if __name__ == "__main__":
    # app.run(debug=True) "only in laptop"
     app.run(host="0.0.0.0", port=5000,debug=True) #other device also"

    
