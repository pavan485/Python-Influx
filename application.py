import logger
import yaml
import request_handler
import utils,log,time
conf = yaml.safe_load(open('./config/config_catchpoint.yaml'))
logger = log.get_logger(__name__,conf['log_file'],conf['log_level'])
class Application(object):
    

    def __init__(self):
        self.__request_handler = request_handler.Catchpoint()

    def batch(self,iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    def run(self):
        while True:
            try:
                self.__request_handler.authorize(conf)
                for test_id_type in conf['test_ids'].values():
                    final_list = []
                    for test_id in self.batch(test_id_type, conf['batch_size']):
                        conf['test_id_params']=",".join(test_id)
                        data = self.__request_handler.fetch_data(conf)
                        expired = self.__request_handler.expired_token_check(data)

                        if expired is True:
                            self.__request_handler.authorize(conf)
                            data = self.__request_handler.fetch_data(conf) 
                        parsed_json = utils.Utils.parse_raw(data)
                        if final_list is []:
                            final_list=parsed_json
                        else:
                            if parsed_json:
                                final_list.extend(parsed_json)
                        logger.info(final_list)
                    if final_list is not None:
                        utils.Utils.insert_to_influx(final_list)
                    else:
                        logger.exception('No Data')
                time.sleep(900000)
            except Exception as e:
                logger.exception(str(e))
            
     
if __name__ == '__main__':
    if not utils.Utils.validate_configurations():
        raise RuntimeError('missing configrations')
    Application().run()
