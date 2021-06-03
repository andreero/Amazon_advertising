from datetime import datetime
from db.models import SponsoredProductsAsinsKeyword, SponsoredProductsAsinsTarget, SponsoredProductsKeyword, \
    SponsoredProductsSearchTerm, SponsoredProductsProductAds, SponsoredBrand, SponsoredBrandVideo, SponsoredDisplay


def create_sp_asins_keywords(asins_keyword_dict):
    if asins_keyword_dict:
        return SponsoredProductsAsinsKeyword(
            CampaignName=asins_keyword_dict.get('campaignName'),
            CampaignId=asins_keyword_dict.get('campaignId'),
            AdGroupName=asins_keyword_dict.get('adGroupName'),
            AdGroupId=asins_keyword_dict.get('adGroupId'),
            KeywordId=asins_keyword_dict.get('keywordId'),
            KeywordText=asins_keyword_dict.get('keywordText'),
            ASIN=asins_keyword_dict.get('asin'),
            OtherASIN=asins_keyword_dict.get('otherAsin'),
            SKU=asins_keyword_dict.get('sku'),
            Currency=asins_keyword_dict.get('currency'),
            MatchType=asins_keyword_dict.get('matchType'),
            AttributedUnitsOrdered1d=asins_keyword_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=asins_keyword_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=asins_keyword_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=asins_keyword_dict.get('attributedUnitsOrdered30d'),
            AttributedUnitsOrdered1dOtherSKU=asins_keyword_dict.get('attributedUnitsOrdered1dOtherSKU'),
            AttributedUnitsOrdered7dOtherSKU=asins_keyword_dict.get('attributedUnitsOrdered7dOtherSKU'),
            AttributedUnitsOrdered14dOtherSKU=asins_keyword_dict.get('attributedUnitsOrdered14dOtherSKU'),
            AttributedUnitsOrdered30dOtherSKU=asins_keyword_dict.get('attributedUnitsOrdered30dOtherSKU'),
            AttributedSales1dOtherSKU=asins_keyword_dict.get('attributedSales1dOtherSKU'),
            AttributedSales7dOtherSKU=asins_keyword_dict.get('attributedSales7dOtherSKU'),
            AttributedSales14dOtherSKU=asins_keyword_dict.get('attributedSales14dOtherSKU'),
            AttributedSales30dOtherSKU=asins_keyword_dict.get('attributedSales30dOtherSKU'),
            Timestamp=datetime.now(),
        )


def create_sp_asins_targets(asins_target_dict):
    if asins_target_dict:
        return SponsoredProductsAsinsTarget(
            CampaignName=asins_target_dict.get('campaignName'),
            CampaignId=asins_target_dict.get('campaignId'),
            AdGroupName=asins_target_dict.get('adGroupName'),
            AdGroupId=asins_target_dict.get('adGroupId'),
            ASIN=asins_target_dict.get('asin'),
            OtherASIN=asins_target_dict.get('otherAsin'),
            SKU=asins_target_dict.get('sku'),
            Currency=asins_target_dict.get('currency'),
            MatchType=asins_target_dict.get('matchType'),
            AttributedUnitsOrdered1d=asins_target_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=asins_target_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=asins_target_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=asins_target_dict.get('attributedUnitsOrdered30d'),
            AttributedUnitsOrdered1dOtherSKU=asins_target_dict.get('attributedUnitsOrdered1dOtherSKU'),
            AttributedUnitsOrdered7dOtherSKU=asins_target_dict.get('attributedUnitsOrdered7dOtherSKU'),
            AttributedUnitsOrdered14dOtherSKU=asins_target_dict.get('attributedUnitsOrdered14dOtherSKU'),
            AttributedUnitsOrdered30dOtherSKU=asins_target_dict.get('attributedUnitsOrdered30dOtherSKU'),
            AttributedSales1dOtherSKU=asins_target_dict.get('attributedSales1dOtherSKU'),
            AttributedSales7dOtherSKU=asins_target_dict.get('attributedSales7dOtherSKU'),
            AttributedSales14dOtherSKU=asins_target_dict.get('attributedSales14dOtherSKU'),
            AttributedSales30dOtherSKU=asins_target_dict.get('attributedSales30dOtherSKU'),
            TargetId=asins_target_dict.get('targetId'),
            TargetingText=asins_target_dict.get('targetingText'),
            TargetingType=asins_target_dict.get('targetingType'),
            Timestamp=datetime.now(),
        )


def create_sp_keywords(keyword_dict):
    if keyword_dict:
        return SponsoredProductsKeyword(
            CampaignName=keyword_dict.get('campaignName'),
            CampaignId=keyword_dict.get('campaignId'),
            AdGroupName=keyword_dict.get('adGroupName'),
            AdGroupId=keyword_dict.get('adGroupId'),
            KeywordId=keyword_dict.get('keywordId'),
            KeywordText=keyword_dict.get('keywordText'),
            MatchType=keyword_dict.get('matchType'),
            Impressions=keyword_dict.get('impressions'),
            Clicks=keyword_dict.get('clicks'),
            Cost=keyword_dict.get('cost'),
            AttributedConversions1d=keyword_dict.get('attributedConversions1d'),
            AttributedConversions7d=keyword_dict.get('attributedConversions7d'),
            AttributedConversions14d=keyword_dict.get('attributedConversions14d'),
            AttributedConversions30d=keyword_dict.get('attributedConversions30d'),
            AttributedConversions1dSameSKU=keyword_dict.get('attributedConversions1dSameSKU'),
            AttributedConversions7dSameSKU=keyword_dict.get('attributedConversions7dSameSKU'),
            AttributedConversions14dSameSKU=keyword_dict.get('attributedConversions14dSameSKU'),
            AttributedConversions30dSameSKU=keyword_dict.get('attributedConversions30dSameSKU'),
            AttributedUnitsOrdered1d=keyword_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=keyword_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=keyword_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=keyword_dict.get('attributedUnitsOrdered30d'),
            AttributedSales1d=keyword_dict.get('attributedSales1d'),
            AttributedSales7d=keyword_dict.get('attributedSales7d'),
            AttributedSales14d=keyword_dict.get('attributedSales14d'),
            AttributedSales30d=keyword_dict.get('attributedSales30d'),
            AttributedSales1dSameSKU=keyword_dict.get('attributedSales1dSameSKU'),
            AttributedSales7dSameSKU=keyword_dict.get('attributedSales7dSameSKU'),
            AttributedSales14dSameSKU=keyword_dict.get('attributedSales14dSameSKU'),
            AttributedSales30dSameSKU=keyword_dict.get('attributedSales30dSameSKU'),
            AttributedUnitsOrdered1dSameSKU=keyword_dict.get('attributedUnitsOrdered1dSameSKU'),
            AttributedUnitsOrdered7dSameSKU=keyword_dict.get('attributedUnitsOrdered7dSameSKU'),
            AttributedUnitsOrdered14dSameSKU=keyword_dict.get('attributedUnitsOrdered14dSameSKU'),
            AttributedUnitsOrdered30dSameSKU=keyword_dict.get('attributedUnitsOrdered30dSameSKU'),
            Timestamp=datetime.now(),
        )


def create_sp_search_terms(search_term_dict):
    if search_term_dict:
        return SponsoredProductsSearchTerm(
            CampaignName=search_term_dict.get('campaignName'),
            CampaignId=search_term_dict.get('campaignId'),
            AdGroupName=search_term_dict.get('adGroupName'),
            AdGroupId=search_term_dict.get('adGroupId'),
            Query=search_term_dict.get('query'),
            KeywordId=search_term_dict.get('keywordId'),
            KeywordText=search_term_dict.get('keywordText'),
            MatchType=search_term_dict.get('matchType'),
            Impressions=search_term_dict.get('impressions'),
            Clicks=search_term_dict.get('clicks'),
            Cost=search_term_dict.get('cost'),
            AttributedConversions1d=search_term_dict.get('attributedConversions1d'),
            AttributedConversions7d=search_term_dict.get('attributedConversions7d'),
            AttributedConversions14d=search_term_dict.get('attributedConversions14d'),
            AttributedConversions30d=search_term_dict.get('attributedConversions30d'),
            AttributedConversions1dSameSKU=search_term_dict.get('attributedConversions1dSameSKU'),
            AttributedConversions7dSameSKU=search_term_dict.get('attributedConversions7dSameSKU'),
            AttributedConversions14dSameSKU=search_term_dict.get('attributedConversions14dSameSKU'),
            AttributedConversions30dSameSKU=search_term_dict.get('attributedConversions30dSameSKU'),
            AttributedUnitsOrdered1d=search_term_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=search_term_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=search_term_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=search_term_dict.get('attributedUnitsOrdered30d'),
            AttributedSales1d=search_term_dict.get('attributedSales1d'),
            AttributedSales7d=search_term_dict.get('attributedSales7d'),
            AttributedSales14d=search_term_dict.get('attributedSales14d'),
            AttributedSales30d=search_term_dict.get('attributedSales30d'),
            AttributedSales1dSameSKU=search_term_dict.get('attributedSales1dSameSKU'),
            AttributedSales7dSameSKU=search_term_dict.get('attributedSales7dSameSKU'),
            AttributedSales14dSameSKU=search_term_dict.get('attributedSales14dSameSKU'),
            AttributedSales30dSameSKU=search_term_dict.get('attributedSales30dSameSKU'),
            AttributedUnitsOrdered1dSameSKU=search_term_dict.get('attributedUnitsOrdered1dSameSKU'),
            AttributedUnitsOrdered7dSameSKU=search_term_dict.get('attributedUnitsOrdered7dSameSKU'),
            AttributedUnitsOrdered14dSameSKU=search_term_dict.get('attributedUnitsOrdered14dSameSKU'),
            AttributedUnitsOrdered30dSameSKU=search_term_dict.get('attributedUnitsOrdered30dSameSKU'),
            Timestamp=datetime.now(),
        )


def create_sp_product_ads(product_ad_dict):
    if product_ad_dict:
        return SponsoredProductsProductAds(
            CampaignName=product_ad_dict.get('campaignName'),
            CampaignId=product_ad_dict.get('campaignId'),
            AdGroupName=product_ad_dict.get('adGroupName'),
            AdGroupId=product_ad_dict.get('adGroupId'),
            Impressions=product_ad_dict.get('impressions'),
            Clicks=product_ad_dict.get('clicks'),
            Cost=product_ad_dict.get('cost'),
            Currency=product_ad_dict.get('currency'),
            ASIN=product_ad_dict.get('asin'),
            SKU=product_ad_dict.get('sku'),
            AttributedConversions1d=product_ad_dict.get('attributedConversions1d'),
            AttributedConversions7d=product_ad_dict.get('attributedConversions7d'),
            AttributedConversions14d=product_ad_dict.get('attributedConversions14d'),
            AttributedConversions30d=product_ad_dict.get('attributedConversions30d'),
            AttributedConversions1dSameSKU=product_ad_dict.get('attributedConversions1dSameSKU'),
            AttributedConversions7dSameSKU=product_ad_dict.get('attributedConversions7dSameSKU'),
            AttributedConversions14dSameSKU=product_ad_dict.get('attributedConversions14dSameSKU'),
            AttributedConversions30dSameSKU=product_ad_dict.get('attributedConversions30dSameSKU'),
            AttributedUnitsOrdered1d=product_ad_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=product_ad_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=product_ad_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=product_ad_dict.get('attributedUnitsOrdered30d'),
            AttributedSales1d=product_ad_dict.get('attributedSales1d'),
            AttributedSales7d=product_ad_dict.get('attributedSales7d'),
            AttributedSales14d=product_ad_dict.get('attributedSales14d'),
            AttributedSales30d=product_ad_dict.get('attributedSales30d'),
            AttributedSales1dSameSKU=product_ad_dict.get('attributedSales1dSameSKU'),
            AttributedSales7dSameSKU=product_ad_dict.get('attributedSales7dSameSKU'),
            AttributedSales14dSameSKU=product_ad_dict.get('attributedSales14dSameSKU'),
            AttributedSales30dSameSKU=product_ad_dict.get('attributedSales30dSameSKU'),
            AttributedUnitsOrdered1dSameSKU=product_ad_dict.get('attributedUnitsOrdered1dSameSKU'),
            AttributedUnitsOrdered7dSameSKU=product_ad_dict.get('attributedUnitsOrdered7dSameSKU'),
            AttributedUnitsOrdered14dSameSKU=product_ad_dict.get('attributedUnitsOrdered14dSameSKU'),
            AttributedUnitsOrdered30dSameSKU=product_ad_dict.get('attributedUnitsOrdered30dSameSKU'),
            Timestamp=datetime.now(),
        )


def create_sponsored_brand(sponsored_brand_dict):
    if sponsored_brand_dict:
        return SponsoredBrand(
            CampaignName=sponsored_brand_dict.get('campaignName'),
            CampaignId=sponsored_brand_dict.get('campaignId'),
            CampaignStatus=sponsored_brand_dict.get('campaignStatus'),
            CampaignBudget=sponsored_brand_dict.get('campaignBudget'),
            CampaignBudgetType=sponsored_brand_dict.get('campaignBudgetType'),
            CampaignRuleBasedBudget=sponsored_brand_dict.get('campaignRuleBasedBudget'),
            ApplicableBudgetRuleId=sponsored_brand_dict.get('applicableBudgetRuleId'),
            ApplicableBudgetRuleName=sponsored_brand_dict.get('applicableBudgetRuleName'),
            AdGroupName=sponsored_brand_dict.get('adGroupName'),
            AdGroupId=sponsored_brand_dict.get('adGroupId'),
            KeywordId=sponsored_brand_dict.get('keywordId'),
            KeywordText=sponsored_brand_dict.get('keywordText'),
            KeywordBid=sponsored_brand_dict.get('keywordBid'),
            KeywordStatus=sponsored_brand_dict.get('keywordStatus'),
            TargetId=sponsored_brand_dict.get('targetId'),
            SearchTermImpressionRank=sponsored_brand_dict.get('searchTermImpressionRank'),
            TargetingExpression=sponsored_brand_dict.get('targetingExpression'),
            TargetingText=sponsored_brand_dict.get('targetingText'),
            TargetingType=sponsored_brand_dict.get('targetingType'),
            MatchType=sponsored_brand_dict.get('matchType'),
            Impressions=sponsored_brand_dict.get('impressions'),
            Clicks=sponsored_brand_dict.get('clicks'),
            Cost=sponsored_brand_dict.get('cost'),
            AttributedDetailPageViewsClicks14d=sponsored_brand_dict.get('attributedDetailPageViewsClicks14d'),
            AttributedSales14d=sponsored_brand_dict.get('attributedSales14d'),
            AttributedSales14dSameSKU=sponsored_brand_dict.get('attributedSales14dSameSKU'),
            AttributedConversions14d=sponsored_brand_dict.get('attributedConversions14d'),
            AttributedConversions14dSameSKU=sponsored_brand_dict.get('attributedConversions14dSameSKU'),
            AttributedOrdersNewToBrand14d=sponsored_brand_dict.get('attributedOrdersNewToBrand14d'),
            AttributedOrdersNewToBrandPercentage14d=sponsored_brand_dict.get('attributedOrdersNewToBrandPercentage14d'),
            AttributedOrderRateNewToBrand14d=sponsored_brand_dict.get('attributedOrderRateNewToBrand14d'),
            AttributedSalesNewToBrand14d=sponsored_brand_dict.get('attributedSalesNewToBrand14d'),
            AttributedSalesNewToBrandPercentage14d=sponsored_brand_dict.get('attributedSalesNewToBrandPercentage14d'),
            AttributedUnitsOrderedNewToBrand14d=sponsored_brand_dict.get('attributedUnitsOrderedNewToBrand14d'),
            AttributedUnitsOrderedNewToBrandPercentage14d=sponsored_brand_dict.get('attributedUnitsOrderedNewToBrandPercentage14d'),
            UnitsSold14d=sponsored_brand_dict.get('unitsSold14d'),
            Dpv14d=sponsored_brand_dict.get('dpv14d'),
            Timestamp=datetime.now(),
        )


def create_sponsored_brand_video(sponsored_brand_video_dict):
    if sponsored_brand_video_dict:
        return SponsoredBrandVideo(
            CampaignName=sponsored_brand_video_dict.get('campaignName'),
            CampaignId=sponsored_brand_video_dict.get('campaignId'),
            CampaignStatus=sponsored_brand_video_dict.get('campaignStatus'),
            CampaignBudget=sponsored_brand_video_dict.get('campaignBudget'),
            CampaignBudgetType=sponsored_brand_video_dict.get('campaignBudgetType'),
            CampaignRuleBasedBudget=sponsored_brand_video_dict.get('campaignRuleBasedBudget'),
            ApplicableBudgetRuleId=sponsored_brand_video_dict.get('applicableBudgetRuleId'),
            ApplicableBudgetRuleName=sponsored_brand_video_dict.get('applicableBudgetRuleName'),
            AdGroupName=sponsored_brand_video_dict.get('adGroupName'),
            AdGroupId=sponsored_brand_video_dict.get('adGroupId'),
            KeywordId=sponsored_brand_video_dict.get('keywordId'),
            KeywordText=sponsored_brand_video_dict.get('keywordText'),
            KeywordBid=sponsored_brand_video_dict.get('keywordBid'),
            KeywordStatus=sponsored_brand_video_dict.get('keywordStatus'),
            TargetId=sponsored_brand_video_dict.get('targetId'),
            TargetingExpression=sponsored_brand_video_dict.get('targetingExpression'),
            TargetingText=sponsored_brand_video_dict.get('targetingText'),
            TargetingType=sponsored_brand_video_dict.get('targetingType'),
            MatchType=sponsored_brand_video_dict.get('matchType'),
            Impressions=sponsored_brand_video_dict.get('impressions'),
            Clicks=sponsored_brand_video_dict.get('clicks'),
            Cost=sponsored_brand_video_dict.get('cost'),
            AttributedSales14d=sponsored_brand_video_dict.get('attributedSales14d'),
            AttributedSales14dSameSKU=sponsored_brand_video_dict.get('attributedSales14dSameSKU'),
            AttributedConversions14d=sponsored_brand_video_dict.get('attributedConversions14d'),
            AttributedConversions14dSameSKU=sponsored_brand_video_dict.get('attributedConversions14dSameSKU'),
            Timestamp=datetime.now(),
        )


def create_sponsored_display(sponsored_display_dict):
    if sponsored_display_dict:
        return SponsoredDisplay(
            CampaignName=sponsored_display_dict.get('campaignName'),
            CampaignId=sponsored_display_dict.get('campaignId'),
            AdGroupName=sponsored_display_dict.get('adGroupName'),
            AdGroupId=sponsored_display_dict.get('adGroupId'),
            ASIN=sponsored_display_dict.get('asin'),
            SKU=sponsored_display_dict.get('sku'),
            AdId=sponsored_display_dict.get('adId'),
            Impressions=sponsored_display_dict.get('impressions'),
            Clicks=sponsored_display_dict.get('clicks'),
            Cost=sponsored_display_dict.get('cost'),
            Currency=sponsored_display_dict.get('currency'),
            AttributedConversions1d=sponsored_display_dict.get('attributedConversions1d'),
            AttributedConversions7d=sponsored_display_dict.get('attributedConversions7d'),
            AttributedConversions14d=sponsored_display_dict.get('attributedConversions14d'),
            AttributedConversions30d=sponsored_display_dict.get('attributedConversions30d'),
            AttributedConversions1dSameSKU=sponsored_display_dict.get('attributedConversions1dSameSKU'),
            AttributedConversions7dSameSKU=sponsored_display_dict.get('attributedConversions7dSameSKU'),
            AttributedConversions14dSameSKU=sponsored_display_dict.get('attributedConversions14dSameSKU'),
            AttributedConversions30dSameSKU=sponsored_display_dict.get('attributedConversions30dSameSKU'),
            AttributedUnitsOrdered1d=sponsored_display_dict.get('attributedUnitsOrdered1d'),
            AttributedUnitsOrdered7d=sponsored_display_dict.get('attributedUnitsOrdered7d'),
            AttributedUnitsOrdered14d=sponsored_display_dict.get('attributedUnitsOrdered14d'),
            AttributedUnitsOrdered30d=sponsored_display_dict.get('attributedUnitsOrdered30d'),
            AttributedSales1d=sponsored_display_dict.get('attributedSales1d'),
            AttributedSales7d=sponsored_display_dict.get('attributedSales7d'),
            AttributedSales14d=sponsored_display_dict.get('attributedSales14d'),
            AttributedSales30d=sponsored_display_dict.get('attributedSales30d'),
            AttributedSales1dSameSKU=sponsored_display_dict.get('attributedSales1dSameSKU'),
            AttributedSales7dSameSKU=sponsored_display_dict.get('attributedSales7dSameSKU'),
            AttributedSales14dSameSKU=sponsored_display_dict.get('attributedSales14dSameSKU'),
            AttributedSales30dSameSKU=sponsored_display_dict.get('attributedSales30dSameSKU'),
            AttributedOrdersNewToBrand14d=sponsored_display_dict.get('attributedOrdersNewToBrand14d'),
            AttributedSalesNewToBrand14d=sponsored_display_dict.get('attributedSalesNewToBrand14d'),
            AttributedUnitsOrderedNewToBrand14d=sponsored_display_dict.get('attributedUnitsOrderedNewToBrand14d'),
            Timestamp=datetime.now(),
        )
