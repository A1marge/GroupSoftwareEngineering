from django.urls import path
from apps.crates.views import crate_shop, crate_inventory, buy_crate, open_crate, bulk_open_crates, item_inventory, \
    bulk_buy_crates, sell_item

urlpatterns = [
    path("shop/", crate_shop, name="crate_shop"),
    path("inventory/", crate_inventory, name="crate_inventory"),
    path("items/", item_inventory, name="item_inventory"),  # New URL for item inventory
    path("buy/<str:crate_type>/", buy_crate, name="buy_crate"),
    path("open/<str:crate_type>/", open_crate, name="open_crate"),
    path("bulk_open/<str:crate_type>/", bulk_open_crates, name="bulk_open_crates"),
    path("buy/bulk/<str:crate_type>/", bulk_buy_crates, name="bulk_buy_crate"),
    path("items/sell/<int:item_id>/", sell_item, name="sell_item"),
]