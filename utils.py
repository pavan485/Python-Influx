import yaml
import log
import pymongo
import dateutil.parser as dp
from influxdb_client.client.write_api import SYNCHRONOUS
creds = yaml.safe_load(open('./config/config_mongo.yaml'))
conf = yaml.safe_load(open('./config/config_catchpoint.yaml'))
logger = log.get_logger(__name__,conf['log_file'],conf['log_level'])


class Utils():
    @staticmethod
    def parse_raw(structure):
        logger.info("Parsing data for InfluxDB")
        synthetic_metrics = []
        if 'error' in structure:
            logger.error(structure['error'])
        if 'detail' not in structure:
            logger.error('No data available')
            return None    
        test_params = []
        final_list = [] #list of all jsons
        synthetic_metrics = structure['detail']['fields']['synthetic_metrics']
        
        for i in synthetic_metrics:
            metrics = i['name']
            test_params.append(metrics)
        
        for value in structure['detail']['items']:
            values = {} # json which contains tags fields time 
            
            
            values['breakdown_1'] = value['breakdown_1']['name']
            values['breakdown_2'] = value['breakdown_2']['name']
            if 'step' in value:
                values['step'] = value['step']
            if 'hop_number' in value:
                values['hop_number'] = value['hop_number']
        
            
            values['time_stamp'] = dp.parse(value['dimension']['name']).timestamp()*1000000

            metric_values = value['synthetic_metrics']
            fields = {}
            for i in range(0,len(metric_values),1):
                fields[test_params[i]]=metric_values[i]
            values['metrics'] = fields
            final_list.append(values)
        logger.info(final_list)
        return final_list
                
        

        

    @staticmethod
    def write_data(data):
        logger.info("Pushing data to mongodb")
        database = creds['database']
        collection = creds['collection']
        
        url = creds['mongo_url']
        try:
        
            myclient = pymongo.MongoClient(url)
            mydb = myclient[database]
            mycol = mydb[collection]

            result = mycol.insert_many(data)
            logger.info("Documents were inserted")
        
        except Exception as e:
            logger.exception(str(e))
            logger.exception('Error while writing data')


    @staticmethod
    def validate_configurations():
        if 'client_id' not in conf or conf['client_id'] is None:
            return False
        if 'client_secret' not in conf or conf['client_secret'] is None:
            return False
        if 'protocol' not in conf or conf['protocol'] is None: 
            return False
        if 'domain' not in conf or conf['domain'] is None:
            return False 
        if 'token_endpoint' not in conf or conf['token_endpoint'] is None: 
            return False
        if 'rawdata_endpoint' not in conf or conf['rawdata_endpoint'] is None:
            return False
        return True
