# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
from canary import processCSV
import google
from model import EpisodeModel
from google.appengine.ext import ndb
import cloudstorage as gcs
import os
from google.appengine.api import app_identity

# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/exp')
def exp():
    # Grab files from the datastore
    bucket_name = app_identity.app_identity.get_default_gcs_bucket_name()
    prefix = '/data'
    bucket = '/' + bucket_name + prefix
    stats = gcs.listbucket(bucket, max_keys=10)
    filenames = []
    for stat in stats:
        filenames.append(stat.filename)
        # read and extract the file data
        #gcs_file = gcs.open(filename)
        #self.response.write(gcs_file.readline())
        #gcs_file.close()
    
    return render_template('exp.html',
                       filenames=filenames)

@app.route('/fc')
def fc():
    #bucket_name = app_identity.app_identity.get_default_gcs_bucket_name()
    filename = request.query_string
    #bucket = '/' + bucket_name + '/' + file_name
    gcs_file = gcs.open(filename)
    line = gcs_file.read()
    #gcs_file.read()
    gcs_file.close()
    return '<html><body>...' + line + '...</html></body>'


@app.route('/cs')
def cs():
    bucket_name = app_identity.app_identity.get_default_gcs_bucket_name()
    #bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
    #bucket_name = 'canary-hh.appspot.com'

    bucket = '/' + bucket_name #canary-hh.appspot.com
    stats = gcs.listbucket(bucket, max_keys=10)
    x = ''
    x += '<div>' + bucket_name + '</div>'
    x += '<div>' + str(dir(stats)) + '</div>'
    x += '<div>' + repr(stats) + '</div>'
    for stat in stats:
        x += '<div>x ' + repr(stat) + '</div>'
    return '<html><body>...' + x + '...</html></body>'


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
