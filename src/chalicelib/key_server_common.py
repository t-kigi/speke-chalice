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

import base64
import xml.etree.ElementTree as element_tree

from chalice import Response
from chalicelib.keys import KeyCache

from typing import Optional


# システム識別のデフォルト値
DEFAULT_HLS_AES_128_SYSTEM_ID = '81376844-f976-481e-a84e-cc25d39b0b33'

HLS_AES_128_KEY_FORMAT = ''  # 'identity'
HLS_AES_128_KEY_FORMAT_VERSIONS = ''  # '1'


class ServerResponseBuilder:
    """
    This class is responsible generating and returning the
    XML document response to the requesting encryptor
    """

    def __init__(self, request_body: bytes,
                 cache: KeyCache,
                 system_id: Optional[str] = None):
        self.cache = cache
        self.hls_aes_system_id = system_id or DEFAULT_HLS_AES_128_SYSTEM_ID
        self.root = element_tree.fromstring(request_body)
        self.document_key = None
        self.hmac_key = None
        self.public_key = None
        self.use_playready_content_key = False
        element_tree.register_namespace("cpix", "urn:dashif:org:cpix")
        element_tree.register_namespace("pskc", "urn:ietf:params:xml:ns:keyprov:pskc")  # noqa
        element_tree.register_namespace("speke", "urn:aws:amazon:com:speke")
        element_tree.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")     # noqa
        element_tree.register_namespace("enc", "http://www.w3.org/2001/04/xmlenc#")     # noqa

    def fixup_document(self, drm_system, system_id, content_id, kid):
        """
        Update the returned XML document based on the specified system ID
        """
        if system_id.lower() == self.hls_aes_system_id.lower():
            ext_x_key = self.cache.url(content_id, kid)
            drm_system.find("{urn:dashif:org:cpix}URIExtXKey").text = (
                base64.b64encode(ext_x_key.encode('utf-8')).decode('utf-8'))
            drm_system.find("{urn:aws:amazon:com:speke}KeyFormat").text = (
                base64.b64encode(HLS_AES_128_KEY_FORMAT.encode('utf-8')).decode('utf-8'))  # noqa
            drm_system.find("{urn:aws:amazon:com:speke}KeyFormatVersions").text = (  # noqa
                base64.b64encode(HLS_AES_128_KEY_FORMAT_VERSIONS.encode('utf-8')).decode('utf-8')) # noqa
            self.safe_remove(
                drm_system, "{urn:dashif:org:cpix}ContentProtectionData")
            self.safe_remove(
                drm_system, "{urn:aws:amazon:com:speke}ProtectionHeader")
            self.safe_remove(
                drm_system, "{urn:dashif:org:cpix}PSSH")
        else:
            raise Exception("Invalid system ID {}".format(system_id))

    def fill_request(self):
        """
        Fill the XML document with data about the requested keys.
        """
        content_id = self.root.get("id")
        system_ids = {}
        nodes = self.root.findall("./{urn:dashif:org:cpix}DRMSystemList/{urn:dashif:org:cpix}DRMSystem")  # noqa
        for drm_system in nodes:
            kid = drm_system.get("kid")
            system_id = drm_system.get("systemId")
            system_ids[system_id] = kid
            self.fixup_document(drm_system, system_id, content_id, kid)

        nodes = self.root.findall("./{urn:dashif:org:cpix}ContentKeyList/{urn:dashif:org:cpix}ContentKey")  # noqa
        for content_key in nodes:
            kid = content_key.get("kid")
            data = element_tree.SubElement(
                content_key, "{urn:dashif:org:cpix}Data")
            secret = element_tree.SubElement(
                data, "{urn:ietf:params:xml:ns:keyprov:pskc}Secret")

            # get (and generate) the key
            key_bytes = self.cache.get(content_id, kid)

            plain_value = element_tree.SubElement(
                secret, "{urn:ietf:params:xml:ns:keyprov:pskc}PlainValue")
            plain_value.text = base64.b64encode(key_bytes).decode('utf-8')

    def get_response(self):
        """
        Get the key request response as an HTTP response.
        """
        self.fill_request()
        return Response(
            status_code=200,
            headers={
                "Content-Type": "application/xml",
                "Speke-User-Agent": "SPEKE HLS AESOnly Server (https://github.com/t-kigi/speke-chalice)"  # noqa
            },
            body=element_tree.tostring(self.root)
        )

    def safe_remove(self, element, match):
        """
        Helper to remove an element only if it exists.
        """
        if element.find(match):
            element.remove(match)
