from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,CategoryForm,CommentForm,BlogForm
from ..models import BlogCategory,Blog,Comments
# from ..models import Review
# Review = review.Review
#display categories on the landing page
from ..request import get_quote

@main.route('/')
def index():
    """ View root page function that returns index page """

    category = BlogCategory.get_categories()

    title = 'Home- Welcome'
    return render_template('index.html', title = title, categories=category)




@main.route('/category/new-blog/<int:id>', methods=['GET', 'POST'])
#@login_required
def new_blog(id):
    ''' Function to check Blogs form and fetch data from the fields '''
    form = BlogForm()
    category = BlogCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content= form.content.data
        new_blog= Blog(content=content,category_id= category.id)
        new_blog.save_blog()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_blog.html', blog_form=form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = BlogCategory.query.get(id)
    if category is None:
        abort(404)

    blogs=Blog.get_blogs(id)
    return render_template('category.html', blogs=blogs, category=category)

@main.route('/add/category', methods=['GET','POST'])
# @login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = BlogCategory(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_category.html', category_form = form,title=title)


#view single pitch alongside its comments
@main.route('/view-blogs/<int:id>', methods=['GET', 'POST'])
# @login_required
def view_blogs(id):
    '''
    Function the returns a single pitch for comment to be added
    '''
    print(id)
    blogs = Blog.query.get(id)


    if blogs is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('view-blog.html', blogs=blogs, comment=comment, category_id=id)


#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
# @login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentForm()
    title = 'post comment'
    blogs = Blog.query.filter_by(id=id).first()

    if blogs is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, blogs_id=blogs.id)
        new_comment.save_comment()
        return redirect(url_for('.view_blogs', id=blogs.id))

    return render_template('post_comment.html', comment_form=form, title=title)
@main.route('/new_quote')
def new_quote():
    """
    """
    quote = get_quote()

    return render_template('quote.html', quote=quote)