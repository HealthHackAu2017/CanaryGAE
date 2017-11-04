# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
from canary import processCSV
import google
from model import EpisodeModel
from google.appengine.ext import ndb

# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]

@app.route('/hack')
def hack():
    # Log the error and stacktrace.
    return '<html><body>An internal awesome occurred.</html></body>'
    #return render_template('form.html')


@app.route('/collect')
def collect():
    # Parse the query
    url = request.query_string

    # Attempt to download the file (blocking operation)
    data_response = google.appengine.api.urlfetch.Fetch(url)
    
    # Check response code?
    
    # Process the data
    process_result = processCSV(data_response.content)
    
    return render_template('link.html', key=str(process_result))



def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route('/restore')
def restore():
    #
    urlkey = request.query_string
    key = ndb.Key(urlsafe=urlkey)
    episode = key.get()


    return render_template('plot.html',
                           x_series=[1e-9 * (i - episode.start_time) for i in episode.somedata[0][0:2000]],
                           y_series=episode.somedata[9][0:2000])

    #return str(episode)

    #return str(episode.start_time) + "    " + str(episode.end_time) + "    " + str(episode.somedata[7])

    # Create a GQL query
    #q = EpisodeModel.query()
    #q.filter('user =', 'BsB-87654')
    #results = q.fetch()


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    
    # [END submitted]
    # [START render_template]
    return render_template(
                           'submitted_form.html',
                           name=name,
                           email=email,
                           site=site,
                           comments=comments)
# [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
