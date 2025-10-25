from dotenv import load_dotenv

from agents.standard import StandardAgent

# Load environment variables
load_dotenv()

fraud_data = """
My company LLC INVOICE
ABN :####123
my company llc
ACT ,  Australia
Mob : 00000000
Email : mycompany@gmail.com
BILL TO
NATIONAL DISABILITY INSURANCE
GPO BOX : 7200 CANBERRA, ACT 2601 Phone :
1800 800 110
INVOICE# DATE
#23 2020-04-17
SL.NO ITEM QTY UNIT AUD TOTAL
1Access Community, Social And Rec
Activities - Level 1 - Evening
Line Item Code : 04_301_0104_1_11 H 58.31 58.31
SUB TOTAL 58.31
TAX 0%
GRAND TOTAL 58.31
Notes
Thank you for your business
Page 1/1
"""

real_data = """

* A full list of codes and description of these line items can be found in the Price Guide of the NDIS, available at 
https://www.ndis.gov.au/providers/pricing -and-payment.html  Sparkling Home  Services  
ABN: 99 999 999 9999  INVOICE  

3 Example D rive 
Melbourne  Vic 3030  
sparkle@ example .com  
Telephone: 03 1234 5678  
 INVOICE NO. 34 
DATE : 05/10/2018  
TO: 
Edward Example  
C/- Plan Partners  
P.O. Box 131  
Richmond  VIC 3121 
invoice@planpartners.com.au  


DATE  DESCRIPTION  NDIS SUPPORT  
LINE ITEM*  HOURS  RATE  
(GST 
INCLUSIVE)  AMOUNT  
(INCLUSIVE 
OF GST)  
03/10/2018  House cleaning  01_020_0120_1_1  3 41.43  124.29  
03/10/2018  Lawn mowing (yard 
maintenance)  01_019_0120_1_1  2 46.20  92.4 







    GST Included  19.69  
   INVO ICE TOTAL  216.69  
PLEASE MAKE THE PAYMENT TO:  

SPARKL ING HOME  SERVICES  
BSB: 111-111 
ACCOUNT NUMBER:  111111 11
"""

if __name__ == "__main__":
    agent = StandardAgent(
        model="gpt-4o-mini"
    )
    result = agent.process(fraud_data)
    print(f"Is Valid: {result.is_valid}")
    print(f"Reason: {result.reason}")
