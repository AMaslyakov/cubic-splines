import click
import csv
import logging

INPUT_DATA = "input_data.csv"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.NOTSET)

logger = logging.getLogger("cubic_splines")
logger.setLevel(logging.DEBUG)

def read_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        result = [(float(row["x"]), float(row["y"])) for row in reader]
        return result

def main():
    input_data = read_data(INPUT_DATA)
    logger.debug(f"Input data: {input_data}")


@click.command()
@click.option('--input-data', prompt='Введите ваше имя')
def hello(input_data):
    click.echo(f'Привет, {input_data}!')




if __name__ == "__main__":
    main()
