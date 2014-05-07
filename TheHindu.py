import urllib2
import xml.etree.ElementTree as xmltree;
import datetime;
from datetime import date, timedelta;
from HTMLParser import HTMLParser;
from bs4 import BeautifulSoup;
import codecs;
import smtplib;
from email.MIMEMultipart import MIMEMultipart;
from email.MIMEBase import MIMEBase;
from email import Encoders;


#Declare reusable variables
basedir = 'C:/TheHindu/'; #Forward slash intentionally used
newsFileName = String = 'TheHindu_' + str(datetime.datetime.today().day) + '_' + str(datetime.datetime.today().month) + '_' + str(datetime.datetime.today().year) + '.html';


def fetchRSSXML():
    response = urllib2.urlopen('http://www.thehindu.com/?service=rss');
    xml = response.read();

    #Write fetched content to file
    myfile = open(basedir+"NewsFeed.xml","w");
    myfile.write(xml);
    myfile.close();


def writeLinks():
    tree = xmltree.parse(basedir+"NewsFeed.xml");

    rss = tree.getroot();
    linksfile = open(basedir+"Links.txt","w");

    articleDate = '';
    criteriaDate = '';

    #Extract links based on date criteria
    for channel in rss:
        for item in channel:
            for node in item:
                if node.tag=='pubDate':
                    pubDate = node.text;
                    articleDate = datetime.datetime.strptime(pubDate,'%a, %d %b %Y %H:%M:%S +0530');
                    criteriaDate = datetime.datetime.now() - datetime.timedelta(days=1);

                if node.tag=='title':
                    if (articleDate > criteriaDate):
                        title = node.text;
                        linksfile.write(title.encode('ascii','ignore')+'\n');
                
                if node.tag=='link':
                    if (articleDate > criteriaDate):
                        link = node.text;
                        linksfile.write(link.encode('ascii','ignore')+'\n');
                        
    linksfile.close();


def createNewsHTML():
    newsfile = open(basedir+newsFileName,"w");
    newsfile.write("<html><body>");
    newsfile.close();


def buildTOC():
    newsfile = open(basedir+newsFileName,"a");
    newsfile.write("<mbp:pagebreak/>");
    newsfile.write("<a name='start'/>");
    newsfile.write("<a name='TOC'><h2>Table of Contents</h2></a>");

    linksfile = open(basedir+"Links.txt","r");
    i=0;

    for line in linksfile:
        i=i+1;
        if i%2==1:
            newsfile.write("<a href='#chap"+str((i+1)/2)+"'><h3>"+line+"</h3></a>");

    newsfile.close();

    
def publishNewsHTML():
    newsfile = open(basedir+newsFileName,"a");
    newsfile.write("</body></html>");
    newsfile.close();


def fetchHTML(url, i):
    newsfile = open(basedir+newsFileName,"a");
    
    response = urllib2.urlopen(url);
    html = response.read();

    #Parse HTML in BeautifulSoup
    htmldoc = BeautifulSoup(html);

    #Remove the annoying related articles column from the parsed HTML
    relCol = htmldoc.find('div', attrs={'class':'related-column'});
    del relCol;

    #Strip hyperlinks from the content
    for hdoc in htmldoc('a'):
        hdoc.extract()
    
    articleTitle = htmldoc.find('h1',attrs={'class':'detail-title'});
    try:
        newsfile.write('<mbp:pagebreak/>');
        print articleTitle.text.encode('ascii','ignore');
        newsfile.write('<p><a name="chap'+str(i/2)+'"><h1>'+articleTitle.text.encode('ascii','ignore')+'</h1></a></p>');
            
        pubDate = htmldoc.find('div', attrs={'class':'artPubUpdate'});
        print pubDate.text.encode('ascii');
        newsfile.write('<p><h4>'+pubDate.text.encode('ascii')+'</h4></p>');

        articleText = htmldoc.find('div', attrs={'class':'article-text'});
        plaintext = articleText.find_all('p', attrs={'class':'body'});

        for para in plaintext:
            newsfile.write('<p>'+para.encode('ascii')+'</p>');

        newsfile.write('<hr>');

    except Exception,e:
        print str(e);

    newsfile.close();
                
    
def aggregateNews():
    createNewsHTML();
    buildTOC();
    linksfile = open(basedir+"Links.txt","r");
    i=0;
    try:
        for line in linksfile:
            i=i+1;
            if i%2==0:
                fetchHTML(line,i);
    except Exception,e:
        print str(e);
        
    publishNewsHTML();


def email(from_gmail_email,from_gmail_pass, to_kindle_email):
    msg = MIMEMultipart();
    msg['Subject'] = 'Convert';
    msg['From'] = from_gmail_email;
    msg['To'] = to_kindle_email;
    
    part = MIMEBase('application','octet-stream');
    part.set_payload(open(basedir+newsFileName,"r").read());
    Encoders.encode_base64(part);
    part.add_header('Content-Disposition','attachment; filename="'+newsFileName+'"');
    msg.attach(part);
    server = smtplib.SMTP('smtp.gmail.com',587);
    server.ehlo();
    server.starttls();
    server.login(from_gmail_email,from_gmail_pass);
    print 'Sending email...'
    server.sendmail(from_gmail_email,to_kindle_email, msg.as_string());
    server.close();



######## Calling modules ########

fetchRSSXML();
writeLinks();
aggregateNews();
email('youremail@gmail.com','yourpassword','email@kindle.com');
