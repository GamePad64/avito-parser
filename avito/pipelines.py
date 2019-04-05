import dataset
import tablib

FIELD_ALIAS = {
    'id': '№',
    'product_id': 'ID Авито',
    'name': 'Название',
    'url': 'URL',
    'phone': 'Тел.',
    'images': 'Фото',
    'address': 'Адрес',
    'description': 'Описание',
    'price': 'Цена',
    'currency': 'Валюта',
}


class AvitoPipeline(object):
    def open_spider(self, spider):
        self.db: dataset.database.Database = dataset.connect('sqlite:///:memory:')
        self.table: dataset.table.Table = self.db['products']

    def close_spider(self, spider):
        conv_dict = FIELD_ALIAS.copy()
        for key in self.table.columns:
            conv_dict[key] = conv_dict.get(key, key)

        ds = tablib.Dataset(headers=conv_dict.values())

        for row in self.table.find():
            values = [row[k] or '' for k in conv_dict]
            ds.append(values)

        with open('result.xlsx', 'wb') as f:
            f.write(ds.xlsx)

    def process_item(self, item, spider):
        self.table.upsert(dict(item), ['product_id'])
        return item
