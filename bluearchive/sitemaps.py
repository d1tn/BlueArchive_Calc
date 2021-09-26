# myproject/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class CalcSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return resolve_url('blog:detail', pk=obj.pk)

    def lastmod(self, obj):
        return obj.created_at


class StaticViewSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['blog:index', 'blog:category_list', 'blog:tag_list']

    def location(self, item):
        return reverse(item)
