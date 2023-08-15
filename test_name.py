from unittest.mock import MagicMock

from scanner_handler import CheckQr


def test_check_scanned_device__exist_in_db__find_color(monkeypatch):
    checker = CheckQr()
    qr_lengths = [3, 5, 7]
    expected_colors = ['Red', 'Green', 'Fuzzy Wuzzy']

    monkeypatch.setattr(checker, 'check_in_db', lambda _: True)

    for qr_length, expected_color in zip(qr_lengths, expected_colors):
        checker.check_scanned_device("X" * qr_length)
        assert checker.color == expected_color


def test_check_scanned_device__exist_in_db__not_find_color(monkeypatch):
    checker = CheckQr()
    qr_wrong_lengths = [1, 2, 4, 6, 8, 9]

    monkeypatch.setattr(checker, 'check_in_db', lambda _: True)

    for qr_length in qr_wrong_lengths:
        result = checker.check_scanned_device("X" * qr_length)
        assert f"Error: Wrong qr length {qr_length}" in result


def test_check_scanned_device__not_exist_in_db(monkeypatch):
    checker = CheckQr()
    qr_lengths = [3, 5, 7]

    monkeypatch.setattr(checker, 'check_in_db', lambda _: None)

    for qr_length in qr_lengths:
        result = checker.check_scanned_device("X" * qr_length)
        assert "Not in DB" in result


def test_send_error__not_exist_in_db__not_find_color(monkeypatch):
    checker = CheckQr()
    qr = "X" * 4

    monkeypatch.setattr(checker, 'check_in_db', lambda _: None)
    checker.send_error = MagicMock()

    checker.check_scanned_device(qr)
    checker.send_error.assert_called_with(f"Error: Wrong qr length {len(qr)}")


def test_send_error__not_exist_in_db__find_color(monkeypatch):
    checker = CheckQr()
    qr = "X" * 3

    monkeypatch.setattr(checker, 'check_in_db', lambda _: None)
    checker.send_error = MagicMock()

    checker.check_scanned_device(qr)
    checker.send_error.assert_called_with("Not in DB")


def test_can_add_device_successful_scan(monkeypatch):
    checker = CheckQr()
    qr = "X" * 3  # Valid length

    monkeypatch.setattr(checker, 'check_in_db', lambda _: True)
    checker.can_add_device = MagicMock()

    checker.check_scanned_device(qr)
    checker.can_add_device.assert_called_with(f"hallelujah {qr}")



'''
* В підході до цих тестів зроблено припущення, 
що випадки коли class CheckQr повинен повертати помилку - 
він повертає строку з описом помилки, а не самий python Exception.


Висновок: 
class CheckQr не вірно обробляє кейси з довжиною QR відмінного від [3, 5, 7] - не видає помилку, замість цього повертає None.
class CheckQr не вірно обробляє кейси коли датчика не існує в БД - не видає помилку, замість цього повертає None.
Але методи check_len_color, can_add_device, send_error працюють вірно.

Додатковий висновок - помилка в методі check_scanned_device, 
замість: return
повинно бути: return func()
'''