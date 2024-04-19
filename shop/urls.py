from django.urls import path
from .Api.auth import CustomTokenObtainPairView, LoginView, LogoutView, VerifyUserToken
from .Api.user import (
        CreateUserView,
    UpdateUserView,
    ChangeUserStateView,
    CustomUserDetailView,
)
from .Api.category import CategoryList, CategoriesWithProductsView, CategoriesByShopView, ShopCategoriesAPIView
from .Api.product import  (    
    # Product management views
    ProductListCreateView,
    ProductDetailAPIView,
    ProductRetrieveUpdateDestroyView,
    ProductUpdateView,
    ProductDeleteView,
    # Product filtering and searching views
    ProductsByShopView,
    ProductsByCategoryShop,
    ProductsByShopAndSubcategoryView,
    ProductsByCategory,
    ProductsByShopAndBestDiscountView,
    ProductsSearchView,
    search_products)
from .Api.shop import (
    ProductShopView,
    ShopProductsListView
)
from .Api.subcategory import (

    SubCategoryList,
)

urlpatterns = [
    # ====================
    # User Management URLs
    # ====================
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('update_user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('change_user_state/<int:pk>/', ChangeUserStateView.as_view(), name='change_user_state'),
    path('users/<str:username>/', CustomUserDetailView.as_view(), name='custom-user-detail'),
    path('token/verify/', VerifyUserToken.as_view(), name='verify_user_token'),

    # =====================
    # Product Management URLs
    # =====================
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('product/<int:product_id>/shop/', ProductShopView.as_view(), name='product_shop'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete-product'),
    path('shop/<int:shop_id>/products/', ShopProductsListView.as_view(), name='shop-products-list'),

    # ==================================
    # Product Filtering and Searching URLs
    # ==================================
    path('products/shop/<int:shop_id>/', ProductsByShopView.as_view()),
    path('products/shop/<int:shop_id>/category/<int:category_id>/', ProductsByCategoryShop.as_view()),
    path('products/shop/<int:shop_id>/subcategory/<int:subcategory_id>/', ProductsByShopAndSubcategoryView.as_view()),
    path('products/category/<int:category_id>/', ProductsByCategory.as_view(), name='products-by-category'),
    path('categories/categories-with-products/', CategoriesWithProductsView.as_view(), name='categories-with-products'),
    path('products/shop/<str:shop_id>/best_discount/', ProductsByShopAndBestDiscountView.as_view()),
    path('products/search/', ProductsSearchView.as_view()),
    path('search_products/', search_products, name='search_products'),

    # ==============================
    # Category and Subcategory Management URLs
    # ==============================
    path('categories_with_products/', CategoriesWithProductsView.as_view(), name='categories-with-products'),
    path('categories/shop/<int:shop_id>/', CategoriesByShopView.as_view(), name='categories-by-shop'),
    path('categories/', CategoryList.as_view(), name='user-category-list'),
    path('subcategories/', SubCategoryList.as_view(), name='subcategories-list'),
    path('categories/shop/<int:shop_id>/', ShopCategoriesAPIView.as_view(), name='shop-categories'),
]