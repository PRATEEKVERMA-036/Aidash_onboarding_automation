config={

    "authority": "https://login.microsoftonline.com/13cee7a3-b15d-47d9-8f30-f5bd649e3967",
    
    "client_id": "eb28dd38-bccb-4c4a-b696-239daeacb264",
    
    "scope": [ "https://graph.microsoft.com/.default"],
    
    "secret": "GrK8Q~45pNWJ0qmUN7zBhDb~XleliBDqf~sYRak7",
    
    "endpoint": "https://graph.microsoft.com/v1.0/users?$top=999"
    
    }


import sys

####################### Jenkins Job inputs

# first_name="test10prateek"
# middle_name="test10midname"
# last_name="test10lastname"
# mobile_number="+916388463747"
# proposed_date_of_joining="10/11/2023"
# manager_email_id="shastry@aidash.com"
# department="gis"
# job_title="DevOps Intern"
# type_of_engagement="Intern-personal-laptop"
# country_of_residence="US"
# email_id_of_joinee=first_name+"."+last_name+"@aidash.com"
# joinee_personal_email_id="prateek544verma@gmail.com"

first_name=sys.argv[1]
middle_name=sys.argv[2]
last_name=sys.argv[3]
mobile_number=sys.argv[4]
proposed_date_of_joining=sys.argv[5]
manager_email_id=sys.argv[6]
department=sys.argv[7]
job_title=sys.argv[8]
type_of_engagement=sys.argv[9]
country_of_residence=sys.argv[10]
email_id_of_joinee=first_name+"."+last_name+"@aidash.com"
joinee_personal_email_id=sys.argv[11]
manually_inserted_aidash_email_id=sys.argv[12]

if(manually_inserted_aidash_email_id != "none"):
    email_id_of_joinee=manually_inserted_aidash_email_id


#######################




####################### Generating random password for new user Azure AD account
### Source: https://pypi.org/project/random-password-generator/

from password_generator import PasswordGenerator

pwo = PasswordGenerator()

pwo.minlen = 10 # Minimum length of the password
pwo.maxlen = 16 # Maximum length of the password
pwo.minuchars = 2 # Minimum upper case characters required in password
pwo.minlchars = 2 # Minimum lower case characters required in password
pwo.minnumbers = 2 # Minimum numbers required in password
pwo.minschars = 2 # Minimum special characters in the password

password_generated=pwo.generate() # Unique password generated

print("Password Generated= ",password_generated)
print()

#######################



####################### List all users

import sys  # For simplicity, we'll read config file from 1st CLI param sys.argv[1]
import json
import logging
import requests
import msal

# Optional logging
# logging.basicConfig(level=logging.DEBUG)

# config = json.load(open(sys.argv[1]))

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(config["client_id"], authority=config["authority"],client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )
# result = None
# result = app.acquire_token_silent(config["scope"], account=None)
# if not result:
#     logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
#     result = app.acquire_token_for_client(scopes=config["scope"])
# if "access_token" in result:
#     # Calling graph using the access token
#     graph_data = requests.get(  # Use token to call downstream service
#         config["endpoint"],
#         headers={'Authorization': 'Bearer ' + result["access_token"]}).json()
#     print("Graph API call result: ")
#     print(json.dumps(graph_data, indent=2))
# else:
#     print(result.get("error"))
#     print(result.get("error_description"))
#     print(result.get("correlation_id"))  # You may need this when reporting a bug

# print("Graph length",len(graph_data['value']))
# print("Typeof",type(graph_data['value']))

# print()
#####################################



###################################### Create new users

endpoint_new_user= "https://graph.microsoft.com/v1.0/users"

result = None
result = app.acquire_token_silent(config["scope"], account=None)
if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])
if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.post(  # Use token to call downstream service
        endpoint_new_user,
        headers={'Authorization': 'Bearer ' + result["access_token"],'Content-Type':'application/json'},


        data=json.dumps({
        "accountEnabled": True,
        # "city": "Seattle",
        "country": country_of_residence,
        "department": department,
        "displayName": first_name,
        "givenName": first_name,
        "jobTitle": job_title,
        "mailNickname": first_name,
        "passwordPolicies": "DisablePasswordExpiration",
        "passwordProfile": {
             "forceChangePasswordNextSignIn": True,
             "forceChangePasswordNextSignInWithMfa": True,
             "password": password_generated
        },
        "officeLocation": country_of_residence,
        # "postalCode": "98052",
        # "preferredLanguage": "en-US",
        # "state": "WA",
        # "streetAddress": "9256 Towne Center Dr., Suite 400",
        "surname": last_name,
        "mobilePhone": mobile_number,
        "usageLocation": "US",
        "userPrincipalName": email_id_of_joinee,
        "mail":email_id_of_joinee,
        }
        )
        
        )
    print("Graph API call result: ")
    print(graph_data.text)
    # print(graph_data.status_code)
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug

print()

###########################

########################### Identifying manager azure object id using email id inputed by HR & object id of currently onboarded candidate

manager_email_id=manager_email_id                   ## Manager email id inputed by HR
onboarded_candidate_email_id=email_id_of_joinee     ## Onoarding Candiadte email id 

result = None
result = app.acquire_token_silent(config["scope"], account=None)
if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])
if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.get(  # Use token to call downstream service
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result["access_token"]}).json()
    # print("Graph API call result: ")
    # print(json.dumps(graph_data, indent=2))
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug

# print("Graph length",len(graph_data['value']))

manager_azure_object_id=""
onboarded_candidate_azure_object_id=""
onboarded_candidate_azure_givenName=""                             ## For Vanta fetched_givenName variable
onboarded_candidate_azure_surname=""                               ## For Vanta fetched_familyName variable

for user in graph_data['value']:
    if(user['userPrincipalName'] == manager_email_id):
        manager_azure_object_id=user['id']
        manager_name=user['displayName']
    if(user['userPrincipalName'] == onboarded_candidate_email_id):
       onboarded_candidate_azure_object_id=user['id']
       onboarded_candidate_name=user['displayName']
       onboarded_candidate_azure_givenName=user['givenName']
       onboarded_candidate_azure_surname=user['surname']

    

print("Manager name=",manager_name," Manager id=",manager_azure_object_id)
print("Onboarding candidate name=",onboarded_candidate_name," Onboarding candidate id=",onboarded_candidate_azure_object_id)

print()

###########################

########################### Adding manager of onboarding candidate

endpoint_new_user= f"https://graph.microsoft.com/v1.0/users/{onboarded_candidate_azure_object_id}/manager/$ref"   ## Azure object id of onboarded candidate

result = None
result = app.acquire_token_silent(config["scope"], account=None)
if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])
if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.put(  # Use token to call downstream service
        endpoint_new_user,
        headers={'Authorization': 'Bearer ' + result["access_token"],'Content-Type':'application/json'},


        data=json.dumps({
         "@odata.id": f"https://graph.microsoft.com/v1.0/users/{manager_azure_object_id}",                       ## Azure object id of manager
        }
        )
        
        )
    print("For assigning manager, if Graph API call is successful, response will be 204")
    print("Graph API call result: ")
    print(graph_data)
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug

print()

##############################

############################## Adding member to groups 

AiDashians_group_azure_object_id="4968bcfb-60d1-4be6-8bc0-e4f877534547"            # All users added to this group       [Microsoft 365 group type]
AiDash_India_group_azure_object_id="11e8ebee-55d3-4bfe-9d0d-6cc96fc52c50"          # All INDIA users added to this group [Microsoft 365 group type]




##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# # INDIA
# AiDash_India_All="0b984877-d3d1-4db2-abab-742817a21c08"           # Distribution list
# AiDash_India_group_azure_object_id="11e8ebee-55d3-4bfe-9d0d-6cc96fc52c50"               # Microsoft 365 group type

# india_group_list=[]
# india_group_list.append(AiDash_India)
# india_group_list.append(AiDash_India_All)
# # india_group_list.append(AiDash_India)

# # US
# AiDash_US_All="d006ddef-da9f-4fc7-9d49-f5eabecd572c"              # Distribution list

# us_group_list=[]
# us_group_list.append(AiDash_US_All)

# # UK
# AiDash_UK_All="efc41b84-34f6-40e7-b086-1eca139be15a"              # Distribution list

# uk_group_list=[]
# uk_group_list.append(AiDash_UK_All)
##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX




# ADDING ALL CANDIDATES TO "AiDashians" GROUP [Microsoft 365 group type]

endpoint_add_user_to_group= f"https://graph.microsoft.com/v1.0/groups/{AiDashians_group_azure_object_id}/members/$ref"     # Group id

result = None
result = app.acquire_token_silent(config["scope"], account=None)
if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])
if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.post(  # Use token to call downstream service
        endpoint_add_user_to_group,
        headers={'Authorization': 'Bearer ' + result["access_token"],'Content-Type':'application/json'},


        data=json.dumps({
         "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{onboarded_candidate_azure_object_id}",    # onboarded_candidate_azure_object_id
        }
        )
        
        )
    print("For 'AiDashians' group, if Graph API call is successful, response will be 204")
    print("Graph API call result: ")
    print(graph_data)
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug

print()


## ADDING INDIA CANDIDATE TO "AiDash_India" GROUP [Microsoft 365 group type]

if(country_of_residence=="India"):
    endpoint_add_user_to_group= f"https://graph.microsoft.com/v1.0/groups/{AiDash_India_group_azure_object_id}/members/$ref"     # Group id

    result = None
    result = app.acquire_token_silent(config["scope"], account=None)
    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=config["scope"])
    if "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.post(  # Use token to call downstream service
            endpoint_add_user_to_group,
            headers={'Authorization': 'Bearer ' + result["access_token"],'Content-Type':'application/json'},


            data=json.dumps({
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{onboarded_candidate_azure_object_id}",    # onboarded_candidate_azure_object_id
            }
            )
            
            )
        print("For'AiDash_India' group, if Graph API call is successful, response will be 204")
        print("Graph API call result: ")
        print(graph_data)
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug

    print()




##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# ## ADDING CANDIDATE TO GROUP ACCORDING TO ORIGIN OF COUNTRY

# country=country_of_residence

# group_list=[]

# if(country=="India"):
#     group_list=india_group_list
# elif(country=="US"):
#     group_list=us_group_list
# elif(country=="UK"):
#     group_list=uk_group_list


# for group_azure_object_id in group_list:

#     endpoint_add_user_to_group= f"https://graph.microsoft.com/v1.0/groups/{group_azure_object_id}/members/$ref"        # Group object id

#     result = None
#     result = app.acquire_token_silent(config["scope"], account=None)
#     if not result:
#         logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
#         result = app.acquire_token_for_client(scopes=config["scope"])
#     if "access_token" in result:
#         # Calling graph using the access token
#         graph_data = requests.post(  # Use token to call downstream service
#             endpoint_add_user_to_group,
#             headers={'Authorization': 'Bearer ' + result["access_token"],'Content-Type':'application/json'},


#             data=json.dumps({
#             "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{onboarded_candidate_azure_object_id}",   # onboarded_candidate_azure_object_id
#             }
#             )
            
#             )
#         print("Graph API call result: ")
#         print(graph_data.text)
#     else:
#         print(result.get("error"))
#         print(result.get("error_description"))
#         print(result.get("correlation_id"))  # You may need this when reporting a bug

# print()


# ##############################

##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


############################## Create delay to let new user sync with Azure AD

import time
time.sleep(300)

##############################


############################## Retrieve Distribution List from aidash_distribution_list_with_managers.py file
import json


f = open("aidash_distribution_list_with_managers.py", "r")
x=json.loads(f.read())
 

## retriving distribution list name using manager email id
distribution_list_names=[]   # Distribution list name in which user is added based on manager

for item in x:
    # print(item['Manager'])
    if(manager_email_id in item['Manager'] and department==item['department']):
        for data in item['location_group']:
            # print(data['location'],"  ",data['distribution_list_name'])
            if(country_of_residence==data['location']):
                distribution_list_names=data['distribution_list_name']
                break

## print("Distribution list names",distribution_list_names)

##############################

############################## Add users to distribution list via powershell

for dl_name in distribution_list_names:

    import subprocess


    def run(self, cmd):
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        return completed

    ### Here prateek.verma@aidash.com is Email id of admin of microsoft 365

    if __name__ == '__main__':
        command = f'''Connect-ExchangeOnline -UserPrincipalName prateek.verma@aidash.com      
                        Add-DistributionGroupMember -Identity "{dl_name}" -Member "{email_id_of_joinee}"'''
        info = run(command,command)
        if info.returncode != 0:
            print("An error occured: %s", info.stderr)
        else:
            print("User added to ",dl_name," successfully!")


##############################

############################## Sending mail at personal email id of joinee with Microsoft Office account login credentials

import requests

url = 'https://prod-172.westus.logic.azure.com:443/workflows/531ededc34e2471cb7d76b61dbca6e8f/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Is7MMO5HHUD_oZBChOC9VRvzEk1NQvIn-NYrjWReRug'

myjson = {
"subject":"Aidash`s Microsoft Office account login credentials",

"body":f'''
<h3>Hi {first_name},</h3>
<h4>Welcome to Aidash.</h4>

<p><strong>Please click on the <a href="https://www.office.com/" target="_blank">link</a> to login to your Microsoft Office account with given credentials.</p>

<p>
<strong>Email ID: {email_id_of_joinee}</strong> 
 <br>
<strong>Password: {password_generated}</strong>  
</p>

<p><strong>
We wish you for a great journey ahead!
</p>
''',

"to":f"{joinee_personal_email_id};prateek.verma@aidash.com;prateek544verma@gmail.com"
}

x = requests.post(url, json = myjson)

## print the response text

print(x.text)
print("Check Power Automate flow named `onboarding automation [ Sending Microsoft office 365 initial credentials to newly onboarded candidate ]` to check status of sended email")


##############################




##****************************************************************************************************************************
#############################  VANTA PARTS BEGINS

import requests
import json

############################## Create delay to let new user data in Azure sync with Vanta

import time
time.sleep(10800)

##############################


####################################### Fetched data of onboarded candidate for Vanta group assigning

fetched_givenName=onboarded_candidate_azure_givenName
fetched_familyName=onboarded_candidate_azure_surname
fetched_user_vanta_group=f"{type_of_engagement}"

fetched_givenName="Prateek"
fetched_familyName="Verma"
fetched_user_vanta_group="FTE"


###################################### 


###################################### Fetch all Vanta users and extract onboarded candidate`s user id and start date

cookies = {
    '_cq_duid': '1.1653388595.qbc734d4IUTlVjy9',
    '_gcl_au': '1.1.1954965017.1653388597',
    '_rdt_uuid': '1653388599034.01e1c110-d0f6-4f17-b8c5-84184ac11266',
    '_ga': 'GA1.2.171947315.1653388599',
    'ajs_user_id': 'null',
    'ajs_group_id': 'null',
    'ajs_anonymous_id': '%221f0beb31-2cc6-436b-af97-c7d3d18916c6%22',
    'hubspotutk': 'b40cffa000fb415486543f87be3c5216',
    '__zlcmid': '1A8kwslbU4ttZff',
    '__q_state_875gDyGoGBpbHL2d': 'eyJ1dWlkIjoiY2IzMGY1MDYtMWY1NC00YjA4LWE5YjAtMDhjN2EwNDA5MjZiIiwiY29va2llRG9tYWluIjoidmFudGEuY29tIn0=',
    '_cq_suid': '1.1653406993.Ld67YWmS2l0GJLNK',
    '__hstc': '148015400.b40cffa000fb415486543f87be3c5216.1653388600214.1653396093248.1653406998448.3',
    '__hssrc': '1',
    '_uetvid': '64da4a60db4d11ec9d5b097b8cf0dbb5',
    'connect.sid': 's%3AZpJKhb56NKYwRtWy6ABd6q1H0cNxCWYN.C3AmsOjUghm1qEi0iXy2GFlVdP%2Bz0P6%2BpL21G6Jlvn4',
    'csrf-token': 'b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699',
    '_hp2_ses_props.948124972': '%7B%22ts%22%3A1653902566340%2C%22d%22%3A%22app.vanta.com%22%2C%22h%22%3A%22%2Fbusiness-information%22%7D',
    '_hp2_id.948124972': '%7B%22userId%22%3A%22793242245338143%22%2C%22pageviewId%22%3A%226523634273766807%22%2C%22sessionId%22%3A%221498979338048076%22%2C%22identity%22%3A%2261ceac288d357312889235a4%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
    '_dd_s': 'rum=1&id=a9d2d9ca-4d33-4444-846f-1c31759f8c2f&created=1653902566183&expire=1653903695624',
}
headers = {
    'authority': 'app.vanta.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'apollographql-client-version': 'b6fb99',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_cq_duid=1.1653388595.qbc734d4IUTlVjy9; _gcl_au=1.1.1954965017.1653388597; _rdt_uuid=1653388599034.01e1c110-d0f6-4f17-b8c5-84184ac11266; _ga=GA1.2.171947315.1653388599; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%221f0beb31-2cc6-436b-af97-c7d3d18916c6%22; hubspotutk=b40cffa000fb415486543f87be3c5216; __zlcmid=1A8kwslbU4ttZff; __q_state_875gDyGoGBpbHL2d=eyJ1dWlkIjoiY2IzMGY1MDYtMWY1NC00YjA4LWE5YjAtMDhjN2EwNDA5MjZiIiwiY29va2llRG9tYWluIjoidmFudGEuY29tIn0=; _cq_suid=1.1653406993.Ld67YWmS2l0GJLNK; __hstc=148015400.b40cffa000fb415486543f87be3c5216.1653388600214.1653396093248.1653406998448.3; __hssrc=1; _uetvid=64da4a60db4d11ec9d5b097b8cf0dbb5; connect.sid=s%3AZpJKhb56NKYwRtWy6ABd6q1H0cNxCWYN.C3AmsOjUghm1qEi0iXy2GFlVdP%2Bz0P6%2BpL21G6Jlvn4; csrf-token=b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699; _hp2_ses_props.948124972=%7B%22ts%22%3A1653902566340%2C%22d%22%3A%22app.vanta.com%22%2C%22h%22%3A%22%2Fbusiness-information%22%7D; _hp2_id.948124972=%7B%22userId%22%3A%22793242245338143%22%2C%22pageviewId%22%3A%226523634273766807%22%2C%22sessionId%22%3A%221498979338048076%22%2C%22identity%22%3A%2261ceac288d357312889235a4%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _dd_s=rum=1&id=a9d2d9ca-4d33-4444-846f-1c31759f8c2f&created=1653902566183&expire=1653903695624',
    'graphql-schema-version': 'b6fb99',
    'origin': 'https://app.vanta.com',
    'referer': 'https://app.vanta.com/people',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    'x-csrf-token': 'b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699',
}
json_data = {
    'operationName': 'fetchUsersForPeoplePage',
    'variables': {
        'utcOffset': 330,
        'withRoleData': True,
        'filters': {
            'includeNonHumanUsers': True,
            'includeRemovedUsers': True,
            'groupId': None,
            'auditId': None,
            'searchString': '',
        },
        'sortParams': {
            'field': 'name',
            'direction': -1,
        },
        'first': 10000,
    },
    'query': 'query fetchUsersForPeoplePage($first: Int!, $after: String, $sortParams: sortParams!, $filters: UserFilters!, $utcOffset: Int! = 0, $withRoleData: Boolean = false) {\n  organization {\n    id\n    audits(pastAudits: true) {\n      id\n      auditStart\n      auditType\n      auditPeriodDays\n      __typename\n    }\n    people(first: $first, after: $after, sortParams: $sortParams, filters: $filters, utcOffset: $utcOffset) {\n      totalCount\n      pageInfo {\n        startCursor\n        endCursor\n        hasNextPage\n        hasPreviousPage\n        __typename\n      }\n      edges {\n        node {\n          id\n          ...peoplePageFields\n          __typename\n        }\n        cursor\n        __typename\n      }\n      __typename\n    }\n    roles @include(if: $withRoleData) {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment peoplePageFields on User {\n  id\n  backgroundChecks {\n    id\n    service\n    completedAt\n    __typename\n  }\n  backgroundCheckDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  securityTrainingDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  gdprSecurityTrainingDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  hipaaSecurityTrainingDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  pciSecurityTrainingDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  employeesWithoutLaptopsDisabledStatus {\n    ...disabledStatus\n    __typename\n  }\n  createdAt\n  displayName\n  domain {\n    id\n    onboardingSla\n    __typename\n  }\n  email\n  endDate\n  endpointState\n  familyName\n  givenName\n  hasAcceptedAllSecurityPolicies\n  hasCompletedBackgroundCheck\n  hasCompletedSecurityTraining\n  hasOSQueryEndpoint\n  hrUser {\n    apolloId\n    endDate\n    jobTitle\n    service\n    startDate\n    uniqueId\n    __typename\n  }\n  inOnboardingSla\n  isActive\n  isContractor\n  isFromScan\n  isNotHuman\n  mostRecentGdprSecurityTraining {\n    completionDate\n    __typename\n  }\n  mostRecentHipaaSecurityTraining {\n    completionDate\n    __typename\n  }\n  mostRecentSecurityTraining {\n    completionDate\n    __typename\n  }\n  mostRecentPciSecurityTraining {\n    completionDate\n    __typename\n  }\n  needsEmployeeDigestReminder\n  onboardingCompletionDate\n  permissionLevel\n  requiresOffboarding\n  role {\n    id\n    name\n    __typename\n  }\n  roleCompletionRecord {\n    id\n    adminCompletionDate\n    employeeCompletionDate\n    hasNoTasks\n    __typename\n  }\n  securityTrainingCompletions {\n    category\n    completionDate\n    __typename\n  }\n  securityRequirements {\n    ...SecurityRequirementsMap\n    __typename\n  }\n  startDate\n  trainingRequirements {\n    id\n    externalURL\n    displayName\n    completionDate\n    service\n    vantaAttributes {\n      key\n      value\n      managedExternally\n      __typename\n    }\n    __typename\n  }\n  ...PeoplePageUserStatuses\n  __typename\n}\n\nfragment disabledStatus on DisabledUserTestEntityStatus {\n  disabledAt\n  reason\n  __typename\n}\n\nfragment SecurityRequirementsMap on securityRequirements {\n  mustAcceptPolicies\n  mustBeBackgroundChecked\n  mustCompleteGdprSecurityTraining\n  mustCompleteHipaaSecurityTraining\n  mustCompletePciSecurityTraining\n  mustCompleteSecurityTraining\n  mustInstallAntivirus\n  mustInstallLaptopMonitoring\n  mustInstallPasswordManager\n  __typename\n}\n\nfragment PeoplePageUserStatuses on User {\n  id\n  employmentStatus\n  taskStatus\n  taskStatusInfo {\n    status\n    dueDate\n    completionDate\n    __typename\n  }\n  __typename\n}\n',
}
response = requests.post('https://app.vanta.com/graphql', cookies=cookies, headers=headers, json=json_data)

print(json.dumps(json.loads(response.text),indent=2))
users_list=json.loads(response.text)['data']['organization']['people']['edges']

print(len(users_list))

fetched_userId=""
fetched_startDate=""

for user in users_list:
    if(user['node']['givenName'] == fetched_givenName and user['node']['familyName'] == fetched_familyName):
        fetched_userId = user['node']['id']
        fetched_startDate = user['node']['startDate']
        break
        
print("Fetched user id=",fetched_userId,"Fetched user start date=",fetched_startDate)


#######################################

####################################### Set onboarded candidate Vanta Group

## Vanta Groups IDs
Contractors_personal_laptop_vanta_group_id="611e53fa7488613324399607"
Contractors_company_laptop_vanta_group_id="622f6304f283c7aed87501fe"
FTEs_vanta_group_id="6125cce6a38ea94c5b67794c"
Interns_personal_laptop_vanta_group_id="6227347cfdcbf82ae8f44cd6"
Interns_company_laptop_vanta_group_id="620a2ca1e8b8f2976a04d9a9"

user_vanta_group_id=""

if(fetched_user_vanta_group=="Contractor-personal-laptop"):
    user_vanta_group_id=Contractors_personal_laptop_vanta_group_id
elif(fetched_user_vanta_group=="Contractor-company-laptop"):
    user_vanta_group_id=Contractors_company_laptop_vanta_group_id
elif(fetched_user_vanta_group=="FTE"):
    user_vanta_group_id=FTEs_vanta_group_id
elif(fetched_user_vanta_group=="Intern-personal-laptop"):
    user_vanta_group_id=Interns_personal_laptop_vanta_group_id
elif(fetched_user_vanta_group=="Intern-company-laptop"):
    user_vanta_group_id=Interns_company_laptop_vanta_group_id


cookies = {
    '_cq_duid': '1.1653388595.qbc734d4IUTlVjy9',
    '_gcl_au': '1.1.1954965017.1653388597',
    '_rdt_uuid': '1653388599034.01e1c110-d0f6-4f17-b8c5-84184ac11266',
    '_ga': 'GA1.2.171947315.1653388599',
    'ajs_user_id': 'null',
    'ajs_group_id': 'null',
    'ajs_anonymous_id': '%221f0beb31-2cc6-436b-af97-c7d3d18916c6%22',
    'hubspotutk': 'b40cffa000fb415486543f87be3c5216',
    '__zlcmid': '1A8kwslbU4ttZff',
    '__q_state_875gDyGoGBpbHL2d': 'eyJ1dWlkIjoiY2IzMGY1MDYtMWY1NC00YjA4LWE5YjAtMDhjN2EwNDA5MjZiIiwiY29va2llRG9tYWluIjoidmFudGEuY29tIn0=',
    '_cq_suid': '1.1653406993.Ld67YWmS2l0GJLNK',
    '__hstc': '148015400.b40cffa000fb415486543f87be3c5216.1653388600214.1653396093248.1653406998448.3',
    '__hssrc': '1',
    '_uetvid': '64da4a60db4d11ec9d5b097b8cf0dbb5',
    'connect.sid': 's%3AZpJKhb56NKYwRtWy6ABd6q1H0cNxCWYN.C3AmsOjUghm1qEi0iXy2GFlVdP%2Bz0P6%2BpL21G6Jlvn4',
    'csrf-token': 'b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699',
    '_hp2_ses_props.948124972': '%7B%22ts%22%3A1653905760883%2C%22d%22%3A%22app.vanta.com%22%2C%22h%22%3A%22%2Fpeople%22%7D',
    '_hp2_id.948124972': '%7B%22userId%22%3A%22793242245338143%22%2C%22pageviewId%22%3A%222448606818806675%22%2C%22sessionId%22%3A%224839332359864252%22%2C%22identity%22%3A%2261ceac288d357312889235a4%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
    '_dd_s': 'rum=1&id=a9d2d9ca-4d33-4444-846f-1c31759f8c2f&created=1653902566183&expire=1653908278865',
}

headers = {
    'authority': 'app.vanta.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'apollographql-client-version': 'b6fb99',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_cq_duid=1.1653388595.qbc734d4IUTlVjy9; _gcl_au=1.1.1954965017.1653388597; _rdt_uuid=1653388599034.01e1c110-d0f6-4f17-b8c5-84184ac11266; _ga=GA1.2.171947315.1653388599; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%221f0beb31-2cc6-436b-af97-c7d3d18916c6%22; hubspotutk=b40cffa000fb415486543f87be3c5216; __zlcmid=1A8kwslbU4ttZff; __q_state_875gDyGoGBpbHL2d=eyJ1dWlkIjoiY2IzMGY1MDYtMWY1NC00YjA4LWE5YjAtMDhjN2EwNDA5MjZiIiwiY29va2llRG9tYWluIjoidmFudGEuY29tIn0=; _cq_suid=1.1653406993.Ld67YWmS2l0GJLNK; __hstc=148015400.b40cffa000fb415486543f87be3c5216.1653388600214.1653396093248.1653406998448.3; __hssrc=1; _uetvid=64da4a60db4d11ec9d5b097b8cf0dbb5; connect.sid=s%3AZpJKhb56NKYwRtWy6ABd6q1H0cNxCWYN.C3AmsOjUghm1qEi0iXy2GFlVdP%2Bz0P6%2BpL21G6Jlvn4; csrf-token=b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699; _hp2_ses_props.948124972=%7B%22ts%22%3A1653905760883%2C%22d%22%3A%22app.vanta.com%22%2C%22h%22%3A%22%2Fpeople%22%7D; _hp2_id.948124972=%7B%22userId%22%3A%22793242245338143%22%2C%22pageviewId%22%3A%222448606818806675%22%2C%22sessionId%22%3A%224839332359864252%22%2C%22identity%22%3A%2261ceac288d357312889235a4%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _dd_s=rum=1&id=a9d2d9ca-4d33-4444-846f-1c31759f8c2f&created=1653902566183&expire=1653908278865',
    'graphql-schema-version': 'b6fb99',
    'origin': 'https://app.vanta.com',
    'referer': 'https://app.vanta.com/people?userId=6290b469b21b7e854a5255c7',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    'x-csrf-token': 'b423edbeb55186adc32916ca0528c7cb2fe64fd2c75ba2eed17d07a1550c2699',
}

json_data = {
    'operationName': 'setUserDetails',
    'variables': {
        'input': {
            'userId': fetched_userId,
            'familyName': fetched_familyName,
            'givenName': fetched_givenName,
            'startDate': fetched_startDate,
            'roleId': user_vanta_group_id,
        },
    },
    'query': 'mutation setUserDetails($input: SetUserDetailsInput!) {\n  setUserDetails(input: $input) {\n    ... on SetUserDetailsSuccess {\n      user {\n        id\n        displayName\n        familyName\n        givenName\n        role {\n          id\n          __typename\n        }\n        startDate\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
}

response = requests.post('https://app.vanta.com/graphql', cookies=cookies, headers=headers, json=json_data)

print("Set user=",json.dumps(json.loads(response.text),indent=2))

#######################################








############################# VANTA PART ENDS
##******************************************************************************************************************************