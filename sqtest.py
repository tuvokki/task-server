#!/usr/bin/env python
import webbrowser

import click
from db_module import DatabaseHandler


@click.group()
def cli():
    pass


@cli.command()
def update_database():
    # Maak een instantie van DatabaseHandler
    db_handler = DatabaseHandler()

    # Haal niet-gecodeerde URL's op
    non_encrypted_urls = db_handler.session.query(DatabaseHandler.URL).all()

    # Upgrade de niet-gecodeerde URL's naar gecodeerde UR_KEY's
    for url in non_encrypted_urls:
        url.url = db_handler.encrypt_ur_key(url.url)

    # Commit de wijzigingen aan de database
    db_handler.session.commit()

    # Sluit de sessie
    db_handler.close()


@cli.command()
@click.argument('ur_key')
def save_ur_key(ur_key):
    # Maak een instantie van DatabaseHandler
    db_handler = DatabaseHandler()

    # Voeg de opgegeven UR_KEY toe aan de database
    db_handler.add_ur_key(ur_key)

    # Sluit de sessie
    db_handler.close()


@cli.command()
@click.argument('index', required=False, type=int)
@click.option('-d', '--delete', is_flag=True, help='Verwijder de geopende URL uit de database')
def open_url(index, delete):
    # Maak een DBHandler-instance om met de database te communiceren
    db_handler = DatabaseHandler()

    # Haal alle URL's op uit de database
    urls = db_handler.get_all_urls()

    if not urls:
        click.echo("De database bevat geen URL's.")
        return

    if index is not None:
        if index < 0 or index >= len(urls):
            click.echo("Ongeldige index. Beschikbare indexen zijn 0 t/m {}.".format(len(urls) - 1))
            return
        url = urls[index]
    else:
        # Geen index opgegeven, open een willekeurige URL
        import random
        url = random.choice(urls)

    # Open de URL in de webbrowser
    webbrowser.open(url)

    if delete:
        # Als de -d vlag is opgegeven, verwijder de URL uit de database
        db_handler.delete_url(url)
        click.echo("URL is verwijderd uit de database.")


if __name__ == '__main__':
    cli()
