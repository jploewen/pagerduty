# pagerduty
#
# This is prototype code to calculate MTTR and MTTA for a given Service 
# The required input is an api key for the pager duty account
# python listIncidents.py --token <token>
#
# Current implementation is fixed for a specfic service_id and 30 day period
# Expected output is MTTR = 12 minutes (based on 16 incidents found), MTTA = 2 minutes
# --- Actual results are MTTR = 11 minutes, MTTA = 0 minutes 
