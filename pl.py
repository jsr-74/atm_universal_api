from flask import Flask, render_template, request
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

SAP_URL_TEMPLATE = "http://192.168.1.49:8000/sap/opu/odata/sap/YJSRB_ATM_DATA_SRV/Atm_dataSet('{}')?$format=json"


USERNAME = "Trainee3"
PASSWORD = "Incresol@789"


@app.route("/Atmcard")
def Atmcard():
    account = request.args.get("account")
    if not account:
        return "account query parameter is required", 400

    try:
        url = SAP_URL_TEMPLATE.format(account)
        response = requests.get(
            url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=10
        )
        response.raise_for_status()
        sap_data = response.json()["d"]

    except Exception as e:
        return str(e), 500

    exp_date = sap_data["AtmExpDate"]

    # If SAP gives /Date(1696118400000)/
    if "Date" in exp_date:
        timestamp = int(exp_date[6:19]) / 1000
        dt = datetime.fromtimestamp(timestamp)
        exp_formatted = dt.strftime("%m/%y")
    else:
        exp_formatted = exp_date[4:6] + "/" + exp_date[2:4]

    atm_number = sap_data["AtmNumber"]
    Atm_no = " ".join(atm_number[i:i+4] for i in range(0, len(atm_number), 4))

    Final_data = {
        "Hname": sap_data["AccHolderName"],
        "AtmNo": Atm_no,
        "AtmDgt": sap_data["AtmDigits"],
        "ExpDt": exp_formatted,
        "AtmCvv": sap_data["AtmCvv"],
        "AtmRef": sap_data["AtmRef"]
    }

    return render_template("index.html", data=Final_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
