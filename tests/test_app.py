#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

import app as target


def test_empty_request():
    """ 入力なしで API が呼ばれた場合のテスト """
    target.app.current_request = MagicMock(raw_body=b'')
    with patch('os.environ') as menv:
        menv.get.return_value = '81376844-f976-481e-a84e-cc25d39b0b33'
        res = target.copy_protection().to_dict()
    assert res['statusCode'] == 500
    assert 'no element found' in res['body'].decode()


INPUT_XML = b'<?xml version="1.0" encoding="UTF-8"?><cpix:CPIX id="5E99137A-BD6C-4ECC-A24D-A3EE04B4E011" xmlns:cpix="urn:dashif:org:cpix" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:speke="urn:aws:amazon:com:speke"><cpix:ContentKeyList><cpix:ContentKey kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"></cpix:ContentKey></cpix:ContentKeyList><cpix:DRMSystemList><cpix:DRMSystem kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe" systemId="81376844-f976-481e-a84e-cc25d39b0b33">    <cpix:ContentProtectionData />    <speke:KeyFormat />    <speke:KeyFormatVersions />    <speke:ProtectionHeader />    <cpix:PSSH />    <cpix:URIExtXKey /></cpix:DRMSystem></cpix:DRMSystemList><cpix:ContentKeyPeriodList><cpix:ContentKeyPeriod id="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622" index="11425"/></cpix:ContentKeyPeriodList><cpix:ContentKeyUsageRuleList><cpix:ContentKeyUsageRule kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"><cpix:KeyPeriodFilter periodId="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622"/></cpix:ContentKeyUsageRule></cpix:ContentKeyUsageRuleList></cpix:CPIX>'  # noqa
EXPECTED_XML = b'<cpix:CPIX xmlns:cpix="urn:dashif:org:cpix" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:speke="urn:aws:amazon:com:speke" id="5E99137A-BD6C-4ECC-A24D-A3EE04B4E011"><cpix:ContentKeyList><cpix:ContentKey kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"><cpix:Data><pskc:Secret><pskc:PlainValue>MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=</pskc:PlainValue></pskc:Secret></cpix:Data></cpix:ContentKey></cpix:ContentKeyList><cpix:DRMSystemList><cpix:DRMSystem kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe" systemId="81376844-f976-481e-a84e-cc25d39b0b33">    <cpix:ContentProtectionData />    <speke:KeyFormat />    <speke:KeyFormatVersions />    <speke:ProtectionHeader />    <cpix:PSSH />    <cpix:URIExtXKey>aHR0cHM6Ly9leGFtcGxlLmNvbS9rZXlzLzAwMDAua2V5</cpix:URIExtXKey></cpix:DRMSystem></cpix:DRMSystemList><cpix:ContentKeyPeriodList><cpix:ContentKeyPeriod id="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622" index="11425" /></cpix:ContentKeyPeriodList><cpix:ContentKeyUsageRuleList><cpix:ContentKeyUsageRule kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"><cpix:KeyPeriodFilter periodId="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622" /></cpix:ContentKeyUsageRule></cpix:ContentKeyUsageRuleList></cpix:CPIX>'  # noqa


@patch('app.KeyCache')
def test_sample_request(mock):
    """ 入力のサンプルを与えた場合のテスト """
    # mocked key cache
    mock().get.return_value = b'00000000000000000000000000000000'
    mock().url.return_value = 'https://example.com/keys/0000.key'

    # get valid response
    raw_body = b'<?xml version="1.0" encoding="UTF-8"?><cpix:CPIX id="5E99137A-BD6C-4ECC-A24D-A3EE04B4E011" xmlns:cpix="urn:dashif:org:cpix" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:speke="urn:aws:amazon:com:speke"><cpix:ContentKeyList><cpix:ContentKey kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"></cpix:ContentKey></cpix:ContentKeyList><cpix:DRMSystemList><cpix:DRMSystem kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe" systemId="81376844-f976-481e-a84e-cc25d39b0b33">    <cpix:ContentProtectionData />    <speke:KeyFormat />    <speke:KeyFormatVersions />    <speke:ProtectionHeader />    <cpix:PSSH />    <cpix:URIExtXKey /></cpix:DRMSystem></cpix:DRMSystemList><cpix:ContentKeyPeriodList><cpix:ContentKeyPeriod id="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622" index="11425"/></cpix:ContentKeyPeriodList><cpix:ContentKeyUsageRuleList><cpix:ContentKeyUsageRule kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"><cpix:KeyPeriodFilter periodId="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622"/></cpix:ContentKeyUsageRule></cpix:ContentKeyUsageRuleList></cpix:CPIX>'  # noqa
    target.app.current_request = MagicMock(raw_body=raw_body)
    with patch('os.environ') as menv:
        menv.get.return_value = '81376844-f976-481e-a84e-cc25d39b0b33'
        res = target.copy_protection().to_dict()
    assert res['statusCode'] == 200
    assert res['body'] == EXPECTED_XML


@patch('app.KeyCache')
def test_error1_request(mock):
    """ 入力のサンプルを与えた場合のテスト """
    # mocked key cache
    mock().get.return_value = b'00000000000000000000000000000000'
    mock().url.return_value = 'https://example.com/keys/0000.key'

    # get valid response
    raw_body = b'<?xml version="1.0" encoding="UTF-8"?><cpix:CPIX id="5E99137A-BD6C-4ECC-A24D-A3EE04B4E011" xmlns:cpix="urn:dashif:org:cpix" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:speke="urn:aws:amazon:com:speke"><cpix:ContentKeyList><cpix:ContentKey kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"></cpix:ContentKey></cpix:ContentKeyList><cpix:DRMSystemList><cpix:DRMSystem kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe" systemId="ERROR">    <cpix:ContentProtectionData />    <speke:KeyFormat />    <speke:KeyFormatVersions />    <speke:ProtectionHeader />    <cpix:PSSH />    <cpix:URIExtXKey /></cpix:DRMSystem></cpix:DRMSystemList><cpix:ContentKeyPeriodList><cpix:ContentKeyPeriod id="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622" index="11425"/></cpix:ContentKeyPeriodList><cpix:ContentKeyUsageRuleList><cpix:ContentKeyUsageRule kid="6c5f5206-7d98-4808-84d8-94f132c1e9fe"><cpix:KeyPeriodFilter periodId="keyPeriod_e64248f6-f307-4b99-aa67-b35a78253622"/></cpix:ContentKeyUsageRule></cpix:ContentKeyUsageRuleList></cpix:CPIX>'  # noqa
    target.app.current_request = MagicMock(raw_body=raw_body)
    with patch('os.environ'):
        res = target.copy_protection().to_dict()
    assert res['statusCode'] == 500
