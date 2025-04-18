from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from . import main
from .. import cache
from ..models import User, Post, Category, Tag, Service, ServicePlan, Project, ProjectImage, AITool, Contact
from ..forms import ContactForm, PostForm, ServiceForm, ProjectForm, AIToolForm
from peewee import JOIN, fn, DoesNotExist

@main.route('/')
@cache.cached(timeout=60)
def home():
    # Fetch featured content for the homepage
    featured_posts = (Post
                      .select()
                      .where(Post.published == True)
                      .order_by(Post.created_at.desc())
                      .limit(3))
    
    featured_services = (Service
                         .select()
                         .where(Service.featured == True)
                         .limit(4))
    
    featured_projects = (Project
                         .select()
                         .where(Project.featured == True)
                         .limit(3))
    
    return render_template('home.html', 
                          featured_posts=featured_posts,
                          featured_services=featured_services,
                          featured_projects=featured_projects)

@main.route('/about')
@cache.cached(timeout=300)
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_message = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        contact_message.save()
        flash('Your message has been sent. Thank you!')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

# Services pages
@main.route('/services')
@cache.cached(timeout=180)
def services():
    services_list = Service.select().order_by(Service.title)
    return render_template('services.html', services=services_list)

@main.route('/services/<slug>')
@cache.cached(timeout=180)
def service_detail(slug):
    try:
        service = Service.get(Service.slug == slug)
        plans = ServicePlan.select().where(ServicePlan.service == service)
        
        # Get related services (excluding current one)
        related_services = (Service
                          .select()
                          .where(Service.id != service.id)
                          .order_by(fn.Random())
                          .limit(3))
        
        return render_template('service_detail.html', 
                              service=service, 
                              plans=plans,
                              related_services=related_services)
    except DoesNotExist:
        abort(404)

# Projects pages
@main.route('/projects')
@cache.cached(timeout=180) # Consider cache timeout if filtering often
def projects():
    # Get categories that have projects associated with them
    # Assumes Project model has a 'category' ForeignKey field added
    try:
        categories = (Category
                      .select()
                      .join(Project) # Join based on the foreign key
                      .where(Project.category.is_null(False))
                      .group_by(Category.id)
                      .order_by(Category.name))
    except Exception as e:
        # Handle case where Project.category doesn't exist yet or other errors
        print(f"Error fetching categories for projects: {e}")
        categories = [] # Pass empty list if category relation isn't ready

    selected_category_slug = request.args.get('category')
    query = Project.select().order_by(Project.completion_date.desc(), Project.created_at.desc()) # Example ordering

    if selected_category_slug:
        try:
            # Assumes Project model has a 'category' ForeignKey field added
            selected_category = Category.get(Category.slug == selected_category_slug)
            query = query.where(Project.category == selected_category)
        except DoesNotExist:
            flash(f"Kateqoriya '{selected_category_slug}' tapılmadı.", "warning")
            selected_category_slug = None # Reset selection if category not found
        except Exception as e:
            # Handle case where Project.category doesn't exist yet or other errors
            print(f"Error filtering projects by category '{selected_category_slug}': {e}")
            flash("Layihələri kateqoriyaya görə filterləmək mümkün olmadı.", "danger")
            selected_category_slug = None # Reset selection on error

    projects_list = query
    return render_template('projects.html',
                          projects=projects_list,
                          categories=categories,
                          selected_category=selected_category_slug) # Pass slug for button styling

@main.route('/projects/<slug>')
@cache.cached(timeout=180)
def project_detail(slug):
    try:
        project = Project.get(Project.slug == slug)
        images = ProjectImage.select().where(ProjectImage.project == project)
        
        # Get related projects (excluding current one)
        related_projects = (Project
                          .select()
                          .where(Project.id != project.id)
                          .order_by(fn.Random())
                          .limit(3))
        
        return render_template('project_detail.html', 
                             project=project, 
                             images=images,
                             related_projects=related_projects)
    except DoesNotExist:
        abort(404)

# AI Tools pages
@main.route('/ai-tools')
@cache.cached(timeout=180)
def ai_tools():
    # Get unique categories for filtering
    categories = (AITool
                  .select(AITool.category)
                  .where(AITool.category.is_null(False))
                  .distinct()
                  .order_by(AITool.category))
    
    # Filter by category if provided
    category = request.args.get('category')
    
    if category:
        tools = (AITool
                .select()
                .where(AITool.category == category)
                .order_by(AITool.name))
    else:
        tools = AITool.select().order_by(AITool.name)
        
    return render_template('ai_tools.html', tools=tools, categories=categories, selected_category=category)

@main.route('/ai-tools/<slug>')
@cache.cached(timeout=180)
def ai_tool_detail(slug):
    try:
        tool = AITool.get(AITool.slug == slug)
        
        # Get similar tools from the same category (if available)
        if tool.category:
            similar_tools = (AITool
                           .select()
                           .where((AITool.category == tool.category) & (AITool.id != tool.id))
                           .order_by(fn.Random())
                           .limit(5))
        else:
            similar_tools = (AITool
                           .select()
                           .where(AITool.id != tool.id)
                           .order_by(fn.Random())
                           .limit(5))
        
        # Get related blog posts
        related_posts = (Post
                       .select()
                       .where(Post.published == True)
                       .order_by(fn.Random())
                       .limit(3))
        
        return render_template('ai_tool_detail.html', 
                             tool=tool, 
                             similar_tools=similar_tools,
                             related_posts=related_posts)
    except DoesNotExist:
        abort(404)

# Blog pages
@main.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    
    total_posts = Post.select().where(Post.published == True).count()
    total_pages = (total_posts + per_page - 1) // per_page
    
    posts = (Post
            .select()
            .where(Post.published == True)
            .order_by(Post.created_at.desc())
            .paginate(page, per_page))
    
    categories = Category.select()
    
    return render_template('blog.html', 
                          posts=posts, 
                          page=page, 
                          total_pages=total_pages,
                          categories=categories)

@main.route('/blog/<slug>')
def blog_post(slug):
    try:
        post = Post.get((Post.slug == slug) & (Post.published == True))
        
        # Get related posts based on category
        related_posts = (Post
                        .select()
                        .where((Post.category == post.category) & 
                              (Post.id != post.id) & 
                              (Post.published == True))
                        .limit(3))
        
        # Get all categories for sidebar
        categories = Category.select().order_by(Category.name)
        
        return render_template('blog_post.html', 
                              post=post, 
                              related_posts=related_posts,
                              categories=categories)
    except DoesNotExist:
        abort(404)

# Static pages
@main.route('/faq')
@cache.cached(timeout=600)
def faq():
    return render_template('faq.html')

@main.route('/terms')
@cache.cached(timeout=600)
def terms():
    return render_template('terms.html')

@main.route('/privacy')
@cache.cached(timeout=600)
def privacy():
    return render_template('privacy.html')
