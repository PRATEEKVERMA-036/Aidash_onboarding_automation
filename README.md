Links:

Github: https://github.com/aidash/python-automation/tree/adhoc-prateek/onboarding_automation_script 

PowerAutomate: https://us.flow.microsoft.com/manage/environments/Default-13cee7a3-b15d-47d9-8f30-f5bd649e3967/flows/979da147-f105-47c2-802d-d3b2e8e11f6f/details

Azure application: Microsoft Azure (https://azure.microsoft.com/en-in)

Jenkin job: https://jenkins-new.aidash.org/view/Self-service/job/windows_ss_onboarding_automation/

Microsoft Graph APIs doc: Create User - Microsoft Graph v1.0 (https://learn.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0&tabs=http)

ExoShell doc: Connect to Exchange Online PowerShell (https://learn.microsoft.com/en-us/powershell/exchange/connect-to-exchange-online-powershell?view=exchange-ps)

Jenkins Windows_slave: https://jenkins-new.aidash.org/computer/Windows_slave/

Execute powershell from python: Executing PowerShell from Python • Jamie Phillips ! (https://www.phillipsj.net/posts/executing-powershell-from-python/#:~:text=Here%20is%20the%20complete%20file,run(hello_command)%20if%20hello_info.)

EC2 instance of Jenkins Window Slave (Rahul account): https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#InstanceDetails:instanceId=i-0c6f1a025a4eab87d



Overview:

Onboarding automation is a Jenkins job, that takes detail of new candidates as input and creates a new user of it in Azure Active DIrectory, adds him to respective Aidash groups based on the department, nationality, manager allotted, along with sending email on its personal email ID, regarding the credential of Microsoft Office account. 

Every time when a new member joins the company, all the onboarding work was done manually that includes creating a new Microsoft account, adding members to different teams groups, sending email for their MS office credentials, adding them to suitable github repos, adding them to Vanta groups etc.

I have done this task often and found it time consuming. I have gone through the documentation of the service involved in this process to create a roadmap to automate this process. It included Microsoft 365 Graph APIs, Microsoft Power Automate, Jenkins Job, Microsoft Exoshell, Vanta. After creating it, I myself suggested to my team manager to Automate Onboarding Process. He instantly found it efficient from the company's long term perspective and agreed upon.


There are 2 types of group in Azure Active Directory

Microsoft 365: These group can be controlled by Microsoft Graph API

Distribution: Since only Admin can handle these groups, so, they controlled by Powershell . Therefore, I have used ExoShell to add user (new candidate) to such type of groups. ExoShell specifically needs Windows OS, therefore I am using Jenkins Windows_slave and its EC2 instance for installing Exoshell and carrying out powershell tasks.

Therefore, I have used ExoShell to add users (new candidates) to such types of groups. ExoShell specifically needs Windows OS, therefore I have to create a Jenkins Windows_slave and its EC2 instance for installing Exoshell and carrying out powershell tasks. And then I had written Powershell commands in Python (with the help of a few blogs).


Process of connecting to Jenkins slave to Azure Active Directory Distribution groups:

1. Open the Jenkins Window Slave instance and open the Command prompt
2. Follow the instruction to connect the Windows workspace to Exchange Online PowerShell using this link: Connect to Exchange Online PowerShell 
3. After following instruction, write these command in command prompt                                                  
“Connect-ExchangeOnline -UserPrincipalName prateek.verma@aidash.com“                                                                     
Here, prateek.verma@aidash.com is the company email ID of person having admin access. You can use other person email id with condition that he should have Azure Admin Access
4. You will be redirected to the sign-in window, where after filling your credentials, you will be connected to Exoshell and can now execute command for Distribution groups
5. You can check it by running command “Get-EXOMailbox“ to list out all email id. You can also check out these filters at link: Filters in the EXO V2 module 


 

Process of connecting to Azure Active Directory Microsoft 365 groups:

1. Create a new application in Azure using this link Microsoft Azure 
2. It will fetch you secret token and client id.
3. Add permissions accordingly to your application depending on the type of tasks you want to execute
4. Use these credentials to execute graph APIs action on Azure Active directory
 

Process for sending mail to new candidate:

1. Micorsoft PowerAutomate is used to send credentials of newly created Microsoft Account at new candidate`s personal email id.

2. You can understand the process using these two link:

How to send Email using Web API in PowerApps Portal ->
Link:https://powerusers.microsoft.com/t5/Power-Apps-Portals/How-to-send-Email-using-Web-API-in-PowerApps-Portal/td-p/642915

Microsoft Flow Send Email from HTTP Request ->
Link:https://medium.com/@zaab_it/microsoft-flow-send-email-from-http-request-f6577ad46b2c
 

