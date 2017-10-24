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


class DMozPage:

    def __init__(self, url, title, description, topic_id, topic_name):
        self.url = url
        self.title = title
        self.description = description
        self.topic_id = str(topic_id)
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

    def __init__(self, topic_id, path_name, output_name, pages):
        self.topic_id = str(topic_id)
        self.path_name = path_name
        self.output_name = output_name
        self.pages = pages

        self._subtopic_map = {}

    def addSubtopic(self, subtopic):
        self._subtopic_map[subtopic.path_name] = subtopic

    def getSubtopicByName(self, path_name):
        return self._subtopic_map[path_name]

    def addPage(self, page):
        self.pages.append(page)

    def writeToXml(self, root):
        topic_el = etree.Element('Topic')
        topic_el.set(DMOZ_RDF + 'id', self.output_name)

        catid_el = etree.Element('catid')
        catid_el.text = self.topic_id

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

        for subtopic in self._subtopic_map.values():
            subtopic.writeToXml(root)


class DMozOntology:

    def __init__(self):
        self._topic_map = {}
        self._root_topic = DMozTopic(1, '', '', [])

        self._root_topic.addSubtopic(DMozTopic(2, 'Top', 'Top/World', []))

    def addPage(self, page):
        topic_id = page.topic_id
        topic_name = page.topic_name

        if not self.topicExists(topic_id):
            raise ValueError('Topic `' + topic_name + '` does not exist!')
            # self._createTopic(topic_id, topic_name)

        topic = self.getTopic(topic_id)
        topic.addPage(page)

    def getTopic(self, topic_id):
        return self._topic_map[topic_id]

    def topicExists(self, topic_id):
        return topic_id in self._topic_map

    def defineTopic(self, topic_id, topic_name):
        if self.topicExists(topic_id):
            return

        topic_path = topic_name.split('/')

        parent_topic = self._root_topic
        for name_part in topic_path[0:-1]:
            parent_topic = parent_topic.getSubtopicByName(name_part)

        topic = DMozTopic(topic_id, topic_path[-1], topic_name, [])
        parent_topic.addSubtopic(topic)
        self._topic_map[topic_id] = topic

    def getContentXml(self):
        root = etree.Element('RDF', nsmap=DMOZ_NS_MAP)

        topic = self._root_topic
        topic.writeToXml(root)
        # for topic in self.topics:
        #     topic.writeToXml(root)
        return root
