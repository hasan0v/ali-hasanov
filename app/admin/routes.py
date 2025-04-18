from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from . import admin
from ..models import User, Post, Category, Tag, Service, ServicePlan, Project, ProjectImage, AITool, Contact, PostTag
from ..forms import PostForm, ServiceForm, ProjectForm, AIToolForm
from slugify import slugify
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from peewee import fn, DoesNotExist

# Admin role verification decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    # Dashboard statistics
    post_count = Post.select().count()
    service_count = Service.select().count()
    project_count = Project.select().count()
    tool_count = AITool.select().count()
    contact_count = Contact.select().where(Contact.read == False).count()
    
    return render_template('admin/index.html', 
                          post_count=post_count,
                          service_count=service_count,
                          project_count=project_count,
                          tool_count=tool_count,
                          contact_count=contact_count)

# Blog management
@admin.route('/posts')
@login_required
@admin_required
def posts():
    posts = Post.select().order_by(Post.created_at.desc())
    return render_template('admin/posts.html', posts=posts)

@admin.route('/posts/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = PostForm()
    # Populate category dropdown
    form.category.choices = [(c.id, c.name) for c in Category.select()]
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            slug=slugify(form.title.data),
            content=form.content.data,
            summary=form.summary.data,
            published=form.published.data,
            user=current_user.id
        )
        
        if form.category.data:
            try:
                category = Category.get_by_id(form.category.data)
                post.category = category
            except DoesNotExist:
                pass
                
        post.save()
        flash('Post created successfully!')
        return redirect(url_for('admin.posts'))
        
    return render_template('admin/post_form.html', form=form, title='Create Post')

@admin.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(id):
    try:
        post = Post.get_by_id(id)
        form = PostForm()
        form.category.choices = [(c.id, c.name) for c in Category.select()]
        
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = slugify(form.title.data)
            post.content = form.content.data
            post.summary = form.summary.data
            post.published = form.published.data
            post.updated_at = datetime.now()
            
            if form.category.data:
                try:
                    category = Category.get_by_id(form.category.data)
                    post.category = category
                except DoesNotExist:
                    pass
            
            post.save()
            flash('Post updated successfully!')
            return redirect(url_for('admin.posts'))
        
        # Populate form with existing data
        if request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            form.summary.data = post.summary
            form.published.data = post.published
            form.category.data = post.category.id if post.category else None
        
        return render_template('admin/post_form.html', form=form, title='Edit Post')
    except DoesNotExist:
        abort(404)

@admin.route('/posts/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_post(id):
    try:
        post = Post.get_by_id(id)
        post.delete_instance(recursive=True)  # Also delete related records
        flash('Post deleted successfully!')
    except DoesNotExist:
        flash('Post not found.', 'error')
    return redirect(url_for('admin.posts'))

# Categories management
@admin.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.select()
    return render_template('admin/categories.html', categories=categories)

@admin.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category = Category(name=name, slug=slugify(name))
            category.save()
            flash('Category created successfully!')
            return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', title='Create Category')

@admin.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    try:
        category = Category.get_by_id(id)
        category.delete_instance()
        flash('Category deleted successfully!')
    except DoesNotExist:
        flash('Category not found.', 'error')
    return redirect(url_for('admin.categories'))

# Service management
@admin.route('/services')
@login_required
@admin_required
def services():
    services = Service.select().order_by(Service.title)
    return render_template('admin/services.html', services=services)

@admin.route('/services/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_service():
    form = ServiceForm()
    
    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            slug=slugify(form.title.data),
            description=form.description.data,
            short_description=form.short_description.data,
            featured=form.featured.data
        )
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join('app', 'static', 'uploads', 'services', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.image.data.save(filepath)
            service.image = f'uploads/services/{filename}'
            
        service.save()
        flash('Xidmət uğurla əlavə edildi!')
        return redirect(url_for('admin.services'))
        
    return render_template('admin/service_form.html', form=form, title='Yeni Xidmət')

@admin.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    try:
        service = Service.get_by_id(id)
        form = ServiceForm(obj=service)
        
        if form.validate_on_submit():
            service.title = form.title.data
            service.slug = slugify(form.title.data)
            service.description = form.description.data
            service.short_description = form.short_description.data
            service.featured = form.featured.data
            service.updated_at = datetime.now()
            
            if form.image.data:
                # Remove old image if exists
                if service.image:
                    old_image_path = os.path.join('app', 'static', service.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join('app', 'static', 'uploads', 'services', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                form.image.data.save(filepath)
                service.image = f'uploads/services/{filename}'
            
            service.save()
            flash('Xidmət uğurla yeniləndi!')
            return redirect(url_for('admin.services'))
        
        return render_template('admin/service_form.html', form=form, service=service, title='Xidməti Redaktə Et')
    
    except DoesNotExist:
        abort(404)

@admin.route('/services/delete/<int:id>')
@login_required
@admin_required
def delete_service(id):
    try:
        service = Service.get_by_id(id)
        
        # Delete associated service plans
        for plan in service.service_plans:
            plan.delete_instance()
        
        # Delete the service
        service.delete_instance()
        flash('Xidmət uğurla silindi!')
        
    except DoesNotExist:
        flash('Xidmət tapılmadı!', 'error')
    
    return redirect(url_for('admin.services'))

@admin.route('/services/<int:service_id>/plans')
@login_required
@admin_required
def service_plans(service_id):
    try:
        service = Service.get_by_id(service_id)
        plans = ServicePlan.select().where(ServicePlan.service == service)
        return render_template('admin/service_plans.html', service=service, plans=plans)
    except DoesNotExist:
        abort(404)

@admin.route('/services/<int:service_id>/plans/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_service_plan(service_id):
    try:
        service = Service.get_by_id(service_id)
        # Your form handling code here for creating a service plan
        # ...

        return render_template('admin/service_plan_form.html', service=service, title='Yeni Plan')
    except DoesNotExist:
        abort(404)

# Project management
@admin.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.select().order_by(Project.title)
    return render_template('admin/projects.html', projects=projects)

@admin.route('/projects/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_project():
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            slug=slugify(form.title.data),
            short_description=form.short_description.data,
            description=form.description.data,
            client=form.client.data,
            completion_date=form.completion_date.data,
            technologies_used=form.technologies_used.data,
            project_url=form.project_url.data,
            featured=form.featured.data
        )
        
        if form.thumbnail.data:
            filename = secure_filename(form.thumbnail.data.filename)
            filepath = os.path.join('app', 'static', 'uploads', 'projects', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.thumbnail.data.save(filepath)
            project.thumbnail = f'uploads/projects/{filename}'
            
        project.save()
        flash('Layihə uğurla əlavə edildi!')
        return redirect(url_for('admin.projects'))
        
    return render_template('admin/project_form.html', form=form, title='Yeni Layihə')

@admin.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    try:
        project = Project.get_by_id(id)
        form = ProjectForm(obj=project)
        
        if form.validate_on_submit():
            project.title = form.title.data
            project.slug = slugify(form.title.data)
            project.short_description = form.short_description.data
            project.description = form.description.data
            project.client = form.client.data
            project.completion_date = form.completion_date.data
            project.technologies_used = form.technologies_used.data
            project.project_url = form.project_url.data
            project.featured = form.featured.data
            
            if form.thumbnail.data:
                # Remove old thumbnail if exists
                if project.thumbnail:
                    old_thumbnail_path = os.path.join('app', 'static', project.thumbnail)
                    if os.path.exists(old_thumbnail_path):
                        os.remove(old_thumbnail_path)
                
                filename = secure_filename(form.thumbnail.data.filename)
                filepath = os.path.join('app', 'static', 'uploads', 'projects', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                form.thumbnail.data.save(filepath)
                project.thumbnail = f'uploads/projects/{filename}'
            
            project.save()
            flash('Layihə uğurla yeniləndi!')
            return redirect(url_for('admin.projects'))
        
        return render_template('admin/project_form.html', form=form, project=project, title='Layihəni Redaktə Et')
    
    except DoesNotExist:
        abort(404)

@admin.route('/projects/delete/<int:id>')
@login_required
@admin_required
def delete_project(id):
    try:
        project = Project.get_by_id(id)
        
        # Delete associated project images
        for image in project.images:
            # Remove image file
            if image.image_url:
                image_path = os.path.join('app', 'static', image.image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
            image.delete_instance()
        
        # Delete the project
        project.delete_instance()
        flash('Layihə uğurla silindi!')
        
    except DoesNotExist:
        flash('Layihə tapılmadı!', 'error')
    
    return redirect(url_for('admin.projects'))

@admin.route('/projects/<int:project_id>/images')
@login_required
@admin_required
def project_images(project_id):
    try:
        project = Project.get_by_id(project_id)
        images = ProjectImage.select().where(ProjectImage.project == project)
        return render_template('admin/project_images.html', project=project, images=images)
    except DoesNotExist:
        abort(404)

@admin.route('/projects/<int:project_id>/images/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_project_image(project_id):
    try:
        project = Project.get_by_id(project_id)
        
        if request.method == 'POST':
            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('app', 'static', 'uploads', 'projects', 'gallery', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    
                    image = ProjectImage(
                        project=project,
                        image_url=f'uploads/projects/gallery/{filename}',
                        caption=request.form.get('caption', '')
                    )
                    image.save()
                    flash('Şəkil uğurla əlavə edildi!')
            
            return redirect(url_for('admin.project_images', project_id=project_id))
        
        return render_template('admin/project_image_form.html', project=project)
    
    except DoesNotExist:
        abort(404)

@admin.route('/projects/images/delete/<int:image_id>')
@login_required
@admin_required
def delete_project_image(image_id):
    try:
        image = ProjectImage.get_by_id(image_id)
        project_id = image.project.id
        
        # Delete image file
        if image.image_url:
            image_path = os.path.join('app', 'static', image.image_url)
            if os.path.exists(image_path):
                os.remove(image_path)
                
        image.delete_instance()
        flash('Şəkil uğurla silindi!')
        
        return redirect(url_for('admin.project_images', project_id=project_id))
    
    except DoesNotExist:
        abort(404)

# AI Tools management
@admin.route('/tools')
@login_required
@admin_required
def tools():
    tools = AITool.select().order_by(AITool.name)
    return render_template('admin/tools.html', tools=tools)

@admin.route('/tools/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tool():
    form = AIToolForm()
    
    if form.validate_on_submit():
        tool = AITool(
            name=form.name.data,
            slug=slugify(form.name.data),
            description=form.description.data,
            url=form.url.data,
            category=form.category.data,
            featured=form.featured.data
        )
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join('app', 'static', 'uploads', 'tools', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.image.data.save(filepath)
            tool.image = f'uploads/tools/{filename}'
            
        tool.save()
        flash('AI aləti uğurla əlavə edildi!')
        return redirect(url_for('admin.tools'))
        
    return render_template('admin/tool_form.html', form=form, title='Yeni AI Aləti')

@admin.route('/tools/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tool(id):
    try:
        tool = AITool.get_by_id(id)
        form = AIToolForm(obj=tool)
        
        if form.validate_on_submit():
            tool.name = form.name.data
            tool.slug = slugify(form.name.data)
            tool.description = form.description.data
            tool.url = form.url.data
            tool.category = form.category.data
            tool.featured = form.featured.data
            
            if form.image.data:
                # Remove old image if exists
                if tool.image:
                    old_image_path = os.path.join('app', 'static', tool.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join('app', 'static', 'uploads', 'tools', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                form.image.data.save(filepath)
                tool.image = f'uploads/tools/{filename}'
            
            tool.save()
            flash('AI aləti uğurla yeniləndi!')
            return redirect(url_for('admin.tools'))
        
        return render_template('admin/tool_form.html', form=form, tool=tool, title='AI Alətini Redaktə Et')
    
    except DoesNotExist:
        abort(404)

@admin.route('/tools/delete/<int:id>')
@login_required
@admin_required
def delete_tool(id):
    try:
        tool = AITool.get_by_id(id)
        
        # Delete image file if exists
        if tool.image:
            image_path = os.path.join('app', 'static', tool.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete the tool
        tool.delete_instance()
        flash('AI aləti uğurla silindi!')
        
    except DoesNotExist:
        flash('AI aləti tapılmadı!', 'error')
    
    return redirect(url_for('admin.tools'))

# Generic image upload for rich text editor
@admin.route('/upload-image', methods=['POST'])
@login_required
@admin_required
def upload_image():
    if 'upload' in request.files:
        file = request.files['upload']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join('app', 'static', 'uploads', 'editor', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Return CKEditor compatible response
            return {
                'uploaded': 1,
                'fileName': filename,
                'url': url_for('static', filename=f'uploads/editor/{filename}')
            }
    
    return {
        'uploaded': 0,
        'error': {'message': 'Upload failed'}
    }
