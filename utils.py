import influxdb_client
import yaml
import log
from influxdb_client.client.write_api import SYNCHRONOUS
creds = yaml.safe_load(open('./config/influx_config.yaml'))
conf = yaml.safe_load(open('./config/config.yaml'))
logger = log.get_logger(__name__,conf['log_file'],conf['log_level'])


class Utils():
    @staticmethod
    def parse_raw(structure):
        logger.info("Parsing data for InfluxDB")
        if structure is not None:    
            test_params = []
            final_list = [] #list of all jsons
            if 'detail' and 'fields' and 'synthetic_metrics' not in structure:
                return None
            synthetic_metrics = structure['detail']['fields']['synthetic_metrics']

        for i in synthetic_metrics:
            metrics = i['name']
            test_params.append(metrics)
        try:
            for value in structure['detail']['items']:
                values = {} # json which contains tags fields time 
                values['measurement'] =  'raw_data'
                tag = {
                    'data_timestamp' : value['dimension']['name'],
                    'breakdown_1' : value['breakdown_1']['name'],
                    'breakdown_2' : value['breakdown_2']['name']
                }
                values['tags'] = tag
                values['time'] = value['dimension']['name']
                metric_values = value['synthetic_metrics']
                fields = {}
                for i in range(0,len(metric_values),1):
                    fields[test_params[i]]=metric_values[i]
                values['fields'] = fields
                final_list.append(values)
                logger.info(final_list)
                return final_list
                
        except Exception as e:
            logger.exception(str(e))

        

    @staticmethod
    def insert_to_influx(data):
        logger.info("Pushing data to Influx")
        token = creds['token']
        org = creds['org']
        bucket = creds['bucket']
        url = creds['influx_url']
        try:
        #todo try catch
            client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
                )
            #todo null
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket, org, data)
            query = f'from(bucket: \"{bucket}\") |> range(start: -1h)'
            tables = client.query_api().query(query, org=org)
        
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