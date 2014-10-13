from urllib import parse 
from distutils.debug import DEBUG
from mpicore.models import *
from datetime import date
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.dispatch.dispatcher import NONE_ID
from lxml import etree

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
        tree = None
        try:
            query = {'query':query,
                     'start':start,
                     'count':count}
            query.update(self.defaultQuery)
            encoded_args = parse.urlencode(query)
            url = apiHost + searchMethod + "?" + encoded_args
            if debug_search:
                tree = etree.parse('search3.xml')
            else:
                tree = etree.parse(url)
        except Exception as e:
            print(e)
            raise
        
        nsmap = tree.getroot().nsmap
        nsmap['ns0'] = nsmap.pop(None)

        for entry in tree.findall('.//ns0:entry', nsmap):
            doi = entry.find('prism:doi', nsmap).text
            pub, created = Publication.objects.get_or_create(doi=doi, defaults = {'date':timezone.now()})
            if created:
                pub.name_en = entry.find('dc:title', nsmap).text
                print('Fill info for new publication: {} {}'.format(doi,pub.name_en))
                dateStr = entry.find('prism:coverDate', nsmap).text
                #todo parse date
                pub.date = timezone.now()
                pub.journal, pub.author, pub.affiliation = self.abstractRetrive(doi)
            pub.citations = int(entry.find('ns0:citedby-count', nsmap).text)
            pub.save()  # otherwise name_en is not saved!
            print(['Finished processing: ', pub], '\n')
        totalRes = int(tree.find('opensearch:totalResults', nsmap).text)
        start = int(tree.find('opensearch:startIndex', nsmap).text)
        itemsPerPage = int(tree.find('opensearch:itemsPerPage', nsmap).text)
        print('totalRes: {}, start{}, count{}'.format(totalRes, start, itemsPerPage))
        return totalRes, start, itemsPerPage  
        
    def abstractRetrive(self, doi):
        tree = None
        try:
            query = self.defaultQuery
            encoded_args = parse.urlencode(query)
            url = parse.urljoin(apiHost, parse.quote(abstractRetrivMethod + doi)) + "?" + encoded_args
            if debug_search:
                tree = etree.parse('abstract3.xml')
            else:
                tree = etree.parse(url)
        except Exception as e:
            print(e)
            raise
 
        nsmap = tree.getroot().nsmap
        nsmap['ns0'] = nsmap.pop(None)

        coredata = tree.find('ns0:coredata', nsmap)
        issn = coredata.find('prism:issn', nsmap).text
        publicationName = coredata.find('prism:publicationName', nsmap).text
        journal,_ = Journal.objects.get_or_create(issn=issn, defaults = {'name_en':publicationName})
        print(['journal: ', journal])

        affils = []
        authors = []
        miptRelatedAuthorGroups = tree.xpath('//author-group[author/@auid=//affiliation[@afid=60000308]/../author/@auid]')
        if not miptRelatedAuthorGroups:
            print('WARNING no mipt related author-group available for this publication!')
        for authorGroups in miptRelatedAuthorGroups:
            for org in authorGroups.xpath('affiliation/organization'):
                affil_id = org.getparent().get('afid')
                affil_name = org.text
                affil,_ = Affiliation.objects.get_or_create(af_id = affil_id, defaults = {'name_en':affil_name})
                print(affil)
                affils.append(affil)
         
            for authorElm in authorGroups.xpath('author'):
                authorID = authorElm.get('auid')
                indexedName = authorElm.find('ce:indexed-name', nsmap).text
                author,_ = Author.objects.get_or_create(author_id=authorID, defaults = {'name_en':indexedName})
                print(author)
                authors.append(author)
        return journal, authors, affils

query = 'AF-ID({})'.format(miptAffilationID)
loader().loadAllResultsForQuery(query)        
#loader().scopusRequest(query,count=5)
#loader().abstractRetrive("10.1016/j.atmosres.2014.07.018")