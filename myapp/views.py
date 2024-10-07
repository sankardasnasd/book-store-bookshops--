import datetime

import razorpay
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import *
from django.contrib import messages



def public(request):
    a=Category.objects.all()
    b=Book.objects.all()[:6]
    paginator = Paginator(b, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    # Get the current page number from the URL

    return render(request,'publicindex.html',{'data':a,'data1':b,'page_obj': page_obj})

def public1(request):
    a=Category.objects.all()
    b=Book.objects.all()
    return render(request,'publicindex.html',{'data':a,'data1':b})

def viewmorebook(request,id):
    a=Category.objects.get(id=id)
    b=Book.objects.get(id=id)
    return render(request,'view more book.html',{'data':a,'i':b})

def public_post(request):
    aa=request.POST['a']
    a=Category.objects.all()
    b=Book.objects.filter(title__icontains=aa)
    return render(request,'publicindex.html',{'data':a,'data1':b})


# def login(request):
#     if 'submit' in request.POST:
#         username = request.POST['username']
#         password = request.POST['password']
#
#         a=Login.objects.filter(username=username,password=password)
#         if a.exists():
#             b = Login.objects.get(username=username, password=password)
#             request.session['lid']=b.id
#             if b.type=='admin':
#                 return HttpResponse('''<script>window.location='/adminhome'</script>''')
#             elif b.type == 'user':
#
#                 return HttpResponse('''<script>window.location='/user_home'</script>''')
#             else:
#                 return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')
#         else:
#             return HttpResponse('''<script>alert("Invalid ");window.location='/'</script>''')
#     return  render(request,'login.html')


def login(request):
    if request.method == 'POST':  # Only process if form is submitted
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username and password match
        user = Login.objects.filter(username=username, password=password).first()

        if user:
            request.session['lid'] = user.id

            # Redirect based on user type
            if user.type == 'admin':
                return HttpResponse('''<script>window.location='/adminhome'</script>''')
            elif user.type == 'user':
                return HttpResponse('''<script>window.location='/user_home'</script>''')
        else:
            # If invalid login, pass error message to the template
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')



from django.utils.dateformat import format

def admin_home(request):


    a=Book.objects.all()
    book=a.count()
    request.session['book'] = book

    u=User.objects.all()
    user=u.count()
    request.session['user']=user

    c=Category.objects.all()
    cat=c.count()
    request.session['cat']=cat



    com=Complaints.objects.filter(reply='pending')
    complaint=com.count()
    request.session['complaint']=complaint

    book_data = (
        Book.objects.values('adddate')
            .annotate(count=Count('id'))
            .order_by('adddate')
    )

    labels = [str(item['adddate']) for item in book_data]  # Convert to string
    data = [item['count'] for item in book_data]

    request.session['lab'] = labels
    request.session['data'] = data

    user_data = (
        User.objects.values('registerationdate')  # Assuming 'registration_date' is the field for user registration
            .annotate(count=Count('id'))
            .order_by('registerationdate')
    )
    user_labels = [str(item['registerationdate']) for item in user_data]  # Convert to string
    user_data_values = [item['count'] for item in user_data]
    request.session['user_lab'] = user_labels
    request.session['user_data'] = user_data_values

    return render(request,'admin/adminhome.html',{'data':a,'complaint':complaint,'book':book,'user':user,'cat':cat})




# def admin_add_category(request):
#     if 'submit' in request.POST:
#         category=request.POST['category']
#         var=Category()
#         var.category=category
#         var.save()
#         return HttpResponse('''<script>alert("Category Added Successfully");window.location='/admin_add_category';</script>''')
#     return render(request,'admin/add category.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category  # Adjust this import based on your project structure

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category  # Adjust this import based on your project structure


def admin_add_category(request):
    if 'submit' in request.POST:
        category = request.POST['category']

        # Check if the category already exists
        if Category.objects.filter(category=category).exists():
            messages.error(request, "Category already exists!")
            return redirect('/admin_add_category')  # Redirect to the same page

        # If it doesn't exist, create the new category
        var = Category()
        var.category = category
        var.save()
        messages.success(request, "Category Added Successfully!")
        return redirect('/admin_add_category')  # Redirect to the same page

    return render(request, 'admin/add category.html')


def admin_add_books(request):
    c=Category.objects.all()
    if 'submit' in request.POST:
        CATEGORY=request.POST['category']
        title=request.POST['title']
        price=request.POST['price']
        quantity=request.POST['quantity']
        isbn=request.POST['isbn']
        author=request.POST['author']
        publish_year=request.POST['publish_year']
        language=request.POST['language']
        publisher=request.POST['publisher']
        description=request.POST['description']
        image=request.FILES['image']

        fs = FileSystemStorage()
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        fs.save(date, image)
        path = fs.url(date)

        b=Book()
        b.CATEGORY=Category.objects.get(id=CATEGORY)
        b.image=path
        b.title=title
        b.isbn=isbn
        b.price=float(price)
        b.quantity=quantity
        b.adddate=datetime.datetime.now().date().today().year
        b.author=author
        b.publish_year=publish_year
        b.language=language
        b.publisher=publisher
        b.description=description


        b.save()
        return HttpResponse('''<script>alert("Book Added Successfully");window.location='/admin_add_books';</script>''')
    return render(request,'admin/add  books.html',{'data':c,"d":datetime.datetime.now().strftime("%Y-%m-%d")})



def admin_view_books(request):
    a=Book.objects.all()
    return render(request,'admin/admin_view_books.html',{'data':a})



def admin_view_user(request):
    a=User.objects.all()
    return render(request,'admin/view_users.html',{'data':a})


def blockuser(request,id):
    ob=Login.objects.get(id=id)
    ob.type='block'
    ob.save()
    return redirect('/admin_view_user')


def unblockuser(request,id):
    ob = Login.objects.get(id=id)
    ob.type = 'user'
    ob.save()

    return redirect('/admin_view_user')


def admin_edit_books(request,id):
    a=Book.objects.get(id=id)
    a1=Category.objects.all()

    return render(request,'admin/edit  books.html',{'data':a,'data1':a1})

def admin_edit_books_post(request):
    CATEGORY = request.POST['category']
    title = request.POST['title']
    price = request.POST['price']
    quantity = request.POST['quantity']
    isbn = request.POST['isbn']
    author = request.POST['author']
    publish_year = request.POST['publish_year']
    language = request.POST['language']
    publisher = request.POST['publisher']
    description = request.POST['description']
    id = request.POST['id']

    b = Book.objects.get(id=id)
    if 'image' in request.FILES:
        image = request.FILES['image']

        fs = FileSystemStorage()
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        path=fs.save(date, image)
        # path = fs.url(date)
        b.image = path

    b.CATEGORY = Category.objects.get(id=CATEGORY)
    b.title = title
    b.price = float(price)
    b.quantity = quantity
    b.isbn = isbn
    b.author = author
    b.publish_year = publish_year
    b.language = language
    b.publisher = publisher
    b.description = description

    b.save()
    return HttpResponse('''<script>window.location='/admin_view_books'</script>''')


def admin_delete_book(request,id):
    var=Book.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>window.location='/admin_view_books'</script>''')


def userreg(request):
    if 'submit' in request.POST:
        fname = request.POST['fname']
        gender = request.POST['gender']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        default_image_path = "user1.jpg"  # Default image path

        # Check if the email already exists
        uu = User.objects.filter(email=email)
        if uu.exists():
            return redirect('/userreg')

        a = Login.objects.filter(username=email)
        if a.exists():
            return redirect('/userreg')
        if password == confirmpassword:
            l = Login()
            l.username = email
            l.password = confirmpassword
            l.type = 'user'
            l.save()

            u = User()
            if 'image' in request.FILES and request.FILES['image']:
                image = request.FILES['image']
                fs = FileSystemStorage()
                date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
                fs.save(date, image)
                path = fs.url(date)
                u.image = path
            else:
                u.image = '/media/user1.jpg'  # Use default image if none is uploaded

            u.LOGIN = l
            u.fname = fname
            u.lname = lastname
            u.gender = gender
            u.email = email
            u.phonenumber = phone
            u.registerationdate = datetime.datetime.now().date().today().year
            u.save()

            # Add a success message and redirect to the login page
            messages.success(request, 'You have successfully registered! Please log in.')
            return HttpResponse('''<script>window.location='/login'</script>''')
        else:
            return HttpResponse('''<script>alert("Passwords do not match");window.location='/userreg'</script>''')

    return render(request, 'registerindex.html')


def terms(request):
    return render(request, 'term.html')

def user_home(request):
    a=Book.objects.all()
    b=Category.objects.all()

    # c = Category.objects.all()
    # cat = c.count()
    # request.session['cat'] = cat


    c=Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
    cc=c.count()
    request.session['bid']=cc
    return render(request,'user/userindex.html',{'data':a,'data1':b,'data2':cc})


# def search_books(request):
#     name=request.POST['a']
#     cat=request.POST['cat']
#     a = Book.objects.filter(title__icontains=name)
#     b = Category.objects.filter(category__icontains=cat)
#
#     # c = Category.objects.all()
#     # cat = c.count()
#     # request.session['cat'] = cat
#
#
#     c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
#     cc = c.count()
#     request.session['bid'] = cc
#     return render(request,'user/userindex.html',{'data':a,'data1':b,'data2':cc})



# def search_books(request):
#     # Get search inputs from the form
#     name = request.POST.get('a', '')  # Search term
#     cat = request.POST.get('cat', '')  # Selected category ID
#
#     # Filter books based on title and category if both are provided
#     books = Book.objects.all()
#
#     # If a name is provided, filter books based on the title
#     if name:
#         books = books.filter(title__icontains=name)
#
#     # If a category is provided, filter books by category
#     if cat:
#         books = books.filter(category_id=cat)
#
#     # Fetch all categories for the dropdown
#     categories = Category.objects.all()
#
#     # Get count of orders for the current user
#     bill_details = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
#     bill_count = bill_details.count()
#
#     # Store the count in the session
#     request.session['bid'] = bill_count
#
#     # Render the user index with filtered books and categories
#     return render(request, 'user/userindex.html', {
#         'data': books,
#         'data1': categories,  # All categories for the dropdown
#         'data2': bill_count,  # Count of user orders
#     })





# def search_books(request):
#     # Get search inputs from the form
#     name = request.POST.get('a', '')  # Search by title
#     cat = request.POST.get('cat', '')  # Search by category
#     author = request.POST.get('author', '')  # Search by author
#     published_year = request.POST.get('published_year', '')  # Search by published year
#     price_min = request.POST.get('price_min', None)  # Search by minimum price
#     price_max = request.POST.get('price_max', None)  # Search by maximum price
#
#     # Start with all books
#     books = Book.objects.all()
#
#     # Filter by title if provided
#     if name:
#         books = books.filter(title__icontains=name)
#
#     # Filter by category if provided
#     if cat:
#         books = books.filter(category_id=cat)
#
#     # Filter by author if provided
#     if author:
#         books = books.filter(author__icontains=author)
#
#     # Filter by published year if provided
#     if published_year:
#         books = books.filter(published_year=published_year)
#
#     # Filter by price range if both min and max are provided
#     if price_min :
#         books = books.filter(price__icontains=price_min)
#
#
#
#     # Fetch all categories for the dropdown
#     categories = Category.objects.all()
#
#     # Get count of orders for the current user
#     bill_details = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
#     bill_count = bill_details.count()
#
#     # Store the count in the session
#     request.session['bid'] = bill_count
#
#     # Render the user index with filtered books and categories
#     return render(request, 'user/userindex.html', {
#         'data': books,      # Filtered books based on search criteria
#         'data1': categories,  # All categories for the dropdown
#         'data2': bill_count,  # Count of user orders
#     })




# 6-10-24
# def search_books(request):
#     # Get search inputs from the form
#     name = request.POST.get('a', '')  # Search by title
#     cat = request.POST.get('cat', '')  # Search by category
#     author = request.POST.get('author', '')  # Search by author
#     published_year = request.POST.get('published_year', '')  # Search by published year
#     price_min = request.POST.get('a')  # Search by minimum price
#
#     # Start with all books
#     books = Book.objects.filter(title__icontains=name)
#
#
#     aa=Book.objects.filter(price__icontains=price_min)
#
#
#
#     if cat:
#         books = books.filter(category_id=cat)
#
#
#
#     categories = Category.objects.all()
#
#     # Get count of orders for the current user
#     bill_details = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
#     bill_count = bill_details.count()
#
#     # Store the count in the session
#     request.session['bid'] = bill_count
#
#     # Render the user index with filtered books and categories
#     return render(request, 'user/userindex.html', {
#         'data': books,      # Filtered books based on search criteria
#         'data1': categories,  # All categories for the dropdown
#         'data2': bill_count,  # Count of user orders
#     })





from django.db.models import Q  # Import Q for OR functionality

from django.db.models import Q

# def search_books(request):
#     cat = request.POST.get('cat', '')  # Search by category
#
#     # Get the search term from a single input field (for example, 'query')
#     query_string = request.POST.get('a', '')  # Single search input field
#
#     # Start with all books
#     books = Book.objects.all()
#
#
#     # If the query_string is provided, search across multiple fields
#     if query_string:
#         books = books.filter(
#             Q(title__icontains=query_string) |            # Search by title
#             Q(author__icontains=query_string) |           # Search by author
#             Q(publish_year__year__icontains=query_string) |  # Search by published year
#             Q(price__icontains=query_string) |            # Search by price
#             Q(CATEGORY__category__icontains=query_string)   # Search by category name
#         )
#
#     if cat:
#         books = books.filter(CATEGORY_id=cat)
#
#     # Get all categories for the dropdown
#     categories = Category.objects.all()
#
#
#
#     # Get count of orders for the current user
#     bill_details = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
#     bill_count = bill_details.count()
#
#     # Store the count in the session
#     request.session['bid'] = bill_count
#
#     # Render the user index with filtered books and categories
#     return render(request, 'user/userindex.html', {
#         'data': books,      # Filtered books based on search criteria
#         'data1': categories,  # All categories for the dropdown
#         'data2': bill_count,  # Count of user orders
#     })



from django.db.models import Q

def search_books(request):
    # Get search inputs from the form
    cat = request.POST.get('cat', '')  # Search by category
    query_string = request.POST.get('a', '')  # Single search input field

    # Start with all books
    books = Book.objects.all()

    # If the query_string is provided, search across multiple fields
    if query_string:
        books = books.filter(
            Q(title__icontains=query_string) |            # Search by title
            Q(author__icontains=query_string) |           # Search by author
            Q(publish_year__year__icontains=query_string) |  # Search by published year
            Q(price__icontains=query_string)               # Search by price
        )

    # Apply the category filter if a category is selected
    if cat and cat != "----SEARCH----":
        books = books.filter(CATEGORY_id=cat)

    # Get all categories for the dropdown
    categories = Category.objects.all()

    # Get count of orders for the current user
    bill_details = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
    bill_count = bill_details.count()

    # Store the count in the session
    request.session['bid'] = bill_count

    # Render the user index with filtered books and categories
    return render(request, 'user/userindex.html', {
        'data': books,      # Filtered books based on search criteria
        'data1': categories,  # All categories for the dropdown
        'data2': bill_count,  # Count of user orders
    })


def user_view_profile(request):
    a=User.objects.get(LOGIN_id=request.session['lid'])
    c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'], ORDER__status='cart')
    cc = c.count()
    request.session['cid'] = cc
    return render(request,'user/pro.html',{'i':a,'cid':cc})


def user_edit_profile(request):
    a=User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'user/edit profile.html',{'i':a})

def user_edit_profile_post(request):
    try:
        fname = request.POST['textfield']
        gender = request.POST['gender']
        lastname = request.POST['lname']
        email = request.POST['textfield3']
        phone = request.POST['textfield2']
        image = request.FILES['file']
        fs = FileSystemStorage()
        path = fs.save(image.name, image)
        u=User.objects.get(LOGIN_id=request.session['lid'])
        u.image = path
        u.fname = fname
        u.lname = lastname
        u.gender = gender
        u.email = email
        u.phonenumber = phone
        u.save()
        # return redirect('/user_view_profile')

        return HttpResponse('''
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                    <script>
                        document.addEventListener("DOMContentLoaded", function() {
                            Swal.fire({
                                icon: 'success',
                                title: 'Successfully Updated!',
                                confirmButtonText: 'OK',
                                reverseButtons: true
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = '/user_view_profile';
                                }
                            });
                        });
                    </script>
                ''')
    except:
        fname = request.POST['textfield']
        gender = request.POST['gender']
        lastname = request.POST['lname']
        email = request.POST['textfield3']
        phone = request.POST['textfield2']

        u = User.objects.get(LOGIN_id=request.session['lid'])

        u.fname = fname
        u.lname = lastname
        u.gender = gender
        u.email = email
        u.phonenumber = phone
        u.save()
        return HttpResponse('''
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                    <script>
                        document.addEventListener("DOMContentLoaded", function() {
                            Swal.fire({
                                icon: 'success',
                                title: 'Successfully Updated!',
                                confirmButtonText: 'OK',
                                reverseButtons: true
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = '/user_view_profile';
                                }
                            });
                        });
                    </script>
                ''')
        # return redirect('/user_view_profile')

def user_view_books(request,id):
    request.session['bid']=id
    a=Book.objects.filter(id=id)
    c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'],ORDER__status='cart')
    cc = c.count()
    request.session['cid'] = cc
    return render(request,'user/user_view_books.html',{'data':a,'cid':cc})





def user_home2(request):
    c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'])
    cc = c.count()
    request.session['bid'] = cc
    return render(request,'user/userindex2.html',{'bid':cc})


def user_booking(request,id):

    request.session['bid']=id
    c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'],ORDER__status='cart')
    cc = c.count()
    request.session['cid'] = cc

    a=Book.objects.filter(id=id)
    return render(request,'user/booking1.html',{'data':a,'cid':cc})

#
def user_booking1(request):
    qty=request.POST['qty']
    request.session['qty']=qty
    id=request.session['bid']
    a=Book.objects.get(id=id)
    vv=a.price

    total=float(vv)*float(qty)
    request.session['amt']=total
    c = Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'], ORDER__status='cart')
    cc = c.count()
    request.session['cid'] = cc
    return render(request,'user/booking.html',{'data':a,'amt':total,'cid':cc})

def user_booking_post(request):
    id=request.POST['id']
    # title=request.POST['title']
    place=request.POST['place']
    landmark=request.POST['landmark']
    qty=float(request.session['qty'])
    pin=request.POST['pin']
    address=request.POST['address']

    cc=Book.objects.get(id=id)
    aa=float(cc.price)
    pp=float(qty*aa)

    a=Order()
    a.BOOK=cc
    a.USER=User.objects.get(LOGIN_id=request.session['lid'])

    a.price=pp
    a.place=place
    a.pin=pin
    a.qty=qty
    a.address=address
    a.landmark=landmark
    a.status='ordered'
    a.date=datetime.datetime.now().today().date()
    a.save()
    ob1=Bill_details()
    ob1.ORDER = a
    ob1.BOOK = cc
    ob1.quantity =qty
    ob1.save()
    return redirect('/user_home')


def admin_view_booking(request):
    # a=Bill_details.objects.all()

    a=Order.objects.filter(status='ordered')
    return render(request,'admin/view bookings.html',{'bookings':a})


def admin_view_booking1(request,id):
    request.session['oid']=id
    # a=Bill_details.objects.all()

    a=Bill_details.objects.filter(ORDER__id=id)
    return render(request,'admin/view bookings1.html',{'bookings':a})

#
# def purchase(request,id):
#     a=Order.objects.filter(status='cart',USER__LOGIN__id=request.session['lid'])
#     if len(a)==0:
#         a=Order()
#         a.USER = User.objects.get(LOGIN__id=request.session['lid'])
#         a.price = 0
#         a.qty = 0
#         a.date = datetime.datetime.today()
#         a.place = ''
#         a.pin = 0
#         a.landmark = ''
#         a.address = ''
#         a.status = 'cart'
#         a.save()
#     obb=Book.objects.get(id=id)
#     ob=Bill_details()
#     # ob.ORDER = Order.objects.get(id=a.id)
#     ob.ORDER = Order.objects.get(id=a.id)
#     ob.BOOK = obb
#     ob.quantity =1
#     ob.save()
#     a.price+=obb.price
#     a.save()
#
#
#     return redirect("/user_home")




def purchase(request, id):
    # Get the order for the current user where the status is 'cart'
    a = Order.objects.filter(status='cart', USER__LOGIN__id=request.session['lid']).first()

    # If no cart exists for the user, create a new one
    if not a:  # Check if 'a' is None
        a = Order()
        a.USER = User.objects.get(LOGIN__id=request.session['lid'])
        a.price = 0
        a.qty = 0
        a.date = datetime.datetime.today()
        a.place = ''
        a.pin = 0
        a.landmark = ''
        a.address = ''
        a.status = 'cart'
        a.save()

    # Fetch the book that the user wants to add to the cart
    obb = Book.objects.get(id=id)

    # Create a new Bill_details entry with the book and order details
    ob = Bill_details()
    ob.ORDER = a  # Now 'a' is the correct Order object
    ob.BOOK = obb
    ob.quantity = 1
    ob.save()

    # Update the total price of the order by adding the book's price
    a.price += obb.price
    a.save()

    return redirect("/user_home")


def view_cart(request):


    a=Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'],ORDER__status='cart')
    cc=a.count()
    request.session['cid']=cc
    return render(request,'user/view cart.html',{'data':a,'cid':cc})


def remove_cart(request,id):
    a=Bill_details.objects.get(id=id)
    a.delete()
    return redirect("/view_cart")




def user_pay_proceed(request,id,amt):
    request.session['rid'] = id


    request.session['pay_amount'] = str(amt).split(".")[0]
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': request.session['pay_amount']+"00", 'currency': "INR", 'payment_capture': '1'})
    res=User.objects.get(LOGIN__id=request.session['lid'])


    ob=Order.objects.get(id=request.session['rid'])
    ob.status='paid'
    ob.save()
    return render(request,'user/UserPayProceed.html',{'p':payment,'val':res,"lid":request.session['lid'],"id":request.session['rid']})


def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    # var = auth.authenticate(username='admin', password='admin')
    # if var is not None:
    #     auth.login(request, var)
    # amt = request.session['pay_amount']
    ob=Payment()
    ob.date=datetime.datetime.now().today().date()
    ob.time=datetime.datetime.now().today().time()
    ob.ORDER=Order.objects.get(id=request.session['rid'])
    ob.status='paid'
    ob.save()
    return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'success',
                            title: 'Order Confirmed... !',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/user_home';
                            }
                        });
                    });
                </script>
            ''')




    # return HttpResponse('''<script>alert("Success! Thank you for your Contribution");window.location="/userhome"</script>''')


def user_view_orders(request):

    a=Bill_details.objects.filter(ORDER__USER__LOGIN_id=request.session['lid'], ORDER__status='cart')
    cc = a.count()
    request.session['cid'] = cc
    return render(request,'user/view_oreders.html',{'data':a,'cid':cc})


def admin_view_payments(request):
    a=Bill_details.objects.all()
    return render(request,'admin/view bookings payment.html',{'data':a})