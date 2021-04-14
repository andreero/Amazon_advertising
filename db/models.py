from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LogMessage(Base):
    __tablename__ = 'amz_adv_scripts_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))

    Timestamp = Column(DateTime(timezone=True))
    SenderModule = Column(String(255))
    MessageType = Column(String(255))
    MessageBody = Column(Text)
    Traceback = Column(Text)


class SponsoredProductsAsinsKeyword(Base):
    __tablename__ = 'amz_adv_sponsored_products_asins_keyword'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    KeywordId = Column(String(255), index=True)
    KeywordText = Column(Text)
    ASIN = Column(String(255))
    OtherASIN = Column(String(255))
    SKU = Column(String(255))
    Currency = Column(String(255))
    MatchType = Column(String(255))
    AttributedUnitsOrdered1d = Column(Float)
    AttributedUnitsOrdered7d = Column(Float)
    AttributedUnitsOrdered14d = Column(Float)
    AttributedUnitsOrdered30d = Column(Float)
    AttributedUnitsOrdered1dOtherSKU = Column(Float)
    AttributedUnitsOrdered7dOtherSKU = Column(Float)
    AttributedUnitsOrdered14dOtherSKU = Column(Float)
    AttributedUnitsOrdered30dOtherSKU = Column(Float)
    AttributedSales1dOtherSKU = Column(Float)
    AttributedSales7dOtherSKU = Column(Float)
    AttributedSales14dOtherSKU = Column(Float)
    AttributedSales30dOtherSKU = Column(Float)
    Timestamp = Column(DateTime(timezone=True))


class SponsoredProductsAsinsTarget(Base):
    __tablename__ = 'amz_adv_sponsored_products_asins_target'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    ASIN = Column(String(255))
    OtherASIN = Column(String(255))
    SKU = Column(String(255))
    Currency = Column(String(255))
    MatchType = Column(String(255))
    AttributedUnitsOrdered1d = Column(Float)
    AttributedUnitsOrdered7d = Column(Float)
    AttributedUnitsOrdered14d = Column(Float)
    AttributedUnitsOrdered30d = Column(Float)
    AttributedUnitsOrdered1dOtherSKU = Column(Float)
    AttributedUnitsOrdered7dOtherSKU = Column(Float)
    AttributedUnitsOrdered14dOtherSKU = Column(Float)
    AttributedUnitsOrdered30dOtherSKU = Column(Float)
    AttributedSales1dOtherSKU = Column(Float)
    AttributedSales7dOtherSKU = Column(Float)
    AttributedSales14dOtherSKU = Column(Float)
    AttributedSales30dOtherSKU = Column(Float)
    TargetId = Column(String(255))
    TargetingText = Column(Text)
    TargetingType = Column(String(255))
    Timestamp = Column(DateTime(timezone=True))


class SponsoredProductsKeyword(Base):
    __tablename__ = 'amz_adv_sponsored_products_keyword'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    KeywordId = Column(String(255), index=True)
    KeywordText = Column(Text)
    MatchType = Column(String(255))
    Impressions = Column(Float)
    Clicks = Column(Float)
    Cost = Column(Float)
    AttributedConversions1d = Column(Float)
    AttributedConversions7d = Column(Float)
    AttributedConversions14d = Column(Float)
    AttributedConversions30d = Column(Float)
    AttributedConversions1dSameSKU = Column(Float)
    AttributedConversions7dSameSKU = Column(Float)
    AttributedConversions14dSameSKU = Column(Float)
    AttributedConversions30dSameSKU = Column(Float)
    AttributedUnitsOrdered1d = Column(Float)
    AttributedUnitsOrdered7d = Column(Float)
    AttributedUnitsOrdered14d = Column(Float)
    AttributedUnitsOrdered30d = Column(Float)
    AttributedSales1d = Column(Float)
    AttributedSales7d = Column(Float)
    AttributedSales14d = Column(Float)
    AttributedSales30d = Column(Float)
    AttributedSales1dSameSKU = Column(Float)
    AttributedSales7dSameSKU = Column(Float)
    AttributedSales14dSameSKU = Column(Float)
    AttributedSales30dSameSKU = Column(Float)
    AttributedUnitsOrdered1dSameSKU = Column(Float)
    AttributedUnitsOrdered7dSameSKU = Column(Float)
    AttributedUnitsOrdered14dSameSKU = Column(Float)
    AttributedUnitsOrdered30dSameSKU = Column(Float)
    Timestamp = Column(DateTime(timezone=True))


class SponsoredProductsProductAds(Base):
    __tablename__ = 'amz_adv_sponsored_products_product_ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    Impressions = Column(Float)
    Clicks = Column(Float)
    Cost = Column(Float)
    Currency = Column(String(255))
    ASIN = Column(String(255))
    SKU = Column(String(255))
    AttributedConversions1d = Column(Float)
    AttributedConversions7d = Column(Float)
    AttributedConversions14d = Column(Float)
    AttributedConversions30d = Column(Float)
    AttributedConversions1dSameSKU = Column(Float)
    AttributedConversions7dSameSKU = Column(Float)
    AttributedConversions14dSameSKU = Column(Float)
    AttributedConversions30dSameSKU = Column(Float)
    AttributedUnitsOrdered1d = Column(Float)
    AttributedUnitsOrdered7d = Column(Float)
    AttributedUnitsOrdered14d = Column(Float)
    AttributedUnitsOrdered30d = Column(Float)
    AttributedSales1d = Column(Float)
    AttributedSales7d = Column(Float)
    AttributedSales14d = Column(Float)
    AttributedSales30d = Column(Float)
    AttributedSales1dSameSKU = Column(Float)
    AttributedSales7dSameSKU = Column(Float)
    AttributedSales14dSameSKU = Column(Float)
    AttributedSales30dSameSKU = Column(Float)
    AttributedUnitsOrdered1dSameSKU = Column(Float)
    AttributedUnitsOrdered7dSameSKU = Column(Float)
    AttributedUnitsOrdered14dSameSKU = Column(Float)
    AttributedUnitsOrdered30dSameSKU = Column(Float)
    Timestamp = Column(DateTime(timezone=True))


class SponsoredBrand(Base):
    __tablename__ = 'amz_adv_sponsored_brand'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    CampaignStatus = Column(String(255))
    CampaignBudget = Column(Float)
    CampaignBudgetType = Column(String(255))
    CampaignRuleBasedBudget = Column(Float)
    ApplicableBudgetRuleId = Column(String(255))
    ApplicableBudgetRuleName = Column(String(255))
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    KeywordId = Column(String(255), index=True)
    KeywordText = Column(Text)
    KeywordBid = Column(Float)
    KeywordStatus = Column(String(255))
    TargetId = Column(String(255))
    SearchTermImpressionRank = Column(String(255))
    TargetingExpression = Column(String(255))
    TargetingText = Column(Text)
    TargetingType = Column(String(255))
    MatchType = Column(String(255))
    Impressions = Column(Float)
    Clicks = Column(Float)
    Cost = Column(Float)
    AttributedDetailPageViewsClicks14d = Column(Float)
    AttributedSales14d = Column(Float)
    AttributedSales14dSameSKU = Column(Float)
    AttributedConversions14d = Column(Float)
    AttributedConversions14dSameSKU = Column(Float)
    AttributedOrdersNewToBrand14d = Column(Float)
    AttributedOrdersNewToBrandPercentage14d = Column(Float)
    AttributedOrderRateNewToBrand14d = Column(Float)
    AttributedSalesNewToBrand14d = Column(Float)
    AttributedSalesNewToBrandPercentage14d = Column(Float)
    AttributedUnitsOrderedNewToBrand14d = Column(Float)
    AttributedUnitsOrderedNewToBrandPercentage14d = Column(Float)
    UnitsSold14d = Column(Float)
    Dpv14d = Column(Float)
    Timestamp = Column(DateTime(timezone=True))


class SponsoredDisplay(Base):
    __tablename__ = 'amz_adv_sponsored_display'

    id = Column(Integer, primary_key=True, autoincrement=True)
    AmzAccount_ID_Internal = Column(String(255))
    AmzAccount_Group = Column(String(255))
    ReportDate = Column(Date, index=True)

    CampaignName = Column(String(255))
    CampaignId = Column(String(255), index=True)
    AdGroupName = Column(String(255))
    AdGroupId = Column(String(255), index=True)
    ASIN = Column(String(255))
    SKU = Column(String(255))
    AdId = Column(String(255), index=True)
    Impressions = Column(Float)
    Clicks = Column(Float)
    Cost = Column(Float)
    Currency = Column(String(255))
    AttributedConversions1d = Column(Float)
    AttributedConversions7d = Column(Float)
    AttributedConversions14d = Column(Float)
    AttributedConversions30d = Column(Float)
    AttributedConversions1dSameSKU = Column(Float)
    AttributedConversions7dSameSKU = Column(Float)
    AttributedConversions14dSameSKU = Column(Float)
    AttributedConversions30dSameSKU = Column(Float)
    AttributedUnitsOrdered1d = Column(Float)
    AttributedUnitsOrdered7d = Column(Float)
    AttributedUnitsOrdered14d = Column(Float)
    AttributedUnitsOrdered30d = Column(Float)
    AttributedSales1d = Column(Float)
    AttributedSales7d = Column(Float)
    AttributedSales14d = Column(Float)
    AttributedSales30d = Column(Float)
    AttributedSales1dSameSKU = Column(Float)
    AttributedSales7dSameSKU = Column(Float)
    AttributedSales14dSameSKU = Column(Float)
    AttributedSales30dSameSKU = Column(Float)
    AttributedOrdersNewToBrand14d = Column(Float)
    AttributedSalesNewToBrand14d = Column(Float)
    AttributedUnitsOrderedNewToBrand14d = Column(Float)
    Timestamp = Column(DateTime(timezone=True))