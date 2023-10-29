# test_db_module.py

from db_module import DatabaseHandler
import pytest
import os


# Test het aanmaken en sluiten van een sessie
def test_session():
    db_handler = DatabaseHandler()
    assert db_handler._open_session()
    assert db_handler._close_session()


# Test het toevoegen en ophalen van een URL
def test_add_and_get_url():
    db_handler = DatabaseHandler()
    url = "http://example.com"
    db_handler.add_url(url)
    assert db_handler.get_all_urls() == [url]


# Test het toevoegen en verwijderen van een URL
def test_add_and_delete_url():
    db_handler = DatabaseHandler()
    url = "http://example.com"
    db_handler.add_url(url)
    db_handler.delete_url(url)
    assert db_handler.get_all_urls() == []


# Test het coderen en decoderen van UR_KEY
def test_encrypt_and_decrypt_ur_key():
    key = "mysecretkey"
    url = "http://example.com"
    encrypted = DatabaseHandler.encrypt_ur_key(url, key)
    decrypted = DatabaseHandler.decrypt_ur_key(encrypted, key)
    assert url == decrypted


if __name__ == '__main__':
    pytest.main([os.path.basename(__file__)])
