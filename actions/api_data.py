import requests 
import json

#class PlanDetails:
def getplandetail(inceptionDate,expiryDate,areaCode,classId,categoryId,issueDate,desCountryId):
    url = "https://kec.kgisl.com/amgqa/amgservices/nonmotor/getnmplandetails"
    payload = json.dumps({
                        "requestData": "{\"inceptionDate\":\""+inceptionDate+"\",\"expiryDate\":\""+expiryDate+"\",\"areaCode\":"+areaCode+",\"classId\":"+classId+",\"categoryId\":"+categoryId+",\"issueDate\":\""+issueDate+"\",\"renewalInd\":\"N\",\"policyId\":0,\"desCountryId\":"+desCountryId+"}"})
    headers = {'channel': 'APSPPS','brand': 'K','device': 'desktop','browser': 'chrome','Content-Type': 'application/json','username': '243400-00'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)# print("HELLOOOOOOOOOOO")return response
    
    return response.text