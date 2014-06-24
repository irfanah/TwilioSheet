from pyquery import PyQuery as pq
import urllib
import urllib2
import re
import logging
import httplib

class GFormException(Exception):
    pass


class GForm:
    formkey = ''
    """String containing the value
       of the formkey GET paramater from a Google Form URL"""
    action_url = ''
    """String containing the URL value
       from the 'action' attribute of the <form> tag in a Google Form"""
    parameters = {}
    """Dictionary where the 'key' is the input name
       and the 'value' is the default value, if any"""
    labels = {}
    """Dictionary where the 'key' is the label
       for a Google Form input and the 'value' is the input name"""

    def __init__(self, formkey):

        """Given a Google Form 'formkey',
           will parse interesting information from said form."""
        form_url = "https://docs.google.com/forms/d/{0}/viewform".format(formkey)

        self.formkey = ''
        self.action_url = ''
        self.parameters = {}
        self.labels = {}

        try:
            html = pq(url=form_url)

        except Exception as inst:
            logging.warn(inst)
            raise GFormException("""Error parsing URL '%s', did you pass the correct formkey?""")

        form = html('#ss-form')
        self.action_url = form.attr['action']

        # Define parameters with default values, if any
        #for item in html('#ss-form input'):
        #    self.parameters[item.name] = item.value

        # Map out the label to form-input-name relationships
        for item in html.find('.ss-item.ss-text'):
            text_item = pq(item)
            input_label = text_item.find('.ss-q-title').text()
            input_id = text_item.find('input[type=\'text\']').attr('id')
            input_name = text_item.find('input[type=\'text\']').attr('name')
            input_value = text_item.find('input[type=\'text\']').val()

            #if (input_label != ""):
                #logging.warn(input_label)

            if (input_id != ""):
                #logging.warn(input_id)
                #logging.warn("Name: {0}".format( input_name ))
                #logging.warn("Value: {0}".format( input_value ))
                self.parameters[input_name] = input_value

            self.labels[input_label] = input_id

    def show_state(self):
        """Print the contents of the 'paramaters' and 'labels' properties"""

        print "Parameters:",
        print self.parameters
        print "Labels:",
        print self.labels

    def submit(self):
        """Submit the contents of the 'parameters' property
           to the Google Form"""

        f = urllib2.urlopen(self.action_url, urllib.urlencode(self.parameters))
        result = pq(f.read())
        message = result.find('.ss-resp-message').text()
        
        # http://bit.ly/12ySdJQ
        response = "<Response><!-- %s --></Response>" % message
        return response
