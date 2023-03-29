class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """"Метод, который показывает расчеты тренировки."""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.'
                   )
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получаем дистанцию в км."""
        mean_distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return (mean_distance)

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""

        formula_mean_speed: float = (self.get_distance()
                                     / self.duration)
        return (formula_mean_speed)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращаем информационное сообщение о тренировке."""
        return (InfoMessage(self.__class__.__name__,
                self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    CAL_SPEED_MULTIPLIER: int = 18
    MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:

        mean_speed_run: float = super().get_mean_speed()
        mean_duration_in_minut: float = (self.duration
                                         * self.MINUTES_IN_HOUR)
        formula_spent_calories: float = ((self.CAL_SPEED_MULTIPLIER
                                          * mean_speed_run
                                          + self.MEAN_SPEED_SHIFT)
                                         * self.weight / self.M_IN_KM
                                         * mean_duration_in_minut)
        return formula_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    HEIGHT_MULTIPLIER: float = 0.029
    WEIGHT_MULTIPLIER: float = 0.035
    KM_H: float = 0.278
    HOURS_IN_MINUT: float = 60
    SM_IN_METERS: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время ходьбы."""

        mean_speed_spwal: float = (super().get_mean_speed()
                                   * self.KM_H)
        mean_duration_in_minutes = self.duration * self.HOURS_IN_MINUT
        mean_height_in_meters = self.height / self.SM_IN_METERS
        mean_spent_calories_spwal: float = ((self.WEIGHT_MULTIPLIER
                                             * self.weight
                                             + (mean_speed_spwal**2
                                                / mean_height_in_meters)
                                             * self.HEIGHT_MULTIPLIER
                                             * self.weight)
                                            * mean_duration_in_minutes)
        return mean_spent_calories_spwal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SW_SPEED_MULTIPLIER: float = 1.1
    SW_DISTANCE_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения во время плавания."""

        mean_speed_sw: float = (self.length_pool
                                * self.count_pool
                                / self.M_IN_KM / self.duration)
        return mean_speed_sw

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время плавания."""

        formula_mean_speed: float = self.get_mean_speed()
        formula_spent_calories: float = ((formula_mean_speed
                                          + self.SW_SPEED_MULTIPLIER)
                                         * self.SW_DISTANCE_MULTIPLIER
                                         * self.weight
                                         * self.duration)
        return formula_spent_calories

    def get_distance(self) -> float:
        formula_distance_sw = super().get_distance()
        return formula_distance_sw


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dictionary:
        workout_name: str = dictionary[workout_type](*data)
        return workout_name
    else:
        return 'Попробуйте нечто другое'


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
