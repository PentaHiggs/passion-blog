from datetime import timedelta
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from django.utils import timezone
from django.utils.http import urlquote, urlunquote
from django.utils.html import strip_tags, escape

from django.template.loader import render_to_string
from django.template import RequestContext

from blog.models import BlogPost, BlogComment, Author


def retrieve_query(from_, name, default):
    """Retrieves a value from a dictionary, if not found defaults to default"""
    try:
        value = from_.__getitem__(name)
    except KeyError:
        return default
    return value

def generate_archive_months():
    """Returns a list of triples, e.g. (2013, 2, "February"),
    containing the last twelve months for which a BlogPost 
    created on that month exists, in reverse chronological order.
    """
    date_ = timezone.datetime.now()
    blogged_months = []
    months_chosen = 0
    months_queried = 0
    while months_chosen < 12 and months_queried < 24:
        if BlogPost.objects.filter(pub_date__year=date_.year,
                                   pub_date__month=date_.month):
            blogged_months.append( (date_.year, date_.month,
                                    date_.strftime("%B")) )
            months_chosen += 1
        date_ = date_.replace(day=1) - timedelta(days=1)
        months_queried += 1
    return blogged_months

def fetch_comments(request, year, month, day, title):
    """Fetches comments HTML for a given blog post and a given level of comments.

    Parameters:
        request - HTTPRequest django object
        year - Year of the BlogPost for which we are fetching comments
        month - Month of the BlogPost for which we are fetching comments
        day - Day of the BlogPost for which we are fetching comments
        title - Title of the BlogPost for which we are fetching comments

    Returns:
        HttpResponse object containing HTML for a number of comments to a BlogPost OR
        containing an HTTP 404 error
    """
    maxNesting = 10  # Maximum permitted comment nesting

    title = urlunquote(title)
    try:
        post = BlogPost.objects.get(
            pub_date__year=year, 
            pub_date__month=month,
            pub_date__day=day,
            post_title=title)
    except KeyError:
        raise Http404

    # Rendering logic for comment nesting due to responses
    def add_comment(comment, commentsList, startNesting, endNestings, 
            numberComments, maxComments):
        """If numberComments < maxComments, adds a comment to commentsList, 
        along with whether a new level of nesting should be started 
        and how many levels of nesting should be ended on that comment.
        Also returns True.

        Else, if numberComments >= maxComments, returns False and does
        not add comment to commentsList
        """
        if numberComments < maxComments:
            commentsList.append({
                'start_blockquote'  : startNesting,
                'end_blockquote'    : range(0, endNestings),
                'post'              : comment,
                })
            return True
        else:
            return False

    def add_children(commentsList, comment, extra_ends,
            numberComments, maxComments):
        """If there is space in the commentsList, determined by
        whether numberComments < maxComments, adds the replies to
        comment to the commentsList, ensuring that extra_ends 
        levels of comment reply nesting end after the chain of 
        comment responses is added to commentsList

        Preconditions:
        It is assumed that comment has children [responses to it]
        It is assumed that commentsList is nonempty

        Returns: 
        False if add_children ran out of space before running out of comments
        The number of children added if add_children ran out of comments before space
        """
        
        # Assert the required preconditions
        assert comment.blogcomment_set.exists() , "Blog Comment, id: %r, has no children" % comment.id
        #assert len(commentsList) > 0 , "commentsList is empty"
        
            
        responses = comment.blogcomment_set.order_by('-pub_date')
        if len(responses) == 1:
            comm = responses[0]
            if comm.blogcomment_set.exists():
                if add_comment(comm, commentsList, True, 0, numberComments, maxComments):
                    numberComments += 1
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0,extra_ends))
                    return False
                return add_children(commentsList, responses[0], (extra_ends + 1),
                        numberComments, maxComments) 
            else:
                #response has no subresponses
                if add_comment(comm, commentsList, True, extra_ends + 1,
                        numberComments, maxComments):
                    numberComments += 1
                    return numberComments
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0, extra_ends))
                    return False
        else:
            # There is more than one response
            for comm in responses[1:-1]:         
                if add_comment(comm, commentsList, False, 0, numberComments, maxComments):
                    numberComments += 1
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0, extra_ends))
                    return False
                if comm.blogcomment_set.exists():
                    if not add_children(commentsList, comm, 0, 
                            numberComments, maxComments):
                        return False
                        
            comm = responses[0]
            if comm.blogcomment_set.exists():
                if add_comment(comm, commentsList, True, 0, numberComments, maxComments):
                    numberComments += 1
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0, extra_ends))
                    return False
                if not add_children(commentsList, comm, 0, numberComments, maxComments):
                    return False
            else:
                if add_comment(comm, commentsList, True, 0, numberComments, maxComments):
                    numberComments += 1
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0, extra_ends))
                    return False

            comm = responses[-1]
            if comm.blogcomment_set.exists():
                if add_comment(comm, commentsList, False, 0, numberComments, maxComments):
                    numberComments += 1
                else:
                    commentsList[-1]['end_blockquote'].extend(range(0, extra_ends))
                if not add_children(commentsList, comm, extra_ends + 1):
                    return False
            else:
                if add_comment(comm, commentsList, False, extra_ends + 1,
                    numberComments, maxComments):
                    numberComments += 1
                else:
                    return False
        assert not "We've made it to the default return, the function should have returned within one of the if/else statements"
        return true


    commentsList = []
    numberComments = 0
    moreStuff = False
    renderedHTML = ""
    #If comments_level is the first level of comments [first ten comments]
    if request.GET['comments_level'] == '0':
        # Order comments that aren't replies to other comments by date.
        comments = BlogComment.objects.filter(parent_blog_post=post,
            response_to__isnull=True).order_by('-pub_date')
        for comment in comments:
            if add_comment(comment, commentsList, False, 0, numberComments, 10):
                numberComments += 1
            else:
                moreStuff = True
                break
            if comment.blogcomment_set.exists():
                kids = add_children(commentsList, comment, 0, numberComments, 10)
                if kids:
                    numberComments += kids
                else:
                    moreStuff = True
                    break

        context = { 'comment_list'      : commentsList,
                    'original_BlogPost' : post  }
        renderedHTML = render_to_string('blog/comments_section.html', RequestContext(request, context))
    else:
        # Insert code for following comments_level s past 0 here
        def older_siblings(comment):
            if comment.response_to:     #It has a post comment as a father
                return comment.response_to.blogcomment_set.filter(id__lt = comment.id).order_by('-pub_date')
            else:    # Its siblings are no n comment-response-posts
                return comment.parent_blog_post.blogcomment_set.filter(id__lt = comment.id,
                    response_to__isnull=True).order_by('-pub_date')
    
        def nesting_level(comment):
            i = 0
            currentComment = comment
            while ( i < maxNesting and currentComment.response_to ):
                currentComment = currentComment.response_to
                i += 1
            return i
        cLevel = 0
        try:
            cLevel = int(request.GET['comments_level'])
        except (TypeError, ValueError):
            raise Http404
        if cLevel < 0:
            raise Http404
			
        lastPost = 0
        try:
            lastPost = int(request.GET['last_post'])
        except KeyError:
            raise Http404
        except (TypeError, ValueError):
            raise Http404
        try:
            lastPost = BlogComment.objects.get(pk=lastPost)
        except BlogComment.DoesNotExist:
            raise Http404
        if BlogComment.objects.filter(response_to=lastPost):
            kids = add_children(commentsList, lastPost, 0, numberComments, 10)
            if kids:
                numberComments += kids
            else:
                moreStuff = True   
        lastPost_ = lastPost #quick fix
        for i in range(0,10):
            if lastPost:
                olderSiblings = older_siblings(lastPost)
                for sibling in olderSiblings:
                    if add_comment(sibling, commentsList, False, 0, numberComments, 10):
                        numberComments += 1
                    else:
                        moreStuff = True
                        break
                    if BlogComment.objects.filter(response_to=sibling):
                        kids = add_children(commentsList, sibling, 0, numberComments, 10)
                        if kids:
                            numberComments += kids
                        else:
                            moreStuff = True
                            break
                commentsList[-1]['end_blockquote'].append(1)
                lastPost = lastPost.response_to
            else:
                break

        context = { 'comment_list'          : commentsList ,
                    'original_BlogPost'     : post,
                    'starting_blockquotes'  : range(0,nesting_level(lastPost_)),
                    }
        renderedHTML = render_to_string('blog/continued_comments.html', RequestContext(request, context))
   
    # Finally, we can return a response...
    data = { 'comments_html' : renderedHTML , 'more_comments' : moreStuff }
    return HttpResponse(json.dumps(data), content_type = 'application/json')

def submit_comment(request, year, month, day, title):
    """Given a post request, stores the comment contained within"""
    title = urlunquote(title)
    post = get_object_or_404(
        BlogPost,
        pub_date__year=year, 
        pub_date__month=month,
        pub_date__day=day,
        post_title=title
        )
    commentBody = request.POST['commentText']
    try:
        author = Author.objects.get(pk=request.POST['emailInput'])
    except (KeyError, Author.DoesNotExist):
        author = Author(name=request.POST['nameInput'],
                        email=request.POST['emailInput'])
        author.save();
        
    parentPost = None
    try:
        parentPost = BlogComment.objects.get(pk=request.POST['ResponseTo'])
    except (KeyError, BlogComment.DoesNotExist, ValueError):
        pass
        
    comment = BlogComment(parent_blog_post=post,author=author,
        post_body=request.POST['commentText'], 
        post_title='',
        response_to=parentPost,
        )
    comment.save()
    context = { 'blog_posts' : [post],
                'blogged_months' : generate_archive_months(),
                'next_posts' : 6 
                }
    return render(request, 'blog/blog_index.html', context)

def index(request):
    """Show the five most recent BlogPosts"""
    posts = int(retrieve_query(request.GET,'posts', '5'))
    all_posts = BlogPost.objects.order_by('-pub_date')
    next_posts = 0 if len(all_posts) <= posts else posts + 5
    displayed_posts = all_posts[:posts]
    context = { 'blog_posts' : displayed_posts , 
                'blogged_months' : generate_archive_months(),
                'next_posts': next_posts,
                }
    return render(request, 'blog/blog_index.html', context)

def index_year(request, year):
    """Show all BlogPosts on the given year"""
    posts = int(retrieve_query(request.GET,'posts', '10'))
    yearly_posts = BlogPost.objects.filter(pub_date__year=year)
    displayed_posts = yearly_posts.order_by('-pub_date')[:posts]
    next_posts = 0 if len(yearly_posts) <= len(displayed_posts) else posts + 5
    context = { 'blog_posts' : displayed_posts,
                'blogged_months': generate_archive_months(),
                'next_posts': next_posts
                }
    return render(request, 'blog/blog_index.html', context)

def index_month(request, year, month):
    """Show all BlogPosts on the given year, month"""
    posts = int(retrieve_query(request.GET,'posts', '5'))
    monthly_posts = BlogPost.objects.filter(pub_date__year=year,
        pub_date__month=month)
    displayed_posts = monthly_posts.order_by('-pub_date')[:posts]
    next_posts = 0 if len(monthly_posts) <= len(displayed_posts) else posts + 5
    context = { 'blog_posts' : displayed_posts,
                'blogged_months': generate_archive_months(),
                'next_posts' : next_posts 
                }
    return render(request, 'blog/blog_index.html', context)


def index_day(request, year, month, day):
    """Show all BlogPosts on the given year, day, month"""
    posts = int(retrieve_query(request.GET,'posts', '5'))
    daily_posts = BlogPost.objects.filter(pub_date__year=year,
        pub_date__month=month, pub_date__day=day)
    displayed_posts = daily_posts.order_by('-pub_date')[:posts]
    next_posts = 0 if len(daily_posts) <= len(displayed_posts) else posts + 5

    context = { 'blog_posts' : displayed_posts,
                'blogged_months': generate_archive_months(),
                'next_posts' : next_posts 
                }
    return render(request, 'blog/blog_index.html', context)

def post_page(request, year, month, day, title):
    """Parses requests for URLs of form /blog/<year>/<day>/<title>/ 
    
    Parameters:
        request - Django HTTPRequest object
        year - Year of the BlogPost for which we are parsing a request
        month - Month of the BlogPost for which we are parsing a request
        day - Day of the BlogPost for which we are parsing a request
        title - Title of the BlogPost for which we are parsing a request
    
    Returns:
        Django HTTPRequest object.

        If a POST request, call submit_comment().
        if a GET request and is from our ajax request (discernable by a 
        query string containing 'comments') then call fetch_comments().
        Otherwise, simply return a page containing the BlogPost matching the 
        given date and title parameters, or a 404 if it does not exist.

    """
    if request.method == 'POST':
        # Form submission goes here
        return submit_comment(request, year, month, day, title)
    elif request.method == 'GET':
        try:
            request.GET['comments_level']
            # Success indicates that we are fetching comments, not the article itself.
        except KeyError:
            # Want to load entire page for this BlogPost, not just the 
            # comments HTML for the AJAX call
            blog_post = get_object_or_404(BlogPost, pub_date__year=year
                ,pub_date__month=month, pub_date__day=day, post_title=title)
            context = { 'blog_posts' : [blog_post] ,
                        'blogged_months' : generate_archive_months(),
                        'next_posts' : 0 }
            return render(request, 'blog/blog_index.html', context)

        # Code to execute in case of AJAX call
        return fetch_comments(request, year, month, day, 
                    title)
    else:
        # Request method wasn't POST nor GET... what the heck, man!
        raise Http404

