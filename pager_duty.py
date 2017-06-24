import json
import sys
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

#astro admin
class pagerDutyAPI:

	# https://api.pagerduty.com/incidents?time_zone=UTC&since=2017-04-17T04%3A31%3A52Z&statuses[]=resolved&serviceids[]=PZ6ZVSY&urgencies[]=high&offset=25

	base_url = 'api.pagerduty.com/'
	
	
	def __init__(self, token=None):
		

		self.base_url = 'https://' + 'api.pagerduty.com/'
		
		self.headers = {
			'Accept': 'application/vnd.pagerduty+json;version=2',
			'Authorization' : 'Token token=' + token
		}
		

	def listIncidents(self, service_ids='PZ6ZVSY', offset=0, limit=25):
		
		# https://api.pagerduty.com/incidents?time_zone=UTC&since=2017-04-17T04%3A31%3A52Z&statuses[]=resolved&serviceids[]=PZ6ZVSY&urgencies[]=high&offset=25

		url = self.base_url + 'incidents?time_zone=EST&since=2017-05-23T04%3A31%3A52Z&until=2017-06-23T05%3A31%3A52Z&statuses[]=resolved&urgencies[]=high' + '&service_ids[]=' + service_ids + '&offset=' + str(offset) + '&limit=' + str(limit)
		
		#print url
		
		rsp = requests.get(url, headers=self.headers, verify=True)
		
		#Let the user know how it went
		#print rsp

		#print 'Response Code: %d' % (rsp.status_code)
		if (rsp.status_code == 400):
			print 'Bad data'
			exit(-1)
		
		#Return the JSON data
		return rsp.json()
		
	def getLogEntries(self, incident_id=None):
		
		# https://api.pagerduty.com/incidents?time_zone=UTC&since=2017-04-17T04%3A31%3A52Z&statuses[]=resolved&serviceids[]=PZ6ZVSY&urgencies[]=high&offset=25

		url = self.base_url + '/incidents/' + incident_id + '/log_entries'
		
		#print url
		
		rsp = requests.get(url, headers=self.headers, verify=True)
		
		#Let the user know how it went
		#print rsp

		#print 'Response Code: %d' % (rsp.status_code)
		if (rsp.status_code == 400):
			print 'Bad data'
			exit(-1)
		
		#Return the JSON data
		return rsp.json()
	