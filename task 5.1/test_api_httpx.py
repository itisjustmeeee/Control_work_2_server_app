import httpx

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "Oli"
PASSWORD = "3421J"

def test_with_httpx():
    with httpx.Client(follow_redirects=True) as client:
        print("Делаем логин...")
        response = client.post(
            f"{BASE_URL}/login",
            auth=(USERNAME, PASSWORD)
        )

        print(f"Статус логина: {response.status_code}")
        if response.status_code != 200:
            print("Ошибка логина:", response.text)
            return
        
        print("Cookies после логина:", client.cookies)

        print("\n Проверка защищенной страницы...")
        protected = client.get(f"{BASE_URL}/user")

        print(f"Статус: {protected.status_code}")
        print("Ответ:", protected.text)

if __name__ == "__main__":
    test_with_httpx()