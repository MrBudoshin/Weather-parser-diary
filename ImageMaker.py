from copy import copy
import cv2 as cv


class ImageCreator:

    def __init__(self, weather_list):
        self.img = cv.imread("img_files//weather_img/probe.jpg").copy()
        self.cloud = cv.imread("img_files//weather_img/cloud.jpg")
        self.rain = cv.imread("img_files//weather_img/rain.jpg")
        self.snow = cv.imread("img_files//weather_img/snow.jpg")
        self.sun = cv.imread("img_files//weather_img/sun.jpg")
        self.error = cv.imread("img_files/weather_img/errors.jpg")
        self.window_name = "weather"
        self.weather_list = weather_list

    def view_image(self):
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.imshow(self.window_name, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def create_weather_image(self, state):
        self.img = cv.imread("img_files/weather_img/probe.jpg").copy()
        mix = 0
        step = 8
        colors = 0
        b = 255
        g = 255
        r = 255

        for _ in range(0, 264, 8):
            mix += step
            if "clear" in state:
                b -= 5
                self.img[_:mix, :] = (b, g, r)
            elif "rain" in state:
                g -= 5
                r -= 5
                self.img[_:mix, :] = (b, g, r)
            elif 'foggy' in state:
                colors += 5
                self.img[_:mix, :] = (colors, colors, colors)
            elif "snow" in state:
                r -= 5
                self.img[_:mix, :] = (b, g, r)
            else:
                pass
        if "clear" in state:
            self.img[50:150, 200:300] = self.sun
        elif "rain" in state:
            self.img[50:150, 200:300] = self.rain
        elif "foggy" in state:
            self.img[50:150, 200:300] = self.cloud
        elif "snow" in state:
            self.img[50:150, 200:300] = self.snow
        else:
            self.img[50:150, 200:300] = self.error

    def weather_text(self, text):
        cv.putText(self.img, text, color=(255, 0, 0), org=(20, 200), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=0.8)

    def run(self):
        for keys, values in self.weather_list.items():
            weather_text = values['date'] + " " + values['state'] + " " + values['temperature'][:-1]
            self.create_weather_image(state=values['state'].lower())
            self.weather_text(weather_text)
            self.view_image()


if __name__ == '__main__':

    cra = {20: {'date': 'Sunday, Dec 20th, 2020', 'state': 'Foggy throughout the\xa0day.', 'temperature': '-5˚'},
           21: {'date': 'Monday, Dec 21st, 2020', 'state': 'Foggy overnight and in the\xa0morning.', 'temperature': '-1˚'},
           22: {'date': 'Tuesday, Dec 22nd, 2020', 'state': 'Overcast throughout the\xa0day.', 'temperature': '-6˚'},
           23: {'date': 'Tuesday, Dec 23nd, 2020', 'state': 'Foggy throughout the\xa0day.', 'temperature': '-8˚'},
           24: {'date': 'Tuesday, Dec 23nd, 2020', 'state': 'Clear throughout the\xa0day.', 'temperature': '-9˚'}, }

    make_magick = ImageCreator(cra)
    make_magick.run()



