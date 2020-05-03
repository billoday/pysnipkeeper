from secrets import randbelow


class Snips:
    def __init__(self, schemas: dict, default_category: str, data: dict = None):
        if data is None:
            self.data = self._init_data(schemas, default_category)
        else:
            self.data = data
        self.schemas = schemas
        self.default_category = default_category

    @staticmethod
    def _init_data(schemas: dict, default_category: str):
        temp_data = {}
        for schema in schemas:
            if schema not in 'default':
                temp_data[schema] = []
        temp_data[default_category] = []
        return temp_data

    def add(self, snip_data: dict, category: str = None):
        if category is None:
            category = self.default_category
        data_to_be_written = {}
        schema = self.schemas.get(category, self.schemas.get('default'))
        if 'default_field' in schema:
            default_field_key = schema.pop('default_field')
        else:
            default_field_key = ''
        default_field_val = snip_data.get('default_field')
        for field, constraints in schema.items():
            if field not in snip_data:
                if 'default' not in constraints:
                    if constraints.get('required', False) is True:
                        if field in default_field_key and default_field_key in field and default_field_val is not None:
                            data_to_be_written[field] = default_field_val
                        else:
                            raise ValueError(f'{field} is required.')
                else:
                    data_to_be_written[field] = constraints.get('default')
            else:
                data_to_be_written[field] = snip_data.get(field)
        # If we make it here, the data is prepared to be written
        try:
            self.data[category].append(data_to_be_written)
        except KeyError:
            self.data[category] = [data_to_be_written, ]

    def get_all_data(self):
        return self.data

    def get_random_entry(self, category: str = None):
        if category is None:
            category = self.default_category
        num_entries = len(self.data.get(category))
        if num_entries == 0:
            return None
        else:
            return self.data.get(category)[randbelow(num_entries)]

    def get_all_entries(self, category: str = None):
        if category is None:
            category = self.default_category
        return self.data.get(category, [])
