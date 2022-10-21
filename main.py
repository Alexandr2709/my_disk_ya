from pathlib import Path

import requests

from environs import Env

env = Env()
env.read_env()


class YaUploader:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, token: str):
        self.token = token
        self.header = self._get_header()

    def _get_header(self):
        """Получить хидер для запроса."""
        header = {"Authorization": f"OAuth {self.token}"}  # создаем хидер для запроса
        return header

    def create_folder(self, path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        param = {"path": path}  # передаем в параметрах путь до папки на диске
        res = requests.put(  # делаем put запрос с параметрами для создания папки
            f'{self.BASE_URL}/resources',
            params=param,
            headers=self.header
        )
        print("Папка создана:", res.text)

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""

        get_upload_url = f'{self.BASE_URL}/resources/upload'  # адрес для получения ссылки для загрузки файла
        ya_disk_dir = "files_by_python"  # название папки на яндекс диске
        self.create_folder(ya_disk_dir)  # создаем папку на яндекс диске
        file_name = Path(file_path).name  # получаем имя загружаемого файла из пути
        print("file_name:", file_name)
        ya_disk_file_path = f"{ya_disk_dir}/{file_name}"  # создаем путь файла на диске
        data = {
            "path": ya_disk_file_path,  # путь файла на диске
            "overwrite": True  # перезаписать файл если существует
        }
        res = requests.get(get_upload_url, params=data, headers=self.header)  # делаем запрос к яндексу чтобы получить ссылку по которой можно загрузить файл
        res = res.json()  # переводим ответ от яндекса в словарь
        print(res)
        upload_url = res.get("href", None)  # берем по ключу "href" ссылку для загрузки файла
        if not upload_url:  # если такого ключа нет, то какая то ошибка, и просто retern  чтобы остановить функцию
            print(res)
            return

        with open(file_path, 'rb') as f:  # открываем наш файл
            response = requests.put(  # делаем put запрос на ссылку для загрузки
                res["href"],
                files={"file": f}  # прикрепляем файл к запросу
            )
        print("Файл загружен:", response.status_code, response.text)
        # Функция может ничего не возвращать


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = str(Path("test.txt").absolute())  # получаем полный путь до файла
    token = 'y0_AgAAAABIuY5GAADLWwAAAADRz2Dc85STuxBnSMeSxszA-pWTOpMv9ng'
    # в файле .env.example оразец как он выглядит
    my_disk = YaUploader(token)
    my_disk.upload(path_to_file)
