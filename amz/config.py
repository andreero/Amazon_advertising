from datetime import datetime, timedelta

import dateparser

MAX_REPORT_CREATION_RETRIES = 3
MAX_POOL_WORKERS = 5
REQUEST_TIMEOUTS_SECONDS = [5, 15, 15, 30, 30]+[60]*30


class AmazonConfig():
    @classmethod
    def from_dict(cls, config_dict):
        """ Initialize class instance with arguments from the provided dict """
        kwargs = {key: value for key, value in config_dict.items()}
        return cls(**kwargs)

    def __init__(
            self,
            AmzAccount_ID_Internal,
            AmzAccount_Name,
            AmzAccount_Group,
            AmzDeveloper_ClientID,
            AmzDeveloper_ClientSecret,
            AmzAccount_API_Advert_RefreshToken,
            ReportType,
            CountryCode,
            ReportStartDate,
            ReportEndDate,
    ):
        self.AmzAccount_ID_Internal = AmzAccount_ID_Internal
        self.AmzAccount_Name = AmzAccount_Name
        self.AmzAccount_Group = AmzAccount_Group
        self.AmzDeveloper_ClientID = AmzDeveloper_ClientID
        self.AmzDeveloper_ClientSecret = AmzDeveloper_ClientSecret
        self.AmzAccount_API_Advert_RefreshToken = AmzAccount_API_Advert_RefreshToken
        self.ReportType = ReportType.replace(' ', '').split(',')
        if 'SponsoredBrands' in self.ReportType:
            self.ReportType.append('SponsoredBrandsVideo')
        if 'SponsoredProducts' in self.ReportType:
            self.ReportType.remove('SponsoredProducts')
            self.ReportType += ['SponsoredProductsKeywords',
                                'SponsoredProductsSearchTermsKeywords',
                                'SponsoredProductsSearchTermsTargets',
                                'SponsoredProductsProductAds',
                                'SponsoredProductsAsinsKeywords',
                                'SponsoredProductsAsinsTargets']
        self.CountryCode = CountryCode.replace(' ', '').split(',')

        self.ReportStartDate = dateparser.parse(ReportStartDate, settings={'TIMEZONE': 'UTC'}).date()
        # API will return an error if the report date is more than 60 days in the past
        safe_amazon_min_date = datetime.utcnow().date()-timedelta(days=60)
        if self.ReportStartDate < safe_amazon_min_date:
            self.ReportStartDate = safe_amazon_min_date

        # Same limitation: API will return an error for future dates
        safe_amazon_max_date = datetime.utcnow().date()
        if not ReportEndDate or dateparser.parse(ReportEndDate, settings={'TIMEZONE': 'UTC'}).date() > safe_amazon_max_date:
            self.ReportEndDate = safe_amazon_max_date
        else:
            self.ReportEndDate = dateparser.parse(ReportEndDate, settings={'TIMEZONE': 'UTC'}).date()
