import base64
from dataclasses import dataclass

import yaml
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Declaratieve basis voor de UR_KEY-tabel
Base = declarative_base()


@dataclass
class AppConfig:
    db_name: str
    encryption_key: str

    @property
    def database_url(self):
        return f"sqlite:///{self.db_name}.sqlite3"

    @classmethod
    def from_yaml(cls, config_file_path):
        with open(config_file_path, "r") as file:
            config_data = yaml.safe_load(file)
        return cls(**config_data)


class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)


class UR_KEY(Base):
    __tablename__ = 'ur_keys'

    id = Column(Integer, primary_key=True)
    ur_key = Column(String)

    def __init__(self, ur_key):
        self.ur_key = ur_key


def load_config():
    # Laad de configuratie uit het YAML-bestand
    return AppConfig.from_yaml(config_file_path="conf.yaml")


class DatabaseHandler:
    config = None

    def __init__(self, db_name='db'):
        self.config = load_config()
        self.engine = create_engine(self.config.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self._open_session()

    def _open_session(self):
        return self.Session()

    def _close_session(self):
        self.session.close()

    @classmethod
    def encrypt_ur_key(cls, url):
        url_bytes = url.encode('utf-8')
        key_bytes = cls.config["encryption_key"].encode('utf-8')

        # XOR de URL met de sleutel
        encrypted_bytes = bytes([a ^ b for a, b in zip(url_bytes, key_bytes)])

        # Converteer de gecodeerde bytes naar een base64-gecodeerde string
        encrypted_ur_key = base64.b64encode(encrypted_bytes).decode('utf-8')

        return encrypted_ur_key

    def add_url(self, url):
        new_url = URL(url=url)
        self.session.add(new_url)
        self.session.commit()

    def add_ur_key(self, ur_key):
        new_ur_key = UR_KEY(ur_key=ur_key)
        self.session.add(new_ur_key)
        self.session.commit()

    def add_url_as_ur_key(self, url):
        encrypted_ur_key = self.encrypt_ur_key(url)
        self.add_ur_key(encrypted_ur_key)

    def close(self):
        self._close_session()

    def get_all_urls(self):
        """
        Haal alle niet-gecodeerde URL's op uit de database.
        """
        session = self._open_session()
        urls = session.query(URL).all()
        self._close_session()
        return [url.url for url in urls]

    def delete_url(self, url):
        """
        Verwijder een URL uit de database op basis van de opgegeven URL.
        """
        session = self._open_session()
        url_to_delete = session.query(URL).filter(URL.url == url).first()
        if url_to_delete:
            session.delete(url_to_delete)
            session.commit()
        self._close_session()
