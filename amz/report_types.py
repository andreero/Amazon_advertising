from amz.metrics import ASINS_KEYWORDS_METRICS, ASINS_TARGETS_METRICS, KEYWORDS_METRICS, \
    PRODUCT_ADS_METRICS, SPONSORED_BRANDS_METRICS, SPONSORED_DISPLAY_METRICS
from db.serializers import create_sp_asins_keywords, create_sp_asins_targets, create_sp_keywords, \
    create_sp_product_ads, create_sponsored_brand, create_sponsored_display
from db.models import SponsoredBrand, SponsoredDisplay, SponsoredProductsKeyword, \
    SponsoredProductsProductAds, SponsoredProductsAsinsKeyword, SponsoredProductsAsinsTarget

report_types = {
    'SponsoredProductsAsinsKeywords': {
        'campaignType': 'sponsoredProducts',
        'interface_type': 'sp',
        'record_type': 'asins',
        'serializer': create_sp_asins_keywords,
        'model': SponsoredProductsAsinsKeyword,
        'metrics': ','.join(ASINS_KEYWORDS_METRICS),
    },
    'SponsoredProductsAsinsTargets': {
        'campaignType': 'sponsoredProducts',
        'interface_type': 'sp',
        'record_type': 'asins',
        'serializer': create_sp_asins_targets,
        'model': SponsoredProductsAsinsTarget,
        'metrics': ','.join(ASINS_TARGETS_METRICS),
    },
    'SponsoredProductsKeywords': {
        'interface_type': 'sp',
        'record_type': 'keywords',
        'serializer': create_sp_keywords,
        'model': SponsoredProductsKeyword,
        'metrics': ','.join(KEYWORDS_METRICS),
    },
    'SponsoredProductsProductAds': {
        'interface_type': 'sp',
        'record_type': 'productAds',
        'serializer': create_sp_product_ads,
        'model': SponsoredProductsProductAds,
        'metrics': ','.join(PRODUCT_ADS_METRICS),
    },
    'SponsoredBrands': {
        'interface_type': 'hsa',
        'record_type': 'keywords',
        'serializer': create_sponsored_brand,
        'model': SponsoredBrand,
        'metrics': ','.join(SPONSORED_BRANDS_METRICS),
    },
    'SponsoredDisplay': {
        'interface_type': 'sd',
        'record_type': 'productAds',
        'tactic': 'T00020',
        'serializer': create_sponsored_display,
        'model': SponsoredDisplay,
        'metrics': ','.join(SPONSORED_DISPLAY_METRICS),
    }
}