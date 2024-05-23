import logging
import sys
import time

import requests
import yaml

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':

    time_start = time.time()
    logger.info('Starting Source Sync')

    scripts: dict[str, dict[str, str]] = yaml.safe_load(open('source.yml', 'r'))

    counter = 0

    for folder, source in scripts.items():
        logger.info(f'Processing {folder}')

        file_extension = source.get('extension', '')

        logger.debug(f'Given File extension: {file_extension}')

        for file_name, url in source.items():
            if file_name == 'extension':
                continue

            logger.info(f'Downloading {file_name} from {url}')
            response = requests.get(url)

            with open(f'{folder}/{file_name}.{file_extension}', 'wb') as file:
                file.write(response.content)

            counter += 1

    time_end = time.time()
    logger.info(f'Processed {counter} files in {time_end - time_start} seconds')
