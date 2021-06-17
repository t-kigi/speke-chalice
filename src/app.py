#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import os

import boto3
from chalice import Chalice, Response, IAMAuthorizer

from chalicelib.keys import KeyCache
from chalicelib.key_server_common import ServerResponseBuilder

app = Chalice(app_name='speke-server')
app.debug = os.environ.get('DEBUG') is not None
app.api.binary_types = [
    '*/*'
]
authorizer = IAMAuthorizer()


if os.environ.get('STAGE') == 'local' and 'PROFILE' in os.environ:
    # ローカル検証でプロファイルを利用する場合
    session = boto3.session.Session(profile_name=os.environ['PROFILE'])
    s3 = session.client('s3')
else:
    # それ以外
    s3 = boto3.client('s3')


@app.route('/copyProtection', methods=['POST'],
           authorizer=authorizer,
           content_types=['*/*'])
def copy_protection():
    try:
        body = app.current_request.raw_body
        app.log.info(body)
        cache = KeyCache(s3, os.environ['S3BUCKET'],
                         os.environ['KEY_PUBLISH_WEBSITE'],
                         os.environ.get('KEY_PUBLISH_PREFIX'))
        response = ServerResponseBuilder(
            body, cache, os.environ.get('SYSTEM_ID')).get_response()
        app.log.info(response.to_dict())
        return response
    except Exception as exception:
        app.log.exception(exception)
        return Response(
            status_code=500,
            headers={"Content-Type": "text/plain"},
            body=str(exception).encode('utf-8'))
