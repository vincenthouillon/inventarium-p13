import json
from datetime import date
from dateutil.relativedelta import relativedelta
import os

TODAY = date.today()


class information:
    """
    Returns the following information about the equipments:

    Arguments:
        date_purchase {str} -- Date purchase '1985-10-26'
        price {float} -- Price
        length_warranty {int} -- Lenght warranty
        category {str} -- Category

    Returns:
        information.end_warranty -- Return a end of warranty date {date}
        information.wear_rate -- Return a residual value of the equipment {float}
        information.lifetime -- Return a percentage of life of the equipment {float}
    """

    def __init__(self, date_purchase, price, length_warranty, category):
        self.date_purchase   = date_purchase
        self.price           = float(price)
        self.length_warranty = int(length_warranty)
        self.category        = category
        self.equipment       = self.__read_json_and_return_dict()

    def __read_json_and_return_dict(self):
        """
        Open a json file and return a dictionary containing:
            - name
            - lifetime
            - rate
        """
        with open(os.path.join('myapp', 'libs', 'data.json'),
                  encoding='utf8') as file:
            data = json.load(file)

        equipment = dict()
        for category in data['categories']:
            name            = category['name']
            lifetime        = category['lifetime']
            rate            = category['rate']

            equipment[name] = lifetime, rate

        return equipment
    

    def __parse_date(self):
        """Text converter to date.

            Transform '1985-10-26' to 'date(1985,10,26)'.
        """
        d_year, d_month, d_day = self.date_purchase.split('-')
        date_purchase =date(int(d_year), int(d_month), int(d_day))

        return date_purchase

    @property
    def end_warranty(self):
        date_purchase = self.__parse_date()
        warranty = relativedelta(date_purchase, months=self.length_warranty)

        return date_purchase + warranty

    @property
    def lifetime(self):
        lt = self.equipment[self.category][0]
        d0 = self.__parse_date()
        d1 = TODAY
        delta = d1 - d0

        return int((delta.days/((lt)*365))*100)

    @property
    def wear_rate(self):
        birthday = self.__parse_date()
        age = relativedelta(TODAY, birthday)
        if age.years > 11:
            rate = self.equipment[self.category][1][11]
        else:
            rate = self.equipment[self.category][1][age.years]

        return '%.2f' % round((self.price * rate) * 0.01, 2)
