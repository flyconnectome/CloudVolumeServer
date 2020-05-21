import datetime
import json
import numpy as np
import traceback

from cloudvolume import CloudVolume

# Import local modules
import process
import config

from flask import Flask, request, make_response, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    """Return service running."""
    running = datetime.datetime.now() - started
    return "Service running for {}".format(running)


@app.route("/help")
def help():
    """Return API endpoints."""
    h = """
        <h1>Available API endpoints</h1>
        <table style="width:50%">
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Example</th>
          </tr>
          <tr>
            <td><code>values (POST)</code></td>
            <td>returns segmentation IDs at given location</td>
            <td>TODO</td>
          <tr>
        </table>
        """
    return h


@app.route("/values", methods=['POST'])
def values():
    """Return segment IDs at given locations."""
    # Parse values
    try:
        if hasattr(request, 'json') and request.json.get('locations'):
            locs = request.json['locations']
        elif hasattr(request, 'form'):
            locs = request.form.get('locations')
    except BaseException as e:
        app.logger.error('Error: {}'.format(e))
        return {'error': str(e)}

    if not locs:
        return make_response(jsonify({'error': 'No locations provided'}), 400)

    if isinstance(locs, str):
        locs = json.loads(locs)

    try:
        locs = np.array(locs)
    except BaseException as e:
        app.logger.error('Error: {}'.format(e))
        return {'error': str(e)}

    app.logger.debug('Locations queried: {}'.format(str(locs)))

    if locs.shape[0] > config.MaxLocations:
        err = {'error': 'Max number of locations ({}) exceeded'.format(config.MaxLocations)}
        return make_response(jsonify(err), 400)

    try:
        seg_ids = process.get_multiple_ids(locs, vol,
                                           max_workers=config.MaxWorkers)
    except BaseException:
        tb = traceback.format_exc()
        app.logger.error('Error: {}'.format(tb))
        return make_response(jsonify({'error': str(tb)}), 500)

    return jsonify(seg_ids.tolist())


started = datetime.datetime.now()

vol = CloudVolume(**config.CloudVolumeKwargs)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
