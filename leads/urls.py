from django.urls import path
from .views import (lead_delete, PerfilView, PerfilDetailView, gerenciar,
                    robos_list, lead_detail, create_robo, lead_update, robo_update, robo_delete, carrinho, OrderSummaryView, remove_single_item_from_cart, remove_from_cart, Pagamento)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "leads"

urlpatterns = [
    path('', robos_list, name='lead-list'),
    path('<int:pk>/', lead_detail, name='lead-detail'),
    path('<int:pk>/delete/', lead_delete, name='lead-delete'),
    path('<int:pk>/deleterob/', robo_delete, name='robo-delete'),
    path('criar/', create_robo, name='criar-robos'),
    path('mercado/', robos_list, name='mercado'),
    path('adicionar-ao-carrinho/<slug>/', carrinho, name='add-to-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart,
         name='remove-from-cart'),
    path('carrinho/', OrderSummaryView.as_view(), name='order-summary'),
    path('gerenciar/', gerenciar, name='gerenciar-robos'),
    path('perfil/', PerfilView, name='perfil-view'),
    path('<int:pk>/update/', lead_update, name='perfil-update'),
    path('<int:pk>/updaterob/', robo_update, name='robo-update'),
    path('<int:pk>/perfil/', PerfilDetailView.as_view(), name='perfil-detail'),
    path('pagamento/<int:pk>', Pagamento.as_view(), name='pagamento'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()