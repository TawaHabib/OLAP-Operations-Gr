class IDimension:

    def get_name(self) -> str:
        pass

    def get_actual_level(self) -> int:
        pass

    def get_max_levels(self) -> int:
        pass

    def get_min_level(self) -> int:
        pass

    def get_levels_name(self) -> list[str]:
        pass

    def get_actual_level_name(self) -> str:
        pass

    def get_previous_levels_name(self) -> str:
        pass

    def dimension_up(self) -> bool:
        pass

    def dimension_down(self) -> bool:
        pass


class Dimension(IDimension):
    def __init__(self, dimension_name: str, dimension_levels: list[str]):

        self.dimension_name = dimension_name
        self.dimension_levels = dimension_levels
        self.actual_dimension_level = min(len(dimension_levels), 1)
        self.min_dimension_level = min(len(dimension_levels), 1)
        self.max_dimension_level = len(dimension_levels)

    def get_name(self) -> str:
        return self.dimension_name

    def get_actual_level(self) -> int:
        return self.actual_dimension_level

    def get_max_levels(self) -> int:
        return self.max_dimension_level

    def get_min_level(self) -> int:
        return self.min_dimension_level

    def get_levels_name(self) -> list[str]:
        return self.dimension_levels

    def get_actual_level_name(self) -> str:
        return self.dimension_levels[self.actual_dimension_level-1]

    def get_previous_levels_name(self) -> str:
        previous = ''
        for i in range(self.actual_dimension_level):
            if i == self.actual_dimension_level-1:
                previous = previous + self.dimension_levels[i]
            else:
                previous = previous+self.dimension_levels[i]+';'
        return previous

    def dimension_up(self) -> bool:
        res: bool = True
        if self.actual_dimension_level < self.max_dimension_level:
            self.actual_dimension_level += 1
        else:
            res = False
        return res

    def dimension_down(self) -> bool:
        res: bool = True
        if self.actual_dimension_level > self.min_dimension_level:
            self.actual_dimension_level -= 1
        else:
            res = False
        return res


class FactInstance:
    def __init__(self, dimensions: list[IDimension], aggregate_datas_name: list[str]):
        self.dimensions = dimensions
        self.aggregate_datas_name = []
        self.aggregate_datas_name.extend(aggregate_datas_name)

    def roll_up(self, dimension_name: str) -> bool:
        return self.get_dimension(dimension_name).dimension_down()

    def drill_down(self, dimension_name: str) -> bool:
        return self.get_dimension(dimension_name).dimension_up()

    def get_dimensions_levels_as_str(self) -> str:
        dim = ''
        for i in self.dimensions:
            dim = dim+str(i.get_actual_level())
        return dim

    def get_aggregate_data_name_as_str(self) -> str:
        previous = ''
        for i in range(len(self.aggregate_datas_name)):
            if i == len(self.aggregate_datas_name) - 1:
                previous = previous + self.aggregate_datas_name[i]
            else:
                previous = previous + self.aggregate_datas_name[i] + ';'
        return previous

    def get_dimensions_names(self) -> str:
        dim = ''
        maximum = len(self.dimensions)
        for i in range(maximum):
            if i == maximum-1:
                dim = dim + self.dimensions[i].get_name()
            else:
                dim = dim + self.dimensions[i].get_name() + ';'

        return dim

    def get_actual_dimensions_names(self) -> str:
        dim = ''
        for i in range(len(self.dimensions)):
            if i == len(self.dimensions):
                dim = dim+self.dimensions[i].get_previous_levels_name()
            else:
                dim = dim+self.dimensions[i].get_previous_levels_name()+';'

        return dim

    def get_actual_name_level(self, dimension_name: str)->str:
        return self.get_dimension(dimension_name).get_actual_level_name()

    def get_all_dimensions(self) -> list[IDimension]:
        return self.dimensions

    def get_dimension(self, dimension_name: str) -> IDimension:
        for dimension in self.dimensions:
            if dimension.get_name().lower() == dimension_name.lower():
                return dimension


def get_sales_fact_instance(dimensions: list[IDimension] = None, aggregate_datas_name=None
                            ) -> FactInstance:
    if aggregate_datas_name is None:
        aggregate_datas_name = 'INCASSO;QUANTITA;NUMERO_CLIENTI'.split(';')

    if dimensions is None:
        tempo = Dimension(dimension_name='TEMPO',
                          dimension_levels=['ANNO', 'TRIMESTRE', 'MESE', 'SETTIMANA', 'DATA'])
        product = Dimension(dimension_name='PRODOTTO',
                            dimension_levels=['TIPO', 'CATEGORIA', 'SUB_CATEGORIA', 'PRODOTTO'])
        place = Dimension(dimension_name='FILIALE',
                          dimension_levels=['PAESE', 'REGIONE', 'CITTA', 'FILIALE'])
        dimensions = [tempo, product, place]

    return FactInstance(dimensions, aggregate_datas_name)

