from __future__ import annotations
from typing import Optional


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, 
                 training_type: Training, 
                 duration: int, 
                 distance: int, 
                 speed: int, 
                 calories: str
                 ) -> None:
        
        self.training_type = training_type
        self.duration = duration
        self.distance = distance 
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories}. ')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance()  / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79


    def get_spent_calories(self) -> str:
        spent_calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * 
             self.get_mean_speed() + 
             self.CALORIES_MEAN_SPEED_SHIFT) * 
             self.weight / self.M_IN_KM * 
             (self.duration * 60)
            )
        
        return f'{spent_calories:.3f}'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    
    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    
    def get_spent_calories(self) -> str:  
        speed_m_s = self.get_mean_speed() / 3600
        spent_calories = (
                           (self.CALORIES_MEAN_SPEED_MULTIPLIER * 
                           self.weight + 
                           (speed_m_s ** 2 / self.height) * 
                           self.CALORIES_MEAN_SPEED_SHIFT * self.weight) * 
                           self.duration
                           )
        
        return f'{spent_calories:.3f}'


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER:float = 1.1
    CALORIES_MEAN_SPEED_SHIFT:float = 2

    def __init__(self, 
                 action: int, 
                 duration: int, 
                 weight: int, 
                 length_pool: int, 
                 count_pool: int,
                 ) -> None:
        
        super().__init__(action, duration, weight)
        self.length_pool =length_pool
        self.count_pool = count_pool

    
    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    
    def get_spent_calories(self) -> str:
        spent_calories = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER) * 
            self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration
            )
        return f'{spent_calories:.3f}'


def read_package(workout_type: str, data: list) -> Training:
    type_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return type_training[workout_type](*data)


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

