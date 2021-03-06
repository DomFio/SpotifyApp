from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login.utils import login_required
# import base64
# import datetime
# from urllib.parse import urlencode
# import requests
# import os
# from dotenv import load_dotenv
from SpotifyApp.Spotify.access import spotify
from SpotifyApp.forms import SpotifyForm 
from SpotifyApp.models import Artist, db

"""
Note that in the code below,
some of the arguments are specified when creating the blueprint object
the first argument, "site", is the blueprints name
which is sed by Flasks routing mechanism

the second arg is __name__, is the blueprint import name
which flask uses to locate the blueprints resources
"""


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/artists', methods = ['GET', 'POST'])
@login_required
def artists():
    form = SpotifyForm()
    related_artists = None
    try:
        if request.method == 'POST' and form.validate_on_submit():
            form_artist = form.form_artist.data
            print(f' form artist {form_artist}')
            artist = spotify.search(query= form_artist) # 
            # print(artist['artists']['items'][0]['name'])
            id = (artist['artists']['items'][0]['id'])
            related_artists = spotify.get_resource(id)
            related_artists = related_artists['artists']
            print(f"RELATED ARTIST IMAGE {related_artists[0]['images'][2]}")
            print(f"RELATED ARTISTS NAME {related_artists[0]['name']}")
            print(f"RELATED ARTISTS GENRES {related_artists[0]['genres'][0]}")
            print(f"RELATED ARTISTS LINK {related_artists[0]['external_urls']['spotify']}")
            print(f"RELATED ARTIST ??? {related_artists[0]}")
            # for artist in related_artists:
            #     musician = Artist(artist) 
            #     db.session.add(musician)
            #     db.session.commit()

            flash(f"You have succesfully called an artist")
            redirect(url_for('site.artists'))
        else:
            flash('Cannot find artists')

    except:
        raise Exception('Invalid Form Data: Please make sure spelling is correct')
    
    return render_template('artists.html', form=form, related_artists = related_artists)