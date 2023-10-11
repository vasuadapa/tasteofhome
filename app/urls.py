from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('catering/', views.catering, name='catering'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-password/', views.verify_password, name='verify_password'),

    path('menu/', views.menu, name='menu'),
    path('takeaway/', views.takeaway, name='takeaway'),
    path('delivery/', views.delivery, name='delivery'),
    path('user-ajax-addtocart/', views.user_ajax_addtocart, name='user_ajax_addtocart'),


    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.sign_out, name='sign_out'),

    path('user-admin/', views.user_admin, name='user_admin'),
    path('user-admin-address-active/', views.user_admin_address_active, name='user_admin_address_active'),

    path('admin-logout/', views.admin_sign_out, name='admin_sign_out'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('address-update/', views.address_update, name='address_update'),
    path('address-delete/<int:id>/', views.address_delete, name='address_delete'),
    path('user-ajax-address-edit/', views.user_ajax_address_edit, name='user_ajax_address_edit'),
    path('user-edit-address-update/', views.user_edit_address_update, name='user_edit_address_update'),

    path('subscription/', views.subscription, name='subscription'),
    path('subscription-details/<str:id>/', views.subscription_details, name='subscription_details'),
    path('subscription-update/', views.subscription_update, name='subscription_update'),


    path('order/', views.order, name='order'),
    path('admin-ajax-order/', views.admin_ajax_order, name='admin_ajax_order'),
    path('order-details/<int:id>/', views.order_details, name='order_details'),
    path('admin-ajax-order-subscription/', views.admin_ajax_order_subscription, name='admin_ajax_order_subscription'),

    path('driver/', views.driver1, name='driver1'),
    path('admin-orders-payment/<int:id>/', views.admin_orders_payment, name='admin_orders_payment'),
    path('driver-orders-completed/<int:id>/', views.driver_orders_completed, name='driver_orders_completed'),
    path('driver-orders-decline/<int:id>/', views.driver_orders_decline, name='driver_orders_decline'),

    #admin
    path('admin-index/', views.admin_index, name='admin_index'),

    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('admin-categories-edit/', views.admin_categories_edit, name='admin_categories_edit'),
    path('admin-categories-edit-value/', views.admin_categories_ed, name='admin_categories_ed'),
    path('admin-categories-delete/<int:id>/', views.admin_categories_delete, name='admin_categories_delete'),

    path('admin-items/', views.admin_items, name='admin_items'),
    path('admin-item-ajax-edit/', views.admin_item_ajax_edit, name='admin_item_ajax_edit'),
    path('admin-item-edit/', views.admin_item_edit, name='admin_item_edit'),
    path('admin-items-delete/<int:id>/', views.admin_items_delete, name='admin_items_delete'),

    path('admin-meals/', views.admin_meals, name='admin_meals'),
    path('admin-meals-edit/<int:id>/', views.admin_meals_edit, name='admin_meals_edit'),
    path('admin-get-items/', views.admin_ajax_get_items, name='admin_ajax_get_items'),
    path('admin-meals-delete/<int:id>/', views.admin_meals_delete, name='admin_meals_delete'),
    path('admin-meals-update-special/', views.admin_meals_update_special, name='admin_meals_update_special'),


    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-ajax-order-make-paid/', views.admin_orders_ajax_order_make_paid, name='admin_orders_ajax_order_make_paid'),


    path('admin-orders-delete/<int:id>/', views.admin_orders_delete, name='admin_orders_delete'),
    path('admin-orders-delivered/<int:id>/', views.admin_orders_delivered, name='admin_orders_delivered'),
    path('admin-orders-edit/<int:id>/', views.admin_orders_edit, name='admin_orders_edit'),
    path('admin-orders-decline/<int:id>/', views.admin_orders_decline, name='admin_orders_decline'),
    path('admin-orders-refund/<int:id>/', views.admin_orders_refund, name='admin_orders_refund'),


    path('admin-todayreport/', views.admin_todayreport, name='admin_todayreport'),
    path('admin-daliyorder/', views.admin_dailyorder, name='admin_dailyorder'),

    path('admin-takeaway-close-time/', views.admin_takeaway_close_time, name='admin_takeaway_close_time'),

    path('admin-suburb/', views.admin_suburb, name='admin_suburb'),
    path('admin-suburb-edit/<int:id>/', views.admin_suburb_edit, name='admin_suburb_edit'),
    path('admin-suburb-delete/<int:id>/', views.admin_suburb_delete, name='admin_suburb_delete'),
    path('admin-add-suburb/', views.admin_add_suburb, name='admin_add_suburb'),


    path('admin-drivers/', views.admin_drivers, name='admin_drivers'),
    path('admin-driver-ajax-edit/', views.admin_driver_ajax_edit, name='admin_driver_ajax_edit'),
    path('admin-driver-edit/', views.admin_driver_edit, name='admin_driver_edit'),
    path('admin-drivers-delete/<int:id>/', views.admin_driver_delete, name='admin_driver_delete'),


    path('admin-deliverytifin/', views.admin_deliverytifin, name='admin_deliverytifin'),
    path('admin-driver-orders/<int:id>/', views.admin_order_details_1, name='admin_order_details_1'),


    path('admin-customers/', views.admin_customers, name='admin_customers'),
    path('admin-customers-profile/<int:id>/', views.admin_customers_profile, name='admin_customers_profile'),
    path('admin-customers-password/<int:id>/', views.admin_customers_password, name='admin_customers_password'),
    path('admin-customers-orders-details/<int:id>/', views.admin_customers_orders_details, name='admin_customers_orders_details'),

    path('admin-user-active/', views.admin_user_update_special, name='admin_user_update_special'),
    path('admin-get-user/', views.admin_ajax_get_user, name='admin_ajax_get_user'),
    path('admin-customer-dashboard/', views.admin_customer_dashboard, name='admin_customer_dashboard'),


    path('admin-balance-edit/<int:id>/', views.admin_bal_edit, name='admin_bal_edit'),
    path('admin-balance-delete/<int:id>/', views.admin_bal_delete, name='admin_bal_delete'),
    path('admin-balance-ajax-edit/', views.admin_ajax_balance_edit, name='admin_ajax_balance_edit'),

    path('admin-note-edit/<int:id>/', views.admin_note_edit, name='admin_note_edit'),
    path('admin-note-delete/<int:id>/', views.admin_note_delete, name='admin_note_delete'),
    path('admin-note-ajax-edit/', views.admin_ajax_note_edit, name='admin_ajax_note_edit'),

    path('admin-customers-balance/<int:id>/', views.admin_customers_balance, name='admin_customers_balance'),
    path('admin-customers-note/<int:id>/', views.admin_customers_note, name='admin_customers_note'),


    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-add-users/', views.admin_add_users, name='admin_add_users'),

    path('admin-sizes/', views.admin_sizes, name='admin_sizes'),
    path('admin-sizes-delete/<int:id>/', views.admin_sizes_delete, name='admin_sizes_delete'),

    path('admin-variations/', views.admin_variations, name='admin_variations'),
    path('admin-variations-ajax-edit/', views.admin_ajax_variations_edit, name='admin_ajax_variations_edit'),
    path('admin-variations-edit-value/', views.admin_variations_edit, name='admin_variations_edit'),
    path('admin-variations-delete/<int:id>/', views.admin_variations_delete, name='admin_variations_delete'),

    path('admin-subscription/', views.admin_subscription, name='admin_subscription'),
    path('admin-subscription-plans/', views.admin_subscription_plans, name='admin_subscription_plans'),

    path('admin-catering-menu/', views.admin_catering_menu, name='admin_catering_menu'),

    path('admin-promocode/', views.admin_promocode, name='admin_promocode'),
    path('admin-promocode-ajax-edit/', views.admin_ajax_promocode_edit, name='admin_ajax_promocode_edit'),
    path('admin-promocode-edit/', views.admin_promocode_edit, name='admin_promocode_edit'),
    path('admin-promocode-completed/<int:id>/', views.admin_promocode_completed, name='admin_promocode_completed'),
    path('admin-promocode-delete/<int:id>/', views.admin_promocode_delete, name='admin_promocode_delete'),

    path('admin-user-subscription-details/', views.admin_user_subscription_details, name='admin_user_subscription_details'),
    path('admin-login/', views.admin_login, name='admin_login'),

    path('admin-salesreport/', views.admin_salesreport, name='admin_salesreport'),
    path('admin-orderreport/', views.admin_orderreport, name='admin_orderreport'),
    path('admin-itemreport/', views.admin_itemreport, name='admin_itemreport'),
    path('admin-subrreport/', views.admin_suburreport, name='admin_suburreport'),

    path('admin-timing/', views.admin_timing, name='admin_timing'),
    path('admin-subrreport/', views.admin_closedate, name='admin_closedate'),

    # footer links
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('indian-tiffin-service-springvale-noble-park/', views.indian_tiffin_service_springvale_noble_park, name='indian_tiffin_service_springvale_noble_park'),
    path('indian-tiffin-service-mount-waverley/', views.indian_tiffin_service_mount_waverley, name='indian_tiffin_service_mount_waverley'),
    path('indian-tiffin-service-melbourne/', views.indian_tiffin_service_melbourne, name='indian_tiffin_service_melbourne'),
    path('indian-tiffin-service-hampton-park/', views.indian_tiffin_service_hampton_park, name='indian_tiffin_service_hampton_park'),
    path('indian-tiffin-service-cranbourne/', views.indian_tiffin_service_cranbourne, name='indian_tiffin_service_cranbourne'),
    path('indian-tiffin-service-dandenong/', views.indian_tiffin_service_dandenong, name='indian_tiffin_service_dandenong'),
    path('indian-tiffin-service-clayton-keysborough/', views.indian_tiffin_service_clayton_keysborough, name='indian_tiffin_service_clayton_keysborough'),




    ]
urlpatterns += staticfiles_urlpatterns()
