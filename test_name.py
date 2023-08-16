import pytest
from unittest.mock import MagicMock
from scanner_handler import CheckQr


@pytest.fixture
def checker_in_db_found(monkeypatch) -> CheckQr:
    checker = CheckQr()
    monkeypatch.setattr(checker, "check_in_db", lambda _: True)
    return checker

@pytest.fixture
def checker_in_db_not_found(monkeypatch) -> CheckQr:
    checker = CheckQr()
    monkeypatch.setattr(checker, "check_in_db", lambda _: None)
    return checker

@pytest.fixture
def qr_test_data():
    qr_lengths = [3, 5, 7]
    expected_colors = ["Red", "Green", "Fuzzy Wuzzy"]
    qr_wrong_lengths = [1, 2, 4, 6, 8, 9]

    return qr_lengths, expected_colors, qr_wrong_lengths


def test_check_scanned_device__exist_in_db__find_color(checker_in_db_found, qr_test_data):
    checker = checker_in_db_found
    qr_lengths, expected_colors, _ = qr_test_data

    for qr_length, expected_color in zip(qr_lengths, expected_colors):
        checker.check_scanned_device("X" * qr_length)
        assert checker.color == expected_color


def test_check_scanned_device__exist_in_db__not_find_color(checker_in_db_not_found, qr_test_data):
    checker = checker_in_db_not_found
    _, _, qr_wrong_lengths = qr_test_data

    for qr_length in qr_wrong_lengths:
        result = checker.check_scanned_device("X" * qr_length)
        assert f"Error: Wrong qr length {qr_length}" in result


def test_check_scanned_device__not_exist_in_db(checker_in_db_not_found, qr_test_data):
    checker = checker_in_db_not_found
    qr_lengths, _, _ = qr_test_data

    for qr_length in qr_lengths:
        result = checker.check_scanned_device("X" * qr_length)
        assert "Not in DB" in result


def test_send_error__not_exist_in_db__not_find_color(checker_in_db_not_found):
    checker = checker_in_db_not_found
    qr = "X" * 4

    checker.send_error = MagicMock()

    checker.check_scanned_device(qr)
    checker.send_error.assert_called_with(f"Error: Wrong qr length {len(qr)}")


def test_send_error__not_exist_in_db__find_color(checker_in_db_not_found):
    checker = checker_in_db_not_found
    qr = "X" * 3

    checker.send_error = MagicMock()

    checker.check_scanned_device(qr)
    checker.send_error.assert_called_with("Not in DB")


def test_can_add_device_successful_scan(checker_in_db_found):
    checker = checker_in_db_found
    qr = "X" * 3

    checker.can_add_device = MagicMock()

    checker.check_scanned_device(qr)
    checker.can_add_device.assert_called_with(f"hallelujah {qr}")


"""
* В підході до цих тестів зроблено припущення, 
що випадки коли class CheckQr повинен повертати помилку - 
він повертає строку з описом помилки, а не самий python Exception.
І це не потрібно перевіряти.


Висновок: 
class CheckQr не вірно обробляє кейси з довжиною QR відмінного від [3, 5, 7] - не видає помилку, замість цього повертає None.
class CheckQr не вірно обробляє кейси коли датчика не існує в БД - не видає помилку, замість цього повертає None.
Але методи check_len_color, can_add_device, send_error працюють вірно.

Додатковий висновок - помилка в методі check_scanned_device, 
замість: return
повинно бути: return func()
"""
