import urllib
import json
import itertools
import collections
import time

#PORT_NUMBER = '80'
PORT_NUMBER = ''
CACHE_SERVER = 'http://192.168.50.131'
MODALITY = 'ccserverae'

flow = [{'url':'find-patient','attribs':['']},
        {'url':'find-patient','attribs':['PatientID']},
        {'url':'find-study','attribs':['PatientID']},
        {'url':'find-study','attribs':['PatientID', 'StudyInstanceUID']},
        {'url':'find-series','attribs':['PatientID', 'StudyInstanceUID']},
        {'url':'find-instance','attribs':['PatientID', 'StudyInstanceUID', 'SeriesInstanceUID']}]

def check(prev_result, definition):
    print "-------------" + str(definition['attribs']) + "-------------"
#    print prev_result
#    print definition
    prev_result = list(itertools.chain.from_iterable(prev_result))
    to_check = [collections.OrderedDict((key, result[key]) for key in definition['attribs']) for result in prev_result]
#    print to_check
#    print dict((key, prev_result[0][key]) for key in definition['attribs'])

#    if more than 1 result, recurr

#    print "/////////////"
#    print to_check
#    print "+++++++++++++"

    m = map(lambda c: check_url(definition, c), to_check)
#    print m
    return m

def check_url(definition, check):
    print check
    params = urllib.urlencode(check)
    if len(params) <= 1:
        params = ''
    else:
        params = '?' + str(params)
    url = CACHE_SERVER + '/' + 'modalities/' + MODALITY + '/' + definition['url'] + params
    print url
    resp = urllib.urlopen(url).read()
    resp_arr = json.loads(resp)
#    print resp_arr
    print "Response length " + str(len(resp_arr))
    print "-------------" + "-------------" + "-------------"
    return resp_arr

if __name__ == '__main__':
#    check('modalities/' + MODALITY + '/' + 'find-patient')
    try:
        while(True):
            reduce(lambda results, definition: check(results, definition), [[[{'':''}]]] + flow)
            time.sleep(10)
    except KeyboardInterrupt:
        print ""
        print "bye"
        pass