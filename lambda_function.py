from __future__ import print_function
import json
import socket
import re
import boto3
import base64
import os
# Initialize client and list for WAF logs
client = boto3.client('wafv2')
# Define variables, WAF's name, scope and Id. Change these to match your WAF details
IPSetName = os.environ['IPSetName']
IPSetScope = os.environ['IPSetScope']
IPSetId = os.environ['IPSetId']
# Start processing logs

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        payloadUTF=payload.decode("UTF-8")
        waflogs = []
        wafDict = json.loads(payloadUTF)
        waflogs.append(wafDict)
        for rec in waflogs:
            for header in rec['httpRequest']['headers']:
                if (header['name'] == 'User-Agent') or (header['name'] == 'user-agent'):
                    val=str([header['value']])
#                   Check if UserAgent contains string Google or Bingbot
                    botG=re.search('[Gg]oogle', val)
                    botB=re.search('[Bb]ingbot', val)
#                   If UserAgent contains Google or Bingbot, start IP address verification              
                    if (botG != None) or (botB !=None):
#                       Forward and Reverse Lookup
                        flookup, faliases, fip = (socket.gethostbyaddr(rec['httpRequest']['clientIp']))
                        rlookup = (socket.getfqdn(flookup))
#                       Check if the fqdn end with one of google bot domains
                        domainG1=re.search('google.com$', (socket.getfqdn(rec['httpRequest']['clientIp'])))
                        domainG2=re.search('googlebot.com$', (socket.getfqdn(rec['httpRequest']['clientIp'])))
#                       Check if the fqdn end with one of msn bot domains
                        domainB1=re.search('search.msn.com$', (socket.getfqdn(rec['httpRequest']['clientIp'])))
#                       Check if condition matches as suggested by google and msn for a legit bots https://support.google.com/webmasters/answer/80553?hl=en, https://www.bing.com/webmaster/help/verifying-that-bingbot-is-bingbot-3905dc26 
                        if ((rec['httpRequest']['clientIp']) == rlookup) and (domainG1 != None) or (domainG2 != None) or (domainB1 !=None) :
                            print ("Found %s , a Real bot" % fip)
#                       Start blocking process if the bot is fake
                        else:
                            newipaddr = (rec['httpRequest']['clientIp'] + "/32")
                            print ("%s is a fake bot. Blocking it" % newipaddr)
#                           Get current ip-list and LockToken necessary for updating the list
                            get_list_response = client.get_ip_set(
                                Name=IPSetName,
                                Scope=IPSetScope,
                                Id=IPSetId
                                )
    
                            CurrentAddresses = (get_list_response['IPSet']['Addresses'])
                            Addressesl=CurrentAddresses
                            #print(CurrentAddresses)
                            if newipaddr in CurrentAddresses:
                                print('%s is already present!' % newipaddr)
                            else:
                                print('%s is not present!' % newipaddr)
                                Addressesl.append(newipaddr)
                                CurrentToken = (get_list_response['LockToken'])
                                NewAddresses = []
                                #Update the ip-list
                                update_list_response = client.update_ip_set(
                                    Name= IPSetName,
                                    Scope= IPSetScope,
                                    Id= IPSetId,
                                    Addresses=Addressesl,
                                    LockToken=CurrentToken
                                )
                                print (update_list_response)

        # Do custom processing on the payload here
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}