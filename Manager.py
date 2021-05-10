import WeatherMaker
import ImageMaker
import DatabaseUpdater
import argparse
import datetime


class Managers:

    def db_append_several(self, day, day_to, month):
        if day_to is None:
            day_to = day
        get_wz = WeatherMaker.Wezer(day, month)
        getter = get_wz.get_weather(day_to)
        DatabaseUpdater.DbUpdater().update_db(weather_list=getter)
        print('добалено  базу данных')

    def get_several_db(self, day, day_to):
        if day_to is None:
            up = DatabaseUpdater.DbUpdater().get_one_result(data_request=day)
        else:
            up = DatabaseUpdater.DbUpdater().get_several_result(fro=day, to=day_to)
        return print(up)

    def several_print(self, forom, to_date, mounth):
        if to_date is None:
            to_date = forom
        prin_wz = WeatherMaker.Wezer(forom, mounth)
        prin_wz.get_weather(to_date)
        for key, value in prin_wz.db_date.items():
            weather_text = value['date'] + " " + value['state'] + " " + value['temperature'][:-1]
            print(weather_text)

    def several_postcard(self, forom, to_date, mounth):
        if to_date is None:
            to_date = forom
        prin_wz = WeatherMaker.Wezer(forom, mounth)
        pogoda = prin_wz.get_weather(to_date)
        image = ImageMaker.ImageCreator(pogoda)
        image.run()

    def parser(self):
        weather_manager = argparse.ArgumentParser()
        weather_manager.add_argument('-add_db_weather', action="store_true", help="Add to data base weather history",
                                     required=False)
        weather_manager.add_argument('-get_weather', action="store_true", help="Get from data base weather",
                                     required=False)
        weather_manager.add_argument('-make_magick', action="store_true", help="Make image from db weather",
                                     required=False)
        weather_manager.add_argument('-show_results', action="store_true", help="Show result in ~ ", required=False)
        weather_manager.add_argument('-b', help='begin data')
        weather_manager.add_argument('-e', help='end data')
        weather_manager.add_argument('-m', help='month', default=datetime.datetime.now().month, required=False)
        argsun = weather_manager.parse_args('-make_magick -b 17 -e 20'.split())
        date = datetime.datetime.today() - datetime.timedelta(days=7)
        self.several_print(forom=str(date.day), to_date=str(str(datetime.datetime.today().day)), mounth=date.month)
        if argsun.show_results:
            self.several_print(forom=argsun.b, to_date=argsun.e, mounth=argsun.m)
        elif argsun.add_db_weather:
            self.db_append_several(day=argsun.b, day_to=argsun.e, month=argsun.m)
        elif argsun.make_magick:
            self.several_postcard(forom=argsun.b, to_date=argsun.e, mounth=argsun.m)
        elif argsun.get_weather:
            self.get_several_db(day=argsun.b, day_to=argsun.e)
        return argsun


if __name__ == '__main__':
    args = Managers()
    args.parser()