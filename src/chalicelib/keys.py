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

import secrets

from boto3_type_annotations import s3

from typing import Optional


class KeyCache:
    """ key を参照・保存する中間レイヤーを提供する """
    def __init__(self,
                 s3client: s3.Client,
                 keystore_bucket: str,
                 client_url_prefix: str,
                 s3_prefix: Optional[str] = None):
        self.s3client = s3client
        self.keystore_bucket = keystore_bucket
        self.client_url_prefix = client_url_prefix
        self.s3_prefix = s3_prefix

    def _key_path(self, content_id: str, key_id: str):
        if self.s3_prefix:
            return f'{self.s3_prefix}/{content_id}/{key_id}'
        return f'{content_id}/{key_id}'

    def get(self, content_id: str, key_id: str) -> bytes:
        """
        get (and create if needed) cache key
        """
        key = self._key_path(content_id, key_id)
        try:
            # get key on S3 bucket
            res = self.s3client.get_object(
                Bucket=self.keystore_bucket, Key=key)
            return res['Body'].read()
        except Exception as ex:
            # generate new key and put it onto bucket
            key_value = secrets.token_bytes(16)
            self.store(content_id, key_id, key_value)
            return key_value

    def store(self, content_id: str, key_id: str, key_value: bytes):
        """
        Store a key into the cache (S3) using the content_id
        as a folder and key_id as the file
        """
        key = self._key_path(content_id, key_id)
        self.s3client.put_object(
            Bucket=self.keystore_bucket,
            ServerSideEncryption='AES256',
            Key=key, Body=key_value)

    def url(self, content_id: str, key_id: str):
        """
        Return a URL that can be used to retrieve the
        specified key_id related to content_id
        """
        if self.s3_prefix:
            return f'{self.client_url_prefix}/{self.s3_prefix}/{content_id}/{key_id}'  # noqa
        else:
            return f'{self.client_url_prefix}/{content_id}/{key_id}'
