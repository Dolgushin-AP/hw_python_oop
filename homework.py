from dataclasses import dataclass
from typing import ClassVar, Dict, Sequence, Type


@dataclass
#dataclass правильно сделал? Почитал про него - похоже, отличная штука! )
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_TYPE: ClassVar[str] = "Тип тренировки"
    TRAINING_DURATION: ClassVar[str] = "Длительность"
    TRAINING_DISTANCE: ClassVar[str] = "Дистанция"
    TRAINING_MEAN_SPEED: ClassVar[str] = "Ср. скорость"
    TRAINING_CALORIE_RATE: ClassVar[str] = "Потрачено ккал"
#в константы вынес фразы, но дальше не догнал
#как их использовать в методе?
#почитал по ссылкам про asdict и .format
#что-то не доходит...
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60  #для перевода в минуты добавил константу

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  #что-то не соображаю, как сделать

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),  #добавил запятую
                           )


class Running(Training):
    """Тренировка: бег."""
#константы переименовал и записал верхним регистром
    CALORIE_RATE_COEFF_RUN_1: float = 18
    CALORIE_RATE_COEFF_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIE_RATE_COEFF_RUN_1 * self.get_mean_speed()
                - self.CALORIE_RATE_COEFF_RUN_2)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIE_RATE_COEFF_WALK_1: float = 0.035
    CALORIE_RATE_COEFF_WALK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIE_RATE_COEFF_WALK_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.CALORIE_RATE_COEFF_WALK_2
                * self.weight) * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38
    CALORIE_RATE_COEFF_SWIM_1: float = 1.1
    CALORIE_RATE_COEFF_SWIM_2: float = 2

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
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIE_RATE_COEFF_SWIM_1)
                * self.CALORIE_RATE_COEFF_SWIM_2 * self.weight)


#mypy подсказал мне взять Sequence вместо List. На List что-то пробухтел...
def read_package(workout_type: str, data:Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
#Type вроде норм зарядил
    dict_training_data: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type not in dict_training_data:
        raise KeyError ("Что-то пошло не так! Проверьте указанный тип тренировки.")
    return dict_training_data[workout_type](*data)
#raise вроде работает. Тут норм?

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
