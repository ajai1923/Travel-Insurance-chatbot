# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker 
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import Action
from rasa_sdk.types import DomainDict
# from api_data import * 
from . import api_data
import re
from datetime import datetime, date
from rasa_sdk.events import SlotSet

#-----------------------------Form validation------------------------------------------------------#

class FormValidation(Action):
    def name(self):
        return "form_validation"
    
    
    def validate_travel_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate travel date question value."""
        
        if slot_value == "01/02/2023":
            
            return {"travel_date": slot_value}
        else:
            dispatcher.utter_message(text="Please enter the your departure date")
            
        
        now = datetime.today()
        date_time1 = now.strftime("%d/%m/%Y")
        print("date_time1:",date_time1,type(date_time1))
        # userInputdate = '30/01/2023'
        userInputdate = slot_value
        # userInputdate = '30-01-2023'
        val1 =''
        if re.search("/", userInputdate):
            print("YES! 1-->: "+userInputdate) 
            val1 = datetime.strptime(userInputdate, "%d/%m/%Y")
        if re.search("-", userInputdate):
            print("YES! 2-->: ",userInputdate) 
            val1 = datetime.strptime(userInputdate, "%d-%m-%Y")

        print('date_values-->: ',val1)
        date_time2 = val1.strftime("%d/%m/%Y")
        print('userInput-->: ',date_time2,type(date_time2))

        current_date = datetime.strptime(date_time1, "%d/%m/%Y").date()
        # print(date1,type(date1))
        user_date = datetime.strptime(date_time2, "%d/%m/%Y").date()
        # print(user_date,type(user_date))
        if current_date <= user_date: 
            print('Trueee')
        else:
            print('Falsee')
            
            return {"travel_date": None}
        
        
        
        
    def validate_arrival_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate arrival date question value."""
        
        if slot_value == "28/02/2023":
            
            return {"arrival_date": slot_value}
        else:
            dispatcher.utter_message(text="Please enter the your departure date")
            
        now = datetime.today()
        date_time1 = now.strftime("%d/%m/%Y")
        print("date_time1:",date_time1,type(date_time1))
        # userInputdate = '30/01/2023'
        userArrivaldate = slot_value
        # userInputdate = '30-01-2023'
        val1 =''
        if re.search("/", userArrivaldate):
            print("YES! 1-->: "+userArrivaldate) 
            val1 = datetime.strptime(userArrivaldate, "%d/%m/%Y")
        if re.search("-", userArrivaldate):
            print("YES! 2-->: ",userArrivaldate) 
            val1 = datetime.strptime(userArrivaldate, "%d-%m-%Y")

        print('date_values-->: ',val1)
        date_time2 = val1.strftime("%d/%m/%Y")
        print('userInput-->: ',date_time2,type(date_time2))

        
        user_date = datetime.strptime(date_time2, "%d/%m/%Y").date()
        # print(user_date,type(user_date))
        arrival_date = datetime.strptime(arrival_date, "%d/%m/%Y").date()
        if arrival_date > user_date: 
            print('Trueee')
        else:
            print('Falsee')
            
            return {"arrival_date": None}
        
        
    
#---------------------- PLan details --------------------------------#

class getPersonalSingleIndividualPlanDetails(Action):
    def name(self) -> Text:
        return "get_personal_single_individual_plan_details"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        inceptiondate = tracker.get_slot("travel_date")
        expirydate = tracker.get_slot("arrival_date")
        country = tracker.get_slot("country_name")
        f = open(r'D:\Travel Insurance chatbot\actions\data.json')
        
        dataa = json.load(f)
        
        
        for i in dataa['nationalityList']:
            if country.lower() == i['desc'].lower():
                countrycode = str(i["id"])
            else:
                countrycode = "0"
            f.close()
            areacode = "3"
            issuedate = date.today()
            issuedate = issuedate.strftime('%d-%m-%Y')
            str(issuedate)
            classid = "238"
            categoryid = "1"
            print(type(inceptiondate),type(expirydate),type(areacode),type(classid),type(categoryid),type(issuedate),type(countrycode))
            print(inceptiondate,expirydate,areacode,classid,categoryid,issuedate,countrycode)
            response = api_data.getplandetail(inceptiondate,expirydate,areacode,classid,categoryid,issuedate,countrycode)
            print(response.text)
            response = json.loads(response.text)
            if "errorCode" not in response["responseData"]:
                resp = json.loads(response["responseData"]) 
                prem_a = resp["planList"][0]["grossPremium"]
                prem_b = resp["planList"][1]["grossPremium"]
                print(prem_a, prem_b)
                return [SlotSet("premium_a",prem_a),SlotSet("premium_b",prem_b)]
            elif "errorCode" in response["responseData"]:
                dispatcher.utter_message("Your details have not been entered properly. Please make sure the dates you have entered do not preced today's date")
            return None
        
        
#------------------------ concatenate method---------------------------#

class AskInfoMsg(Action):
    def name(self):
        return "ask_info_msg"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_ask_info_msg", tracker)

        return []
    
#----------------------------2nd-----------------------------#    
    
# class AskPlan(Action):
#     def name(self):
#         return "ask_plan"
    
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_template("utter_ask_plan", tracker)
        
#         return []
                
                
#------------------- concatenate the string optionsss ----------------------------------#

# class ActionUserInfo(Action):
#     def name(self):
#         return "action_user_info"

#     def run(self, dispatcher, tracker, domain):
#         inceptiondate = tracker.get_slot("travel_date")
#         expirydate = tracker.get_slot("arrival_date")
#         country = tracker.get_slot("country_name")
#         message = tracker.get_slot("info_msg")
#         response = "You have chosen Single Trip policy for Personal purpose travelling to {}. Your coverage starts on {}  and ends on {}.".format(country_name, travel_date, arrival_date)
#         dispatcher.utter_message(response)
#         return [SlotSet("info_msg", message)]
        
        #   return []              
                
#---------------- API Calling ---------------------------------------


    #print('PlanDetails--->', api_data.getplandetail)
    
    
    

