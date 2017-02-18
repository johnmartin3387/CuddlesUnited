
from django.shortcuts import render_to_response, redirect
from lostpet_auth.models import *
from lostpet_auth.image_utils import ImageText
from django.template import RequestContext
from django.contrib.auth.models import *

from functools import wraps

import datetime
from django.http import HttpResponse
from lostpet import settings
from lostpet_auth.util import *

import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from allauth.socialaccount.models import SocialAccount
import os
import stripe
import mailchimp

import random
import string
from PIL import *

# Login Required decorator
def login_required():
    def login_decorator(function):
        @wraps(function)
        def wrapped_function(request):

            # if a user is not authorized, redirect to login page
            if 'user' not in request.session or request.session['user'] is None:
                return redirect("/")
            # otherwise, go on the request
            else:
                return function(request)

        return wrapped_function

    return login_decorator


# login view
def login(request):
    error = 'none'
    request.session['user'] = None

    if 'username' in request.POST:

        # get username and password from request.
        username = request.POST['username']
        password = request.POST['password']

        # check whether the user is in database or not
        if username == settings.ADMIN_NAME and password == settings.ADMIN_PASSWORD:
            request.session['user'] = {
                # "id": user[0].id,
                "username": settings.ADMIN_NAME, #user[0].email,
                "password": settings.ADMIN_PASSWORD, #user[0].name.split(" ")[0],
                "role": "admin"
            }

            return redirect("/admin_main")

        user = Client.objects.filter(email=username, password=password)

        if len(user) > 0:
            request.session['user'] = {
                # "id": user[0].id,
                "username": user[0].name.split(" ")[0],
                "email": user[0].email,
                "password": user[0].password,
                "role": "client"
            }

            return redirect("/pricing")
        else:
            error = 'block'

    return render_to_response('login.html', {'error':error}, context_instance=RequestContext(request))


# logout view
#   initialize session variable
def logout(request):
    request.session['user'] = None
    return redirect("/")

@login_required()
def main(request):
    clients = Client.objects.all().order_by("-created_on")
    return render_to_response('blank.html', locals(), context_instance=RequestContext(request))

@login_required()
def admin_main(request):
    if request.session["user"]["role"] != "admin":
        return redirect("/")

    clients = Client.objects.all().order_by("-created_on")
    return render_to_response('main.html', locals(), context_instance=RequestContext(request))

@login_required()
def create(request):
    breeds = settings.BREED

    if request.POST:
        client = Client()
        client.name = request.POST["client_name"]
        client.email = request.POST["email"]
        client.password = request.POST["password"]
        client.pet_name = request.POST["pet_name"]
        client.type = request.POST["type"]
        client.size = request.POST["size"]
        client.breed = request.POST["breed"]
        client.color = request.POST["color"]
        client.sex = request.POST["sex"]
        client.state = request.POST["state"]
        client.zip_code = request.POST["zip_code"]
        client.date = "%s 00:00" % request.POST["date"]

        client.save()

        # subscribe in mailchimp
        merge_vars = {
              "FNAME": client.name,
              "PNAME": client.pet_name,
              "PTYPE": client.type,
              "GROUPINGS": [
                    {
                        "name": "Leads",
                        "groups":["Website Lead"]
                    }
                ]
        }
        api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        api.lists.subscribe(settings.MAILCHIMP_LIST_ID, {"email": client.email}, merge_vars)

        return redirect("/admin_main")

    return render_to_response('create.html', locals(), context_instance=RequestContext(request))

@login_required()
def remove(request):
    id = request.GET["id"]
    client = Client.objects.get(pk=id)

    #api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    #api.lists.unsubscribe(settings.MAILCHIMP_LIST_ID, {"email": client.email})

    client.delete()

    return redirect("/admin_main")

@login_required()
def remove_history(request):
    Pet.objects.all().delete()

    return redirect("/admin_main")
    

def signup(request):
    breeds = settings.BREED
    
    if request.POST:
        colors = request.POST.getlist("color")

        client = Client()
        client.name = "%s %s" % (request.POST["firstname"], request.POST["lastname"])
        client.email = request.POST["email"]
        client.phone = request.POST["phone"]
        client.password = request.POST["password"]
        client.pet_name = request.POST["petname"]
        client.type = request.POST["type"]
        client.size = request.POST["size"]
        client.breed = request.POST["breed"]
        client.mixed = request.POST["mixed"]

        client.color = colors[0]
        if len(colors) > 1:
            client.color_sec = colors[1]

        client.sex = request.POST["sex"]

        date = request.POST["date"].split("/")
        date = "%s-%s-%s 00:01" % (date[2], date[0], date[1])
        client.date = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M")
        
        client.city = request.POST["city"]
        client.state = request.POST["state"]
        client.zip_code = request.POST["zipcode"]
        client.microchip = int(request.POST["microchip"])
        client.collar = int(request.POST["collar"])
        client.description = request.POST["description"]   

        if "pet_image" in request.FILES:
            client.pet_image = save_file(request.FILES["pet_image"])

        client.save()

        # subscribe in mailchimp
        merge_vars = {
              "FNAME": request.POST["firstname"],
              "LNAME": request.POST["lastname"],
              "PNAME": client.pet_name,
              "PTYPE": client.type,
              "PIMAGE": client.pet_image,
              "CITY": client.state,
              "GROUPINGS": [
                    {
                        "name": "Leads",
                        "groups":["Website Lead"]
                    }
                ]
        }

        phone = ""
        if len(client.phone) > 6:
            phone = "%s %s %s" % (client.phone[:3], client.phone[3:6], client.phone[6:])

        sex = "Male"
        if client.sex == "girl":
            sex = "Female"

        # upload file into AWS S3
        with open("%s/email_template_profile.tpl" % settings.STATICFILES_DIRS[0], "rb") as fp:
            template = fp.read()
            alert_data = '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Client Name")
            alert_data += getTemplate(client.name)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Email")
            alert_data += getTemplate(client.email)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Phone Number")
            alert_data += getTemplate(phone)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Type")
            alert_data += getTemplate(client.type)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Sex")
            alert_data += getTemplate(sex)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Description")
            alert_data += getTemplate(client.description)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Size")
            alert_data += getTemplate(client.size)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Breed")
            alert_data += getTemplate(client.breed)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Age")
            alert_data += getTemplate(request.POST["age"])
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Pet Color")
            alert_data += getTemplate(client.color)
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("When were they last seen?")
            alert_data += getTemplate(request.POST["date"])
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Where were they last seen?")
            alert_data += getTemplate("%s, %s, %s" % (client.city, client.state, client.zip_code))
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Are they micro-chipped?")
            alert_data += getTemplate('Yes' if client.microchip==1 else "No")
            alert_data += '</tr>'

            alert_data += '<tr style="text-align: center;  padding-left:20px;">'
            alert_data += getTemplate("Are they possibly wearing a collar?")
            alert_data += getTemplate('Yes' if client.collar==1 else "No")
            alert_data += '</tr>'

            template = template.replace("<alert-statistics>", alert_data)

            send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                          settings.EMIAL_ADMIN, "%s signed up the site" % request.POST["firstname"], template)
        
        # api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        # api.lists.subscribe(settings.MAILCHIMP_LIST_ID, {"email": client.email, 'double_optin': False}, merge_vars)

        request.session['user'] = {
            # "id": user[0].id,
            "username": request.POST["firstname"],
            "email": client.email,
            "password": client.password,
            "role": "client"
        }
        return redirect("/pricing")

    return render_to_response('signup.html', locals(), context_instance=RequestContext(request))

def save_file(file, path='images', filename=""):
    temp = settings.BASE_DIR + settings.STATIC_URL + str(path)

    if not os.path.exists(temp):
        os.makedirs(temp)

    if filename == "":
        filename = file._get_name()
    
    fd = open('%s/%s' % (temp, str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

    return filename

# check email duplication
@csrf_exempt
def check_duplication(request):
    res = {"result": "false"}

    email = request.POST["email"]
    if len(Client.objects.filter(email=email)) > 0:
        res["result"] = "true"

    return HttpResponse(json.dumps(res)) 

@login_required()
def pricing(request):
    stripe_pk = settings.STRIPE_PUBLIC_KEY

    if "email" not in request.session['user']:
        return redirect("/main")

    client = Client.objects.filter(email=request.session['user']["email"])[0]
    price = Client.objects.filter(email=request.session['user']["email"])[0].pricing

    return render_to_response('pricing.html', locals(), context_instance=RequestContext(request))


def blog(request, blog_id):
    blog = Post.objects.filter(path_key=blog_id)
    if len(blog) == 0:
        return redirect("/login")

    blog = blog[0]
    phone = ""
    if len(blog.client.phone) > 6:
        phone = "%s-%s-%s" % (blog.client.phone[:3], blog.client.phone[3:6], blog.client.phone[6:])
    comments = Comment.objects.filter(post=blog)

    return render_to_response('blog.html', locals(), context_instance=RequestContext(request))

def comment(request):
    print request.GET

    blog = Post.objects.filter(path_key=request.GET["blog_id"])

    comment = Comment()
    comment.post = blog[0]
    comment.text = request.GET["comment"]
    comment.save()

    comments = Comment.objects.filter(post=blog[0])
    cmt = []
    for comment in comments:
        cmt.append({"date": comment.created_on.strftime("%b.%m, %Y, %I:%M %p"), "comment": comment.text})

    res = {"num": len(comments), "content": cmt}
    return HttpResponse(json.dumps(res)) 

def setup_pricing(request):
    return redirect("/accounts/stripe/login/?process=login&next=/setup_info?price=" + request.GET["price"])

def setup_info(request):
    '''tp_user = User.objects.filter(username=request.user)
    stripe_uid = SocialAccount.objects.filter(user=tp_user[0], provider="stripe")[0]	
    data = stripe_uid.extra_data
    
    client = Client.objects.filter(email=data['email'])

    if len(client) == 0:
        return redirect("/pricing")

    client = client[0]
    client.pricing = request.GET["price"]
    client.save()'''

    # subscribe a price in stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    charge = stripe.Charge.create(
        amount= int(request.GET["price"]) * 100,
        currency="usd",
        source=request.GET['token'],
        description='Sent the money!'
    )

    client = Client.objects.filter(email=request.session['user']["email"])[0]
    client.pricing = int(request.GET["price"])
    client.save()

    # create blog
    post = Post()
    post.client = client
    post.path_key = getRandomStr(15)
    post.save()

    # send eamil to client with flyer and blog url
    
    phone = ""
    if len(client.phone) > 6:
        phone = "%s %s %s" % (client.phone[:3], client.phone[3:6], client.phone[6:])

    sex = "Male"
    if client.sex == "girl":
        sex = "Female"

    colors = [client.color]
    if client.color_sec != None and client.color_sec != "":
        colors.append(client.color_sec)

    data = {"logo": "%s/images/logo.jpg" % settings.STATICFILES_DIRS[0], "pet_type": client.type, \
              "city": client.city, "state": client.state, \
              "zip_code": client.zip_code, "pet_image": "%s/images/%s" % (settings.STATICFILES_DIRS[0], client.pet_image), \
              "pet_name": client.pet_name, \
              "breed": client.breed, "date": client.date.strftime("%m/%d/%Y"), \
              "sex": sex, "color": colors, "phone": phone}
        
    # create pdf
    createPDF(data)

    # upload file into AWS S3
    with open("form_letter.pdf") as fp:
        res = upload_to_s3(settings.AWS_ACESS_KEY, settings.AWS_SECRET_KEY, fp, settings.BUCKET, settings.DIRECTORY, "%s-flyer.pdf" % phone.replace(" ", "-"))

    blog_url = "http://%s/blog/%s" % (request.META['HTTP_HOST'], post.path_key)


    image_file = str("%simages/%s" % (settings.BASE_DIR + settings.STATIC_URL, client.pet_image))
    bg_image = Image.new('RGB', (714, 374), (85, 113, 127))
    pet_image = Image.open(image_file)

    # resize image with ratio
    ratio = 340.0 / pet_image.size[1]
    width = int(pet_image.size[0] * ratio)
    pet_image = pet_image.resize((width, 340), Image.ANTIALIAS)
    bg_image.paste(pet_image, ((bg_image.size[0] - pet_image.size[0])/2, 34))
    bg_image.save(image_file)

    img = ImageText(image_file, background=(255, 0, 0, 255))
    img.write_text_box((0, 0), "MISSING PET ALERT - %s, %s" % (client.city.upper(), client.state.split("-")[0].strip()), box_width=img.getWidth(), font_filename=str("%sIMPACT.TTF" % (settings.BASE_DIR + settings.STATIC_URL)), font_size=35, color=(250, 250, 250), place='center')
    img.save(image_file)

    data = {
               "client": "Help Us Find %s! | Cuddles United" % client.pet_name, "blog_url":blog_url, 
               "server_domain": request.META['HTTP_HOST'], "description": client.description, 
               "image_url": "http://%s/static/images/%s" % (request.META['HTTP_HOST'], client.pet_image), 
               "caption": "Missing Pet Alert - Help Us Find %s!" % (client.pet_name) 
           }

    api = get_api({"page_id": settings.FACEBOOK_PAGE_ID, "access_token": settings.FACEBOOK_ACCESS_TOKEN})
    post_id = postFacebook(api, data)
    post_id = post_id["id"].split("_")[1]

    if res:
        # email 1
        subject = "%s's Printable Flyer - Download your copy" % client.pet_name
        body = "<p>Hi <b>%s</b>,</p><p>Have no fear, Cuddles United is here! We're here to do everything we can to help reunite you with %s. Below you'll find a link to %s's downloadable and printable missing pet flyer. If you haven't done so already we highly suggest spreading flyers around your neighbourhood. It's important your neighbors are aware of %s's disappearance</p>" % (client.name.split(" ")[0], client.pet_name, client.pet_name, client.pet_name)
        body += "<p><a href='%s'>%s</a></p>" % (res, res)
        body += "<p>We will email with general updates regarding your alert and let you know immediately if we find any leads. Please don't hesitate to ask if you have any questions. </p><p>Thanks,<br/>The Cuddles United Team</p>"
        send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                           client.email, subject, body.encode("utf8"))

        # email 2
        subject = "%s's Facebook Post - Your alert is live" % client.pet_name
        body = "<p>Hi <b>%s</b>,</p> <p>%s's missing pet alert is now live on Facebook. We expect within 2-12 hours thousands of people will have seen %s's lost pet alert. We suggest that you and those close to you with Facebook accounts share the following link for maximum post engagement.</p>" % (client.name.split(" ")[0], client.pet_name, client.pet_name)
        body += "<p>Facebook Post: <a href='https://www.facebook.com/cuddlesunited/posts/%s'>https://www.facebook.com/cuddlesunited/posts/%s</a></p> <p>You can also use the link below to share %s's customized missing pet alert on Facebook. To do so simply copy and paste the link below to your personal Facebook profile or any local Facebook page or group. The link will generate a banner that looks similar to your Cuddles United alert.</p> <p><a href='%s'>%s</a></p> <p>We will email you again with general updates regarding your alert and let you know immediately if we find any leads.</p> <p>Thanks,<br/>The Cuddles United Team</p>" % (post_id, post_id, client.pet_name, blog_url, blog_url)
        send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                           client.email, subject, body.encode("utf8"))
        # email 3
        subject = "%s - Status Update" % client.pet_name
        body = "<p>Your missing pet flyer has now been sent to every nearby contact in our network. These contacts include local businesses, non-profits, shelters and volunteers with whom we have direct personal relationships with. Everyone in our network genuinely cares about the well being of missing pets. We've also contacted a number of other local businesses who we are not partnered with, in hopes that they too will share the word of your pets disappearance.</p><p>Your flyer has also been posted to every online pet related website in our database. We're now goint to start posting to all local/active Facebook groups and local email listeners. To prevent your email account from being spammed with unwanted emails from all of the online boards we post to, we use one of our own email accounts to filter any unwanted emails and forward only the ones that pertain to your search.</p><p>Our team is in the process of personally contacting your neighbors via phone call. This is a non-automated service, so we will be on the phone giving a brief description of your pet and how to contact us if they have any information. Phone laws prohibit us from making community notification calls after 8PM CT.</p><p>We also have custom software programs running that are monitoring shelters and animal control services for any and all descriptions that potentially resemble your pet. In addition, our team is manually contacting local shelters and pounds and will contact you immediately if there's a match.</p><p>We will email with general updates regarding your alert and let you know immediately if we find any leads. Please don't hesitate to ask if you have any questions. </p><p>Thanks,<br/>The Cuddles United Team</p>"
        send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                           client.email, subject, body.encode("utf8"))

    # subscribe in mailchimp
    merge_vars = {
          "FNAME": client.name,
          "PNAME": client.pet_name,
          "PTYPE": client.type,
    }

    if client.pricing == 29:
        merge_vars["GROUPINGS"] = [{
                    "name": "Paid",
                    "groups":["Basic"]
                }]
    elif client.pricing == 89:
        merge_vars["GROUPINGS"] = [{
                    "name": "Paid",
                    "groups":["Most Popular"]
                }]
    else:
        merge_vars["GROUPINGS"] = [{
                    "name": "Paid",
                    "groups":["Premier"]
                }]

    # api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    # api.lists.subscribe(settings.MAILCHIMP_LIST_ID, {"email": client.email}, merge_vars, update_existing=True)

    os.remove("form_letter.pdf")
    
    return render_to_response('progress.html', locals(), context_instance=RequestContext(request))

def getRandomStr(length):
    s=string.lowercase+string.digits
    return ''.join(random.sample(s,length))


