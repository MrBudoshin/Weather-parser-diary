from peewee import *

database = SqliteDatabase('Weather.db')


class BaseTable(Model):
    class Meta:
        database = database


class Weather(BaseTable):
    date = DateTimeField(unique=True)
    weather_date = CharField()
    state = CharField()
    temp = IntegerField()


database.create_tables([Weather])


class DbUpdater:

    def __init__(self):
        self.user_request = []

    def update_db(self, weather_list):
        for key, value in weather_list.items():
            weather = [
                {
                    'date': key,
                    'weather_date': value['date'],
                    'state': value['state'],
                    'temp': value['temperature']
                }]
            Weather.insert_many(weather).on_conflict('replace').execute()

    def get_several_result(self, fro, to):
        for result in Weather.select().where(Weather.date.between(fro, to)):
            self.user_request.append((result.weather_date, result.state, result.temp))
        return self.user_request

    def get_one_result(self, data_request):
        one_result = Weather.select().where(Weather.date == data_request).get()
        return one_result.weather_date, one_result.state, one_result.temp


if __name__ == '__main__':
    cra = {20: {'date': 'Sunday, Dec 20th, 2020', 'state': 'Foggy throughout the\xa0day.', 'temperature': '-5˚'},
           21: {'date': 'Monday, Dec 21st, 2020', 'state': 'Foggy overnight and in the\xa0morning.', 'temperature': '-1˚'},
           22: {'date': 'Tuesday, Dec 22nd, 2020', 'state': 'Overcast throughout the\xa0day.', 'temperature': '-6˚'},
           23: {'date': 'Wednesday, Dec 23rd, 2020', 'state': 'Foggy until morning, starting again in the\xa0evening.',
                'temperature': '-7˚'},
           24: {'date': 'Thursday, Dec 24th, 2020', 'state': 'Foggy throughout the\xa0day.', 'temperature': '-6˚'},
           25: {'date': 'Friday, Dec 25th, 2020', 'state': 'Foggy until morning, starting again in the\xa0evening.',
                'temperature': '-5˚'}}

    up = DbUpdater()
    up.update_db(cra)
    print(up.get_several_result(20, 23))
    print(up.get_one_result(25))
