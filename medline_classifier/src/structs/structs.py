from lxml import etree


DMOZ_DEFAULT_NS = 'http://dmoz.org/rdf/'
DMOZ_RDF_NS = 'http://www.w3.org/TR/RDF/'
DMOZ_ELEMENTS_NS = 'http://purl.org/dc/elements/1.0/'

DMOZ_DEFAULT = '{%s}' % DMOZ_DEFAULT_NS
DMOZ_RDF = '{%s}' % DMOZ_RDF_NS
DMOZ_ELEMENTS = '{%s}' % DMOZ_ELEMENTS_NS

DMOZ_NS_MAP = {
    None: DMOZ_DEFAULT_NS,
    'r': DMOZ_RDF_NS,
    'd': DMOZ_ELEMENTS_NS
}


class MedlineArticle:

    def __init__(self, pmid, title, abstract, category_ids):
        self.pmid = pmid
        self.title = title
        self.abstract = abstract
        self.category_ids = category_ids


class DMozOntology:

    def __init__(self, topics):
        self.topics = topics

    def getXml(self):
        root = etree.Element('RDF', nsmap=DMOZ_NS_MAP)
        for topic in self.topics:
            topic.writeToXml(root)
        return root


class DMozPage:

    def __init__(self, url, title, description, topic_name):
        self.url = url
        self.title = title
        self.description = description
        self.topic_name = topic_name

    def writeToXml(self, root):
        root.append(self.getXml())

    def getXml(self):
        page_el = etree.Element('ExternalPage', about=self.url)

        title_el = etree.Element(DMOZ_ELEMENTS + 'Title', nsmap=DMOZ_NS_MAP)
        title_el.text = self.title
        page_el.append(title_el)

        desc_el = etree.Element(DMOZ_ELEMENTS + 'Description', nsmap=DMOZ_NS_MAP)
        desc_el.text = self.description
        page_el.append(desc_el)

        topic_el = etree.Element('topic')
        topic_el.text = self.topic_name
        page_el.append(topic_el)

        return page_el


class DMozTopic:

    def __init__(self, category_id, category_name, pages):
        self.category_id = category_id
        self.category_name = category_name
        self.pages = pages

    def writeToXml(self, root):
        topic_el = etree.Element('Topic')
        topic_el.set(DMOZ_RDF + 'id', self.category_name)

        catid_el = etree.Element('catid')
        catid_el.text = self.category_id

        topic_el.append(catid_el)

        root.append(topic_el)
        for i, page in enumerate(self.pages):
            link = etree.Element('link')
            link.set(DMOZ_RDF + 'resource', page.url)

            topic_el.append(link)
            page_el = page.getXml()

            if i == 0:
                priority_el = etree.Element('priority')
                priority_el.text = '1'
                page_el.append(priority_el)

            root.append(page_el)
