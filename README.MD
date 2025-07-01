# Budowlanka 🏗️
![Django Tests](https://github.com/wojtekjurkowicz/budowlanka/actions/workflows/tests.yml/badge.svg)

Aplikacja webowa stworzona w Django, umożliwiająca przeglądanie realizacji budowlanych, dodawanie komentarzy, rejestrację użytkowników oraz zarządzanie wizytami.

## 📂 Struktura aplikacji

### `mainapp`
- `Realization` – model realizacji budowlanych
- `Comment` – komentarze przypisane do realizacji
- `Appointment` – model wizyt
- Widoki:
  - `index` – strona główna
  - `blog` – lista realizacji z paginacją
  - `detail` – szczegóły realizacji + komentarze
  - `contact` – formularz kontaktowy
  - `calendar_view` – kalendarz z wizytami
- Panel administratora z generowaniem PDF (ReportLab)

### `accounts`
- Rejestracja i logowanie użytkownika
- Obsługa formularzy Django (`UserCreationForm`, `AuthenticationForm`)

## 🚀 Instalacja

1. Sklonuj repozytorium:

```bash
git clone https://github.com/TwojaNazwa/budowlanka.git
cd budowlanka
````

2. Utwórz środowisko wirtualne i aktywuj:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

4. Wykonaj migracje i uruchom serwer:

```bash
python manage.py migrate
python manage.py runserver
```

## 🧪 Testowanie

Aby uruchomić testy jednostkowe:

```bash
python manage.py test
```

Projekt zawiera ponad 30 testów jednostkowych pokrywających:

* logowanie i rejestrację
* formularze (poprawne i błędne dane)
* widoki (`GET`, `POST`, 404)
* paginację
* eksport PDF w adminie

## 🛠 Technologie

* Python 3.x
* Django 5.0.4
* HTML5, CSS3
* Bootstrap (jeśli używany)
* ReportLab (generowanie PDF)
* SQLite (domyślna baza) / PostgreSQL (w środowisku CI)

## 👤 Autor

Projekt stworzony przez \[Twoje Imię lub GitHub Username].

## 📄 Licencja

Zobacz plik [LICENSE](./LICENSE) – wszelkie prawa zastrzeżone.
