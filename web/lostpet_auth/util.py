import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

import os

import boto
from boto.s3.key import Key

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import facebook

import PIL

def createPDF(data):
    doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=32,leftMargin=32,
                        topMargin=22,bottomMargin=18)
    Story=[]

    #data = {"logo": "/home/wolf/logo.jpg", "pet_type": "dog", "city": "Vancouver", "state": "British Columbia", \
    #          "zip_code": "bc 12343", "pet_image": "/home/wolf/lost_dog.jpg", "pet_name": "Sweety", \
    #          "breed": "American Bulldog", "date": "12/03/2016", "sex": "Female", "color": "White", "phone": "773 777 8888"}

    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
 
    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
 
    # display logo
    im = Image(data["logo"], 8*inch, 0.6*inch)
    Story.append(im)
    Story.append(Spacer(1, 8))

    # define stylesheed
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))

    # pet type
    ptext = '<font size=84 color="red"><b>LOST %s</b></font>' % data["pet_type"].upper()
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 92))
 
    # address
    ptext = '<font size=24><b>%s, %s, %s</b></font>' % (data["city"], data["state"], data["zip_code"])
    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 45))

    # pet image
    tp_im = PIL.Image.open(data["pet_image"])
    width, height = tp_im.size
    
    if width > height:
        height = float(height) / width * 4 * inch
        width = 4 * inch 
    else:
        width = float(width) / height * 4 * inch
        height = 4 * inch

    im = Image(data["pet_image"], width, height)
    Story.append(im)
    Story.append(Spacer(1, 12))

    # pet name
    ptext = '<font size=46 color="red"><b>%s</b></font>' % (data["pet_name"].upper())
    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 52)) 

    # breed
    ptext = '<font size=24><b>%s</b></font>' % data["breed"]
    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 22))

    # date
    ptext = '<font size=24>Missing Since: %s</font>' % data["date"]
    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 18))

    # sex
    ptext = '<font size=24>%s</font>' % data["sex"]
    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 18))

    # color
    ptext = '<font size=24>%s</font>' % data["color"][0]
    if len(data["color"]) > 1:
        ptext = '<font size=24>%s / %s</font>' % (data["color"][0], data["color"][1])

    Story.append(Paragraph(ptext, styles["Justify"]))  
    Story.append(Spacer(1, 22))

    # breed
    ptext = '<font size=24><b>Call If Seen: %s</b></font>' % data["phone"]
    Story.append(Paragraph(ptext, styles["Justify"]))  

    doc.build(Story)

def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket_name, directory, key, callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket_name, validate=True)
    k = Key(bucket)
    k.key = "%s/%s" % (directory, key)
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        url = "https://s3-us-west-2.amazonaws.com/%s/%s/%s" % (bucket_name, directory.replace(" ", "+"), key)
        return url

    return False

def send_email(user, pwd, sender, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = sender
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = MIMEText(body, 'html')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)

    msg.attach(TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print 'successfully sent the mail:\n'
        return True
    except:
        print "failed to send mail:\n"
        return False

def getTemplate(data):
    return """
        <td style="padding:10px;
    border-top: 1px solid #ffffff;
    border-bottom:1px solid #e0e0e0;
    border-left: 1px solid #e0e0e0;
    
    background: #fafafa;
    background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
    background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);">""" + data + """</td>"""


def postFacebook(api, data):
    attachment =  {
        'name': data["client"],
        'link': data["blog_url"],
        'caption': data["server_domain"],
        'description': data["description"],
        'picture': data["image_url"]
    }

    return api.put_wall_post(message=data["caption"], attachment=attachment)


def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph

