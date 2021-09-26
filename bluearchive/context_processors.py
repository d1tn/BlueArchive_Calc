from django.conf import settings

def google_analytics(request):
    """
    DEBUG=Falseの場合に、GoogleアナリティクスのトラッキングIDを返す
    """
    # GoogleアナリティクスのトラッキングIDをsettings.pyから取得する
    # settings.py内に、GOOGLE_ANALYTICS_TRACKING_ID='自分のトラッキングID'を書き込んでおく
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', False)

    # DEBUG=FalseかつGoogleアナリティクスのトラッキングIDを取得できたら、
    # テンプレート内で'GOOGLE_ANALYTICS_TRACKING_ID'という変数を利用できるようにする
    if not settings.DEBUG and ga_tracking_id:
        return {
            'GOOGLE_ANALYTICS_TRACKING_ID': ga_tracking_id,
        }
    return {}
