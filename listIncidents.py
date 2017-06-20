from __future__ import division
import json
import sys
import requests
from pager_duty import pagerDutyAPI
import time
import dateutil.parser
import argparse
from pprint import pprint

def ttr(created_at, resolved_at):
    create_date = dateutil.parser.parse(created_at)
    resolved_date = dateutil.parser.parse(resolved_at)
    age_seconds = (resolved_date - create_date).total_seconds()
    return age_seconds/60

def serviceMTTR1(token): 

    total = 0   
    resolved = 0
    acknowledged = 0
    incident_count = 0
    total_ttr_min = 0
    
    pd_admin = pagerDutyAPI(token)

    more = True
    offset = 0
    limit = 100

    while(more==True and total<5000):

        rsp_json = pd_admin.listIncidents(service_ids='P9I0XO1', offset=offset, limit=limit)
        my_service_id = 'P9I0XO1'
        
        incidents = rsp_json['incidents']
        for incident in incidents:    
            
            total += 1

            if (incident['status']=="resolved"):
                resolved += 1

            service = incident['service']
            if service['id']==my_service_id:
                incident_ttr = ttr(incident['created_at'], incident['last_status_change_at'])
                total_ttr_min += incident_ttr
                print "Incident number %s created at %s was resolved at %s (TTR = %d minutes)" % (incident['incident_number'], incident['created_at'], incident['last_status_change_at'], incident_ttr)
                incident_count += 1
                #print json.dumps(incident, indent=4, sort_keys=True)

            acks = incident['acknowledgements']

        print 'Incident Summary: total = %d, resolved = %d, my_service = %d' % (total, resolved, incident_count)
        #print '  Pagenation: limit = %d, offset = %d, more = %s' % (rsp_json['limit'], rsp_json['offset'], rsp_json['more'])
        
        offset = rsp_json['offset'] + limit
        more = bool(rsp_json['more'])

    print 'MTTR for Service %s = %d minutes over %d days (%d incidents)' % ("Developer and Team Insights", total_ttr_min/incident_count, 30, incident_count)
    
def serviceMTTR2(token): 

    total = 0   
    resolved = 0
    acknowledged = 0
    incident_count = 0
    total_ttr_min = 0
    
    pd_admin = pagerDutyAPI(token)

    more = True
    offset = 0
    limit = 100

    while(more==True and total<5000):

        rsp_json = pd_admin.listIncidents(service_ids='P9I0XO1', offset=offset, limit=limit)
        my_service_id = 'P9I0XO1'
        
        incidents = rsp_json['incidents']
        for incident in incidents:    
            
            total += 1

            if (incident['status']=="resolved"):
                resolved += 1

            service = incident['service']
            if service['id']==my_service_id:
                le_rsp = pd_admin.getLogEntries(incident['id'])
                log_entries = le_rsp['log_entries']
                for log_entry in log_entries:
                    if (log_entry['type']=='trigger_log_entry'):
                        created_at = log_entry['created_at']
                    if (log_entry['type']=='resolve_log_entry'):
                        resolved_at = log_entry['created_at']   
                incident_ttr = ttr(created_at, resolved_at)
                total_ttr_min += incident_ttr
                print "Incident number %s created at %s was resolved at %s (TTR = %d minutes)" % (incident['incident_number'], created_at, resolved_at, incident_ttr)
                incident_count += 1
                #print json.dumps(incident, indent=4, sort_keys=True)

            acks = incident['acknowledgements']

        print 'Incident Summary: total = %d, resolved = %d, my_service = %d' % (total, resolved, incident_count)
        #print '  Pagenation: limit = %d, offset = %d, more = %s' % (rsp_json['limit'], rsp_json['offset'], rsp_json['more'])
        
        offset = rsp_json['offset'] + limit
        more = bool(rsp_json['more'])

    print 'MTTR for Service %s = %d minutes over %d days (%d incidents)' % ("Developer and Team Insights", total_ttr_min/incident_count, 30, incident_count)

    
def serviceMTTA(token): 

    total = 0   
    acknowledged = 0
    incident_count = 0
    total_tta_min = 0
    
    pd_admin = pagerDutyAPI(token)

    more = True
    offset = 0
    limit = 100

    while(more==True and total<5000):

        rsp_json = pd_admin.listIncidents(service_ids='P9I0XO1', offset=offset, limit=limit)
        my_service_id = 'P9I0XO1'
        
        incidents = rsp_json['incidents']
        for incident in incidents:    
            
            total += 1

            service = incident['service']
            if service['id']==my_service_id:
                acked_at = None
                incident_tta = 0
                le_rsp = pd_admin.getLogEntries(incident['id'])
                log_entries = le_rsp['log_entries']
                for log_entry in log_entries:
                    if (log_entry['type']=='trigger_log_entry'):
                        created_at = log_entry['created_at']
                    if (log_entry['type']=='ack_log_entry'):
                        acked_at = log_entry['created_at'] 
                if (acked_at!=None):
                    acknowledged += 1  
                    incident_tta = ttr(created_at, acked_at)
                    total_tta_min += incident_tta
                    print "Incident number %s created at %s was acknowledged at %s (TTA = %d minutes)" % (incident['incident_number'], created_at, acked_at, incident_tta)
                incident_count += 1
                #print json.dumps(incident, indent=4, sort_keys=True)

            #acks = incident['acknowledgements']

        print 'Incident Summary: total = %d, acknowledged = %d, my_service = %d' % (total, acknowledged, incident_count)
        #print '  Pagenation: limit = %d, offset = %d, more = %s' % (rsp_json['limit'], rsp_json['offset'], rsp_json['more'])
        
        offset = rsp_json['offset'] + limit
        more = bool(rsp_json['more'])

    print 'MTTA for Service %s = %d minutes over %d days (%d incidents)' % ("Developer and Team Insights", total_tta_min/incident_count, 30, incident_count)

#Parser for command line arguments
parser = argparse.ArgumentParser(description="A script that calculate MTTR and MTTA for a given service")

#Add an argument for the environment
parser.add_argument('-t', '--token',
                action="store", dest="token",
                help="Pager Duty api token", default=None)

#Parse the arguments
args = parser.parse_args()

if args.token== None:
    print "Pager Duty API token is required"

serviceMTTR1(args.token)  
serviceMTTR2(args.token)
serviceMTTA(args.token)
