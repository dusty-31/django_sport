from django.contrib import admin

from blog.models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Контент', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Налаштування', {
            'fields': ('status', 'is_featured', 'reading_time')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username']
    list_editable = ['is_approved']
    raw_id_fields = ['post', 'parent']