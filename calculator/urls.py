from django.conf.urls import url

from . import views


urlpatterns = [
    # url(r'^$', views., name='list_all_products'),
    # url(r'^(?P<category_slug>[-\w]*)/$', views.list_products, name='list_products_by_category'),
    # url(r'^(?P<category_slug>[-\w]+)/(?P<id>\d+)-(?P<product_slug>[-\w]+)/$',
    #     views.render_product_page, name='render_product')
    url(r'^$', views.main_page, name='main_page'),
    url(r'^programs/(?P<pk>\d+)/$', views.ProgramDetailView.as_view(), name='program_details'),
]