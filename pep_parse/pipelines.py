import collections
import csv
import datetime as dt

from settings import BASE_DIR


class PepParsePipeline:
    """Pipeline формирует таблицу из статусов PEP
    в формате "Статус" - "Количество"
    и подсчитывает общее количество документов

    Возврат осуществляется в виде status_summary_date.csv
    по пути /results/pep_date.csv
    """
    total_by_status = collections.defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item['status']
        self.total_by_status[status] += 1
        return item

    def close_spider(self, spider):
        header = ['Статус', 'Количество']
        res_dir = BASE_DIR / 'results'
        res_dir.mkdir(exist_ok=True)
        now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{now}.csv'
        archive_path = res_dir / filename
        with open(archive_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f,
                                dialect='unix',
                                quoting=csv.QUOTE_MINIMAL)
            total = sum(self.total_by_status.values())
            writer.writerows([
                header,
                *self.total_by_status.items(),
                ['Total', total]
            ])
