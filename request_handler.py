import requests,base64,sys
import yaml,log
import logger
conf = yaml.safe_load(open('./config/config_catchpoint.yaml'))
logger = log.get_logger(__name__,conf['log_file'],conf['log_level'])


class Catchpoint(object):
    def __init__(self):
        """
        Basic init method.
        """
        self.auth = False
        self.token = None
        self.expires_in = None
        self.verbose = False 


    def debug(self, msg):
        """
        Debug output. Set self.verbose to True to enable.
        """
        if self.verbose:
                logger.info(str(msg))


    def connection_error(e):
        msg = "Unable to reach {0}".format(e)
        sys.exit(msg)
        
    def authorize(self,creds):
        logger.info("Getting authorization token")
        """
        Request an auth token.
        creds :  Configuration file with requred credentails in key, value pair
        """

        uri = '{0}://{1}/{2}'.format(creds['protocol'],creds['domain'],creds['token_endpoint'])
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'refresh_token': creds['refresh_token'],
            'grant_type': 'client_credentials',
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret']
        }    
        try:
            response = requests.post(uri, headers=headers,data=payload,verify=False) 
        except Exception as e:
            logger.exception(str(e))

        data = response.json()
        if 'message' in data:
            logger.exception(data['message'])
        self.token = data['access_token']
        self.expires_in = data['expires_in']
        self.auth = True
        ## 
        ## 	obtain a token before calling the API for the first time
        ## 	the token is valid for 15 minutes
        ##
    
    def fetch_data(self,creds):
       
        """
        Make a request with an auth token.
        creds :  Configuration file with requred credentails in key, value pair
        """
        logger.info("calling API with the token")
         
        uri = '{0}://{1}/{2}/{3}={4}'.format(creds['protocol'],creds['domain'],creds['version'],creds['rawdata_endpoint'],creds['test_id_params'])
        payload = ""
        headers = {
                    'Accept': 'application/json',
                    'Authorization': "Bearer " + base64.b64encode(

                        self.token.encode('ascii')

                    ).decode("utf-8")
            }

        try:
            response = requests.get(uri, headers=headers, data=payload)
            if response.status_code != 200:
                self.debug("The response is "+str(response.content))	
                self.debug("there was some error"+str(response))
            if response.status_code == 401:
                self.authorize(self,creds)
                response = requests.get(uri, headers=headers, data=payload)
        except requests.ConnectionError as e:
            self.debug(str(e))
            self.connection_error(e)

        try:
            response_data = response.json()
        except TypeError as e:
            return e
        return response_data
       

    def expired_token_check(self,data):
            """
            Determine whether the token is expired. While this check could
            technically be performed before each request, it's easier to offload
            retry logic onto the script using this class to avoid too many
            req/min.
            - data: The json data returned from the API call.
            """
            if "Message" in data:
                if data['Message'].find("Expired token") != -1:
                    self.debug("Token was expired and has been cleared, try again...")
                    self.token = None
                    self.auth = False
                    return True
    