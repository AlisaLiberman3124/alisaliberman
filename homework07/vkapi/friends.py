import dataclasses
import time
import typing as tp

from homework07.vkapi import config
from homework07.vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(user_id: int, count: int = 5000, offset: int = 0, fields: tp.Any = None) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = config.VK_CONFIG["domain"]
    access_token = config.VK_CONFIG["access_token"]
    version_ = config.VK_CONFIG["version"]
    fields = ", ".join(fields) if fields else ""  # преобразуется в строку, так как вкапи не работает только с таким типом данных

    base = f"{domain}"
    url = (
        # Значения access_token, user_id, fields, offset, count и version_ вставляются в соответствующие места в строке
        f"friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&offset={offset}&count={count}&v={version_}"
    )
    session_ = Session(base)
    get_url = session_.get(url)
    # результат запроса сохраняется в переменную
    try:  # обработка полученного ответа от сервера.
        response = FriendsResponse(get_url.json()["response"]["count"], get_url.json()["response"]["items"])
    except KeyError:
        response = get_url.json()
        print(response)
    return response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = config.VK_CONFIG["domain"]
    access_token = config.VK_CONFIG["access_token"]
    version_ = config.VK_CONFIG["version"]
    session_ = Session(domain)
    results_of_requests = []  # пустой список, который будет содержать результаты запросов.

    if target_uids:  # если список не является пустым
        for i in range(((len(target_uids) - 1) // 100) + 1): # ограничение на количество идентификаторов в одном запросе
            try:
                url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uids={','.join(list(map(str, target_uids)))}&count={count}&offset={i * 100}&v={version_}"
                friends = session_.get(url)
                for friend in friends.json()["response"]:  # Цикл, который перебирает каждого друга в ответе от VK API.
                    # Объекты друзей извлекаются из JSON-ответа с помощью ключа "response".
                    results_of_requests.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
            except KeyError:
                pass
            time.sleep(0.34)  # Задержка выполнения программы, необходимая для соблюдения ограничения выполнения запросов для вк апи
        return results_of_requests
    try:
        url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&count={count}&offset={offset}&v={version_}"
        friends = session_.get(url)  # Выполнение HTTP-запроса с помощью метода get объекта session_.
        results_of_requests.extend(friends.json()["response"])  # Извлечение данных из JSON-ответа на запрос.
        # Метод json() возвращает JSON-ответ в виде словаря, и с помощью ключа "response" извлекаются данные общ. друзей
        # Затем метод extend() используется для добавления данных в список results_of_requests.
    except:
        pass
    return results_of_requests


if __name__ == "__main__":
    friends_response = get_friends(user_id=239843379, fields=["nickname"])
    active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]  # type: ignore
    print("Количество активных друзей:", len(active_users))
    mutual_friends = get_mutual(source_uid=239843379, target_uid=269738261, count=len(active_users))
    print("Количество общих друзей пользователей:", len(mutual_friends))
    print("ID общих друзей:", mutual_friends)
