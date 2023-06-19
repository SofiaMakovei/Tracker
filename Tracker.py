
class Training:
    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = 1000

    def get_distance(self):
        """Возвращает дистанцию в километрах, которую пользователь
        преодолел во время тренировки"""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return round(distance,2)

    def get_mean_speed(self):
        """Возвращает значение средней скорости движения во время
        тренировки"""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self):
        """Подсчет кол-ва калорий израсходованных во время тренировки"""
        pass

    def show_training_info(self):
        training_type = self.__class__.__name__
        info = InfoMessage(training_type, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    LEN_STEP = 0.65

    def get_spent_calories(self):
        SPEED_MULTIPLIER = 18
        SPEED_SHIFT = 1.79

        speed = SPEED_MULTIPLIER * self.get_mean_speed() + SPEED_SHIFT

        calories = (speed * self.weight) / self.M_IN_KM * self.duration * 60
        return round(calories, 2)


class SportWalking(Training):
    LEN_STEP = 0.65

    def __init__(self, action: int, duration: float, weight: float,
                 height: float):
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        """Подсчет количества калорий израсходованных во время ходьбы"""
        new_speed = self.get_mean_speed()*1000 / 3600
        calories = (0.035 * self.weight + (new_speed**2/self.height) * 0.029 *
                    self.weight)*self.duration*60
        return round(calories, 2)


class Swimming(Training):
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int):
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self):
        """Подсчет скорости"""
        speed = (((self.length_pool * self.count_pool)/self.M_IN_KM) /
                 self.duration)
        return round(speed, 2)

    def get_spent_calories(self):
        """Подсчет количества калорий израсходованных во время плавания"""
        calories = ((((self.get_mean_speed() + 1.1)*2) * self.weight) *
                    self.duration)
        return round(calories, 2)


class InfoMessage:
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Выводит сообщение на экран """
        return f"Тип тренировки: {self.training_type};" \
               f"Длительность:{self.duration} ч.;" \
               f"Дистанция:{self.distance} км.;Скорость:{self.speed};" \
               f"Калории:{self.calories}"


def read_package(workout_type, data):
    """Функция определяет тип тренировки """
    if workout_type == "SWM":
        swim1 = Swimming(action=data[0], duration=data[1], weight=data[2],
                         length_pool=data[3], count_pool=data[4])
        return swim1
    if workout_type == "RUN":
        run1 = Running(action=data[0], duration=data[1], weight=data[2])
        return run1
    if workout_type == "WLK":
        walk1 = SportWalking(action=data[0], duration=data[1],
                             weight=data[2], height=data[3])
        return walk1


def main(training: Training):
    info = training.show_training_info()
    print(info.get_message())


package = [
    ("SWM", [720, 1, 80, 25, 40]),
    ("RUN", [15000, 1, 75]),
    ("WLK", [9000, 1, 75, 1.8])
]

for workout_type, data in package:
    training = read_package(workout_type, data)
    main(training)