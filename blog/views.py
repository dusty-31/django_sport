from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from blog.models import Post, Category, Tag, Comment

class BlogView(TemplateView):
    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо опубліковані пости
        posts = Post.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')

        # Фільтрація за категорією
        category_slug = self.request.GET.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)

        # Фільтрація за тегом
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            posts = posts.filter(tags__slug=tag_slug)

        # Пошук
        search_query = self.request.GET.get('search')
        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Пагінація
        paginator = Paginator(posts, 6)  # 6 постів на сторінку
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Рекомендовані пости
        featured_posts = Post.objects.filter(status='published', is_featured=True)[:3]

        # Популярні пости
        popular_posts = Post.objects.filter(status='published').order_by('-views_count')[:5]

        # Категорії та теги
        categories = Category.objects.filter(is_active=True).annotate(posts_count=Count('posts'))
        tags = Tag.objects.annotate(posts_count=Count('post')).filter(posts_count__gt=0)

        context.update({
            'posts': page_obj,
            'featured_posts': featured_posts,
            'popular_posts': popular_posts,
            'categories': categories,
            'tags': tags,
            'current_category': category_slug,
            'current_tag': tag_slug,
            'search_query': search_query,
        })

        return context


class BlogPostView(TemplateView):
    template_name = 'blog/blog_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=kwargs['slug'], status='published')
        post.increment_views()
        related_posts = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id)[:3]
        comments = post.comments.filter(is_approved=True, parent=None).select_related('author')
        prev_post = Post.objects.filter(
            status='published',
            created_at__lt=post.created_at
        ).first()
        next_post = Post.objects.filter(
            status='published',
            created_at__gt=post.created_at
        ).last()
        context.update({
            'post': post,
            'related_posts': related_posts,
            'comments': comments,
            'prev_post': prev_post,
            'next_post': next_post,
        })

        return context


class BlogCategoryView(TemplateView):
    template_name = '/blog_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=kwargs['slug'], is_active=True)
        posts = Post.objects.filter(
            status='published',
            category=category
        ).select_related('author').prefetch_related('tags')
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update({
            'category': category,
            'posts': page_obj,
        })
        return context


class BlogTagView(TemplateView):
    template_name = 'blog/blog_tag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=kwargs['slug'])
        posts = Post.objects.filter(
            status='published',
            tags=tag
        ).select_related('category', 'author').prefetch_related('tags')
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'tag': tag,
            'posts': page_obj,
        })

        return context