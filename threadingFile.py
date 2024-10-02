import time

from dotenv import load_dotenv

from YamlExecutor import YamlExecutor

def main():
    load_dotenv()

    yaml_executor = YamlExecutor(
        pipeline_location='Pipelines/wiki_fin_scraper.yaml')

    scraping_start_time = time.time()
    # yaml_executor.start()
    #yaml_executor.process_pipeline()


    print("Extracting took: ", round(time.time() - scraping_start_time, 1))


if __name__ == '__main__':
    main()
