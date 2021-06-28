from amz.regions import regions
from amz.versions import versions
from io import BytesIO
import urllib.request
import urllib.parse
import urllib.error
import gzip
import json
import time

# adapted from https://github.com/dbrent-amazon/amazon-advertising-api-python


class AdvertisingApi(object):
    
    """Lightweight client library for Amazon Sponsored Products API."""

    v3_campaign_types = {
        'sb': 'sponsoredBrands',
        'sd': 'sponsoredDisplays',
    }

    def __init__(self,
                 client_id,
                 client_secret,
                 region,
                 profile_id=None,
                 access_token=None,
                 last_refreshed_access_token=None,
                 refresh_token=None,
                 sandbox=False):
        """
        Client initialization.

        :param client_id: Login with Amazon client Id that has been whitelisted
            for cpc_advertising:campaign_management
        :type client_id: string
        :param client_secret: Login with Amazon client secret key.
        :type client_id: string
        :param region: Region code for endpoint. See regions.py.
        :type region: string
        :param access_token: The access token for the advertiser account.
        :type access_token: string
        :param last_refreshed_access_token: Last time access token was refreshed.
        :type last_refreshed_access_token: time.time()
        :param refresh_token: The refresh token for the advertiser account.
        :type refresh_token: string
        :param sandbox: Indicate whether you are operating in sandbox or prod.
        :type sandbox: boolean
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = access_token
        self.last_refreshed_access_token = last_refreshed_access_token
        self.refresh_token = refresh_token

        self.api_version = versions['api_version']
        self.user_agent = 'AdvertisingAPI Python Client Library v{}'.format(
            versions['application_version'])
        self.profile_id = profile_id
        self.token_url = None
        self.sandbox = sandbox

        if region in regions:
            if sandbox:
                self.endpoint = regions[region]['sandbox']
            else:
                self.endpoint = regions[region]['prod']
            self.token_url = regions[region]['token_url']
        else:
            raise KeyError('Region {} not found in regions.'.format(region))
    
    @classmethod
    def has_version(cls, campaign_type):
        return campaign_type in cls.v3_campaign_types

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        """Set access_token"""
        self._access_token = value

    def do_refresh_token(self):
        if self.refresh_token is None:
            return {'success': False,
                    'code': 0,
                    'response': 'refresh_token is empty.'}

        if self._access_token:
            self._access_token = urllib.parse.unquote(self._access_token)
        self.refresh_token = urllib.parse.unquote(self.refresh_token)

        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret}

        data = urllib.parse.urlencode(params)

        req = urllib.request.Request(
            url='https://{}'.format(self.token_url),
            data=data.encode('utf-8'))

        try:
            f = urllib.request.urlopen(req)
            response = f.read().decode('utf-8')
            if 'access_token' in response:
                json_data = json.loads(response)
                self._access_token = json_data['access_token']
                self.last_refreshed_access_token = time.time()
                return {'success': True,
                        'code': f.code,
                        'response': self._access_token}
            else:
                return {'success': False,
                        'code': f.code,
                        'response': 'access_token not in response.'}
        except urllib.error.HTTPError as e:
            return {'success': False,
                    'code': e.code,
                    'response': '{msg}: {details}'.format(msg=e.msg, details=e.read())}

    def list_campaigns(self, data=None, campaign_type='sp'):
        """
        Retrieves a list of campaigns satisfying optional criteria.
        :GET: /{campaignType}/campaigns
        :param campaign_type: The campaignType to retrieve campaigns for ('sp' or 'hsa')
          Defaults to 'sp'
        :type campaign_type: string
        :param data: Optional, search criteria containing the following
            parameters.
        data may contain the following optional parameters:
        :param startIndex: 0-indexed record offset for the result set.
            Defaults to 0.
        :type startIndex: Integer
        :param count: Number of records to include in the paged response.
            Defaults to max page size.
        :type count: Integer
        :param campaignType: Restricts results to campaigns of a single
            campaign type. Must be **sponsoredProducts**.
        :type campaignType: String
        :param stateFilter: Restricts results to campaigns with state within
            the specified comma-separatedlist. Must be one of **enabled**,
            **paused**, **archived**. Default behavior is to include all.
        :param name: Restricts results to campaigns with the specified name.
        :type name: String
        :param campaignFilterId: Restricts results to campaigns specified in
            comma-separated list.
        :type campaignFilterId: String
        :returns:
            :200: Success. list of campaign
            :401: Unauthorized
        """
        interface = '{}/campaigns' .format(campaign_type)

        return self._operation(interface, data)

    def get_profiles(self):
        """
        Retrieves profiles associated with an auth token.

        :GET: /profiles
        :returns:
            :200: Success
            :401: Unauthorized
        """
        interface = 'profiles'
        return self._operation(interface)

    def get_profile(self, profile_id):
        """
        Retrieves a single profile by Id.

        :GET: /profiles/{profileId}
        :param profile_id: The Id of the requested profile.
        :type profile_id: string
        :returns:
            :200: List of **Profile**
            :401: Unauthorized
            :404: Profile not found
        """
        interface = 'profiles/{}'.format(profile_id)
        return self._operation(interface)

    def request_report(self, record_type=None, report_id=None, data=None, campaign_type='sp'):
        """
        :POST: /{campaignType}/reports

        :param campaign_type: The campaignType to request the report for ('sp' or 'hsa')
          Defaults to 'sp'
        :type data: string
        """
        if record_type is not None:
            interface = '{}/{}/report'.format(campaign_type, record_type)
            return self._operation(interface, data, method='POST')
        elif report_id is not None:
            interface = 'reports/{}'.format(report_id)
            return self._operation(interface)
        else:
            return {'success': False,
                    'code': 0,
                    'response': 'record_type and report_id are both empty.'}

    def get_report(self, report_id):
        interface = 'reports/{}'.format(report_id)
        res = self._operation(interface)
        if res['code'] == 200 and json.loads(res['response'])['status'] == 'SUCCESS':
            res = self._download(
                location=json.loads(res['response'])['location'])
            return res
        else:
            return res

    def _download(self, location):
        headers = {'Authorization': 'Bearer {}'.format(self._access_token),
                   'Content-Type': 'application/json',
                   'User-Agent': self.user_agent}

        if self.profile_id is not None:
            headers['Amazon-Advertising-API-Scope'] = self.profile_id
        else:
            raise ValueError('Invalid profile Id.')

        opener = urllib.request.build_opener(NoRedirectHandler())
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url=location, headers=headers, data=None)
        try:
            response = urllib.request.urlopen(req)
            if 'location' in response:
                if response['location'] is not None:
                    req = urllib.request.Request(url=response['location'])
                    res = urllib.request.urlopen(req)
                    res_data = res.read()
                    buf = BytesIO(res_data)
                    f = gzip.GzipFile(fileobj=buf)
                    data = f.read()
                    return {'success': True,
                            'code': res.code,
                            'response': json.loads(data.decode('utf-8'))}
                else:
                    return {'success': False,
                            'code': response.code,
                            'response': 'Location is empty.'}
            else:
                return {'success': False,
                        'code': response.code,
                        'response': 'Location not found.'}
        except urllib.error.HTTPError as e:
            return {'success': False,
                    'code': e.code,
                    'response': '{msg}: {details}'.format(msg=e.msg, details=e.read())}

    def _operation(self, interface, params=None, method='GET', ignore_version=False):
        """
        Makes that actual API call.

        :param interface: Interface used for this call.
        :type interface: string
        :param params: Parameters associated with this call.
        :type params: GET: string POST: dictionary
        :param method: Call method. Should be either 'GET', 'PUT', or 'POST'
        :type method: string
        """
        if self._access_token is None:
            return {'success': False,
                    'code': 0,
                    'response': 'access_token is empty.'}

        headers = {'Authorization': 'Bearer {}'.format(self._access_token),
                   'Amazon-Advertising-API-ClientId': self.client_id,
                   'Content-Type': 'application/json',
                   'User-Agent': self.user_agent}

        if self.sandbox:
            headers['BIDDING_CONTROLS_ON'] = 'true'

        if self.profile_id is not None and self.profile_id != '':
            headers['Amazon-Advertising-API-Scope'] = self.profile_id
        elif 'profiles' not in interface:
            # Profile ID is required for all calls beyond authentication and getting profile info
            return {'success': False,
                    'code': 0,
                    'response': 'profile_id is empty.'}

        data = None

        if method == 'GET':
            if params is not None:
                p = '?{}'.format(urllib.parse.urlencode(params))
            else:
                p = ''

            if ignore_version:
                url = 'https://{host}/{interface}{params}'.format(
                    host=self.endpoint,
                    interface=interface,
                    params=p)
            else:
                url = 'https://{host}/{api_version}/{interface}{params}'.format(
                    host=self.endpoint,
                    api_version=self.api_version,
                    interface=interface,
                    params=p)
        else:
            if params is not None:
                data = json.dumps(params).encode('utf-8')

            if ignore_version:
                url = 'https://{host}/{interface}'.format(
                    host=self.endpoint,
                    interface=interface)
            else:
                url = 'https://{host}/{api_version}/{interface}'.format(
                    host=self.endpoint,
                    api_version=self.api_version,
                    interface=interface)

        req = urllib.request.Request(url=url, headers=headers, data=data)
        req.method = method

        try:
            f = urllib.request.urlopen(req)
            return {'success': True,
                    'code': f.code,
                    'response': f.read().decode('utf-8')}
        except urllib.error.HTTPError as e:
            return {'success': False,
                    'code': e.code,
                    'response': '{msg}: {details}'.format(msg=e.msg, details=e.read())}


class NoRedirectHandler(urllib.request.HTTPErrorProcessor):
    """Handles report and snapshot redirects."""

    def http_response(self, request, response):
        if response.code == 307:
            if 'Location' in response.headers:
                return {'code': 307,
                        'location': response.headers['Location']}
            else:
                return {'code': response.code, 'location': None}
        else:
            return urllib.request.HTTPErrorProcessor.http_response(
                self, request, response)

    https_response = http_response
