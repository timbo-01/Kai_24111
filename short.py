import pyshorteners


def shorten_link(long_url):
    try:
        # Инициализируем укоротитель
        s = pyshorteners.Shortener()
        # Генерируем короткую ссылку через сервис TinyURL
        short_url = s.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return f"Произошла ошибка: {e}"


if __name__ == "__main__":
    print("--- Простой укоротитель ссылок ---")
    user_url = input("Введите длинную ссылку: ").strip()

    if user_url:
        print("Сокращаем...")
        result = shorten_link(user_url)
        print(f"Короткая ссылка: {result}")
    else:
        print("Ссылка не может быть пустой.")