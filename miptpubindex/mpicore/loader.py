import urllib 
import urllib.request as req
from urllib import parse
from bs4 import BeautifulSoup
from distutils.debug import DEBUG
from mpicore.models import *
from datetime import date
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import xml.etree.ElementTree as ET
from django.dispatch.dispatcher import NONE_ID


apiKey = "8b3a879351906d834617638b92a47857"
apiHost = 'http://api.elsevier.com'
searchMethod = '/content/search/index:scopus'
abstractRetrivMethod = '/content/abstract/doi/'
miptAffilationID = "60000308"

debug_search = False

class loader:
    defaultQuery = {'apiKey':apiKey,
                    'httpAccept':'application/xml'}
    def loadAllResultsForQuery(self, query):
        resultCount, start, count = self.scopusRequest(query)
        downloadCount = count
        while downloadCount < resultCount:            
            left = resultCount-downloadCount 
            resultCount, start, count = self.scopusRequest(query, downloadCount, min(left, count))
            downloadCount += count
        
    def scopusRequest(self, query, start=0, count=25):
        print("call start: {} count:{}".format(start, count))
        try:
            query = {'query':query,
                     'start':start,
                     'count':count}
            query.update(self.defaultQuery)
            encoded_args = urllib.parse.urlencode(query)
            url = apiHost + searchMethod + "?" + encoded_args
            request = req.Request(url)
            if debug_search:
                returnDoc = open('search.xml', 'r').read()
            else:
                returnDoc = req.urlopen(request).read()
        except (urllib.error.HTTPError, urllib.error.URLError) as er:
            print(er)
        
        tree = ET.XML(returnDoc)
        namespaces = {'xmlns':'http://www.w3.org/2005/Atom',
                      'dc':'http://purl.org/dc/elements/1.1/',
                      'prism':'http://prismstandard.org/namespaces/basic/2.0/',
                      'opensearch':'http://a9.com/-/spec/opensearch/1.1/'}

        for entry in tree.findall('.//xmlns:entry', namespaces):
            doi = entry.find('prism:doi', namespaces).text
            print ('===== pub: {}'.format(doi))
            try:
               pub = Publication.objects.get(doi=doi)
            except (Publication.DoesNotExist):
                name_en = entry.find('dc:title', namespaces).text
                dateStr = entry.find('prism:coverDate', namespaces).text
                #todo parse date
                date = timezone.now()
                affil_name = entry.find('./xmlns:affiliation/xmlns:affilname', namespaces).text
                affil = Affiliation.objects.get_or_create(af_id = affil_name, name_en = affil_name)
                journal, authors = self.abstractRetrive(doi)
                pub = Publication(doi=doi, 
                                  name_en = name_en, 
                                  date = date,  
                                  journal = journal)
                pub.save()
                pub.author = authors
                pub.affiliation = [affil,]
            pub.citations = int(entry.find('xmlns:citedby-count', namespaces).text)
            #print(pub)
        totalRes = int(tree.find('opensearch:totalResults', namespaces).text)
        start = int(tree.find('opensearch:startIndex', namespaces).text)
        itemsPerPage = int(tree.find('opensearch:itemsPerPage', namespaces).text)
        print('totalRes: {}, start{}, count{}'.format(totalRes, start, itemsPerPage))
        return totalRes, start, itemsPerPage  
        
    def abstractRetrive(self, doi):
        try:
            query = self.defaultQuery
            encoded_args = parse.urlencode(query)
            url = parse.urljoin(apiHost, parse.quote(abstractRetrivMethod + doi)) + "?" + encoded_args
            print(url)
            request = req.Request(url)
            if debug_search:
                returnDoc = open('abstract.xml', 'r').read()
            else:
                returnDoc = req.urlopen(request).read()
        except (urllib.error.HTTPError, urllib.error.URLError) as er:
            print(er)
 
        tree = ET.XML(returnDoc)
        namespaces = {'xmlns':'http://www.elsevier.com/xml/svapi/abstract/dtd',
                      'ce':'http://www.elsevier.com/xml/ani/common',
                      'prism':'http://prismstandard.org/namespaces/basic/2.0/'
                      }
        
        
        
        coredata = tree.find('xmlns:coredata', namespaces)
        issn = coredata.find('prism:issn', namespaces).text
        try:
            journal = Journal.objects.get(issn=issn)
        except (Journal.DoesNotExist):
            publicationName = coredata.find('prism:publicationName', namespaces).text
            journal = Journal(issn = issn, name_en = publicationName)
            journal.save()
        
        authors = []
        for authorElm in tree.findall('.//xmlns:authors/xmlns:author', namespaces):
            authorID = authorElm.attrib['auid']
            try:
                author = Author.objects.get(author_id=authorID)
                print ("authore {} for id {}".format(author, authorID))
            except (Author.DoesNotExist):    
                indexedName = authorElm.find('ce:indexed-name', namespaces).text
                author = Author(author_id=authorID, name_en = indexedName)
                author.save()
                print(author)
            authors.append(author)
        return journal, authors

query = 'AF-ID({})'.format(miptAffilationID)
loader().loadAllResultsForQuery(query)        
#loader().scopusRequest(query,count=5)
#loader().abstractRetrive("10.1016/j.atmosres.2014.07.018")

