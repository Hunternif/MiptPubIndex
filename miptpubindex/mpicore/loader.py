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
abstractRetrivMethod = '/content/abstract/eid/'
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
        query = {'query':query,
                 'start':start,
                 'count':count}
        query.update(self.defaultQuery)
        encoded_args = parse.urlencode(query)
        url = apiHost + searchMethod + "?" + encoded_args
        try:
            if debug_search:
                tree = etree.parse('search3.xml')
            else:
                tree = etree.parse(url)
        except IOError as e:
            print(['Failed to load search request: ',e])
            return 0,0,0
        
        nsmap = tree.getroot().nsmap
        nsmap['ns0'] = nsmap.pop(None)

        for entry in tree.findall('.//ns0:entry', nsmap):           
            eid = entry.find('ns0:eid', nsmap).text
            print('Fill info for new publication: {}'.format(eid))
            pub, created = Publication.objects.get_or_create(eid=eid, defaults = {'date':timezone.now()})
            if created:
                doiElm = entry.find('prism:doi', nsmap)
                if doiElm is not None:
                    pub.doi = doiElm.text
                pub.name_en = entry.find('dc:title', nsmap).text
                print('Title: {}'.format(pub.name_en))
                dateStr = entry.find('prism:coverDate', nsmap).text
                #todo parse date
                pub.date = timezone.now()
                try:
                    pub.journal, pub.author, pub.affiliation = self.abstractRetrive(eid)
                except IOError as e:
                    print(['Failed to load more details about this paper:', e])
                    pub.delete();
                    pub = None;
            if pub is not None:                        
                pub.citations = int(entry.find('ns0:citedby-count', nsmap).text)
                pub.save()  # otherwise name_en is not saved!
                print(['Finished processing: ', pub], '\n')
        totalRes = int(tree.find('opensearch:totalResults', nsmap).text)
        start = int(tree.find('opensearch:startIndex', nsmap).text)
        itemsPerPage = int(tree.find('opensearch:itemsPerPage', nsmap).text)
        print('totalRes: {}, start{}, count{}'.format(totalRes, start, itemsPerPage))
        return totalRes, start, itemsPerPage  
        
    def abstractRetrive(self, eid):
        tree = None        
        query = self.defaultQuery
        encoded_args = parse.urlencode(query)
        url = parse.urljoin(apiHost, parse.quote(abstractRetrivMethod + eid)) + "?" + encoded_args
        if debug_search:
            tree = etree.parse('abstract3.xml')
        else:
            tree = etree.parse(url)
 
        nsmap = tree.getroot().nsmap
        nsmap['ns0'] = nsmap.pop(None)

        coredata = tree.find('ns0:coredata', nsmap)
        id_type = None
        journal_id = None
        publicationName = None
        issnElm = coredata.find('prism:issn', nsmap)
        isbnElm = coredata.find('prism:isbn', nsmap)
        publicationNameElm = coredata.find('prism:publicationName', nsmap)
        
        if publicationNameElm is not None:
            publicationName = publicationNameElm.text
        if issnElm is not None:
            id_type = 'ISSN'
            journal_id = issnElm.text
        elif isbnElm is not None:
            id_type = 'ISBN'
            journal_id = isbnElm.text
        elif publicationName is not None:
            id_type = 'NAME'
            journal_id = publicationName[:50]
            
        if journal_id is not None:
            if publicationName is None:
                publicationName = journal_id
            journal,_ = Journal.objects.get_or_create(id=journal_id, id_type=id_type, defaults={'name_en':publicationName})
            print(['journal: ', journal])
        else:
            print('could not get info about journal')

        affils = []
        authors = []
        miptRelatedAuthorGroups = tree.xpath('//author-group[author/@auid=//affiliation[@afid=60000308]/../author/@auid]')
        if not miptRelatedAuthorGroups:
            print('WARNING no mipt related author-group available for this publication!')
        for authorGroups in miptRelatedAuthorGroups:
            for org in authorGroups.xpath('affiliation/organization'):
                affil_name = org.text
                affil_id = org.getparent().get('afid')
                if affil_id is None:
                    affil_id = affil_name[:50]
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
#loader().scopusRequest(query,5000, 25)
#loader().abstractRetrive("2-s2.0-84897695957")
