import datetime as da
import statistics
import typing as tp

from homework07.vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    items = get_friends(user_id, fields=["bdate"]).items
    today = da.datetime.now()  # текущее дата и время
    year = today.year  # текущий год
    age = []
    for element in items:
        if "bdate" in element and len(element["bdate"]) >= 9:  # type: ignore
            # строка, предназначенная для чтения года состоящего как из 4х, так и из 2х цифр
            birthdate_ = element["bdate"]  # type: ignore
            birth_year = int(birthdate_[-4:])
            age.append(year - birth_year)
    average_ = statistics.median(age) if age else None
    return average_


if __name__ == "__main__":
    print(age_predict(189183825))
