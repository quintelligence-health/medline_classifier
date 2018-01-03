import os
import json
import shutil
import platform


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

# linesep = os.linesep
linesep = ''
# linesep = u'\n'

is_win = platform.system() != 'Linux' and platform.system() != 'Darwin'

print 'using Windows: ' + str(is_win)

def os_path(path):
    if is_win:
        print 'returning Windows path'
        return r"\\?\%s" % path
    else:
        print 'returning Unix path'
        return path

def os_category(category):
    if is_win:
        return category.replace('/', '\\')
    else:
        return category


class DMozPage:

    def __init__(self, url, title, description, topic_id, topic_name):
        self.url = url
        self.title = title
        self.description = description
        self.topic_id = str(topic_id)
        self.topic_name = topic_name

    def getJson(self):
        page_json = {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'topic_id': self.topic_id,
            'topic_name': self.topic_name
        }
        return json.dumps(page_json)

    @staticmethod
    def parseJson(json_str):
        page_json = json.loads(json_str)
        url = page_json['url']
        title = page_json['title']
        description = page_json['description']
        topic_id = page_json['topic_id']
        topic_name = page_json['topic_name']
        return DMozPage(url, title, description, topic_id, topic_name)

    def writeToXml(self, fout, write_priority):
        fout.write(u'<ExternalPage about="' + self.url + '">')
        fout.write(u'<d:Title>' + unicode(self.title) + u'</d:Title>')
        fout.write(u'<d:Description>' + unicode(self.description) + u'</d:Description>')
        fout.write(u'<topic>' + self.topic_name + '</topic>')
        if write_priority:
            fout.write(u'<priority>1</priority>')
        fout.write(u'</ExternalPage>')

    # def getXml(self):
    #     page_el = etree.Element('ExternalPage', about=self.url)

    #     title_el = etree.Element(DMOZ_ELEMENTS + 'Title', nsmap=DMOZ_NS_MAP)
    #     title_el.text = self.title
    #     page_el.append(title_el)

    #     desc_el = etree.Element(DMOZ_ELEMENTS + 'Description', nsmap=DMOZ_NS_MAP)
    #     desc_el.text = self.description
    #     page_el.append(desc_el)

    #     topic_el = etree.Element('topic')
    #     topic_el.text = self.topic_name
    #     page_el.append(topic_el)

    #     return page_el



class DMozTopic:

    def __init__(self, root_path, topic_id, title, path_name, output_name, description):
        self.topic_id = str(topic_id)
        self.title = title
        self.path_name = path_name
        self.output_name = output_name
        self.description = description
        # self.pages = []

        self._subtopic_map = {}
        self._root_path = root_path

        self._should_write = None

        topic_dir = os.path.join(root_path, os_category(output_name))
        if not os.path.exists(os_path(topic_dir)):
            os.makedirs(os_path(topic_dir))

    def addSubtopic(self, subtopic):
        self._subtopic_map[subtopic.title] = subtopic

    def getSubtopicByTitle(self, title):
        if title not in self._subtopic_map:
            raise ValueError('Subtopic `' + title + '` doesn\'t exist!')
        return self._subtopic_map[title]

    def addPage(self, page):
        fname = self._getPagesFName()
        with open(os_path(fname), 'a') as f:
            f.write(page.getJson() + '\n')
        # self.pages.append(page)

    def writeContentToXml(self, fout):
        print 'writing content of ' + self.path_name

        pages = self._getPages()

        fout.write(u'<Topic r:id="' + self.output_name + '">' + linesep)
        fout.write(u'<catid>' + self.topic_id + '</catid>' + linesep)
        for page in pages:
            fout.write(u'<link r:resource="' + page.url + '"></link>' + linesep)
        fout.write(u'</Topic>' + linesep)

        # write the pages
        for pageN, page in enumerate(pages):
            page.writeToXml(fout, pageN == 0)

        # write the subtopics
        for subtopic in self._subtopic_map.values():
            subtopic.writeContentToXml(fout)

    def shouldWriteStructureToXml(self):
        if not hasattr(self, '_should_write'):
            self._should_write = None

        if self._should_write is None:
            print 'counting subtree structure of ' + self.path_name
            pages = self._getPages()    # TODO put this after the recursive call

            should_write = len(pages) > 0
            for subtopic in self._subtopic_map.values():
                should_write_child = subtopic.shouldWriteStructureToXml()
                should_write |= should_write_child

            self._should_write = should_write
        return self._should_write


    def writeStructureToXml(self, fout):
        print 'writing structure of ' + self.path_name

        pages = self._getPages()    # TODO put this after the recursive should_write

        should_write = len(pages) > 0
        write_child_arr = []
        subtopics_rev = [subtopic for subtopic in self._subtopic_map.values()]
        subtopics = [subtopics_rev[len(subtopics_rev)-1-i] for i in range(len(subtopics_rev))]

        # write all the subtopics
        for subtopic in subtopics:
            should_write_child = subtopic.shouldWriteStructureToXml()
            should_write |= should_write_child
            write_child_arr.append(should_write_child)

        # if we wrote at least one subtopic then insert yourself at the begining
        if should_write:
            print 'writing node ' + self.path_name
            fout.write(u'<Topic r:id="' + self.output_name + '">' + linesep)
            # topic_el = etree.Element('Topic')
            # topic_el.set(DMOZ_RDF + 'id', self.output_name)

            fout.write(u'<catid>' + self.topic_id + '</catid>' + linesep)
            # catid_el = etree.Element('catid')
            # catid_el.text = self.topic_id
            # topic_el.append(catid_el)

            fout.write(u'<d:Title>' + self.title + '</d:Title>' + linesep)
            # title_el = etree.Element(DMOZ_ELEMENTS + 'Title', nsmap=DMOZ_NS_MAP)
            # title_el.text = self.title
            # topic_el.append(title_el)

            fout.write(u'<d:Description>' + (self.description if self.description is not None else '') + '</d:Description>' + linesep)
            # desc_el = etree.Element(DMOZ_ELEMENTS + 'Description', nsmap=DMOZ_NS_MAP)
            # desc_el.text = self.description if self.description is not None else ''
            # topic_el.append(desc_el)

            for subtopicN, subtopic in enumerate(self._subtopic_map.values()):
                if not write_child_arr[subtopicN]:
                    continue
                fout.write(u'<narrow r:resource="' + subtopic.path_name + '"></narrow>' + linesep)
                # narrow_el = etree.Element('narrow')
                # narrow_el.set(DMOZ_RDF + 'resource', subtopic.path_name)
                # narrow_el.text = ''
                # topic_el.append(narrow_el)

            fout.write(u'</Topic>' + linesep)

            # write the subtopics
            for subtopicN, subtopic in enumerate(subtopics):
                if not write_child_arr[subtopicN]:
                    continue
                subtopic.writeStructureToXml(fout)


        # return whether we wrote ourself

    def _getPages(self):
        pages = []
        fname = self._getPagesFName()
        if os.path.exists(os_path(fname)):
            with open(os_path(fname), 'r') as f:
                for page_json in f.xreadlines():
                    page_json = page_json.strip()
                    if len(page_json) == 0:
                        continue
                    page = DMozPage.parseJson(page_json)
                    pages.append(page)
        return pages

    def _getTopicDir(self):
        return os.path.join(self._root_path, os_category(self.output_name))

    def _getPagesFName(self):
        return os.path.join(self._getTopicDir(), 'pages.json')

    def __str__(self):
        return '<`' + self.topic_id + '`,`' + self.path_name + '`>'


class DMozOntology:

    def __init__(self, cache_path):
        self._cache_path = cache_path
        self._root_topic = DMozTopic(cache_path, '1', '', '', '', '')
        self._topic_map = {
            '1': self._root_topic
        }

        self._root_topic.addSubtopic(DMozTopic(cache_path, '2', 'Top', 'Top', 'Top/World', ''))

    def clearCacheDir(self):
        for file in os.listdir(os_path(self._cache_path)):
            path_name = os.path.join(os_path(self._cache_path), file)
            shutil.rmtree(path_name)

    def defineTopic(self, topic_id, topic_name, description):
        topic_id = str(topic_id)

        if self.topicExists(topic_id):
            raise ValueError('Topic `' + str(topic_id) + '` already exists!')

        topic_path = topic_name.split('/')

        parent_topic = self._root_topic
        for subtopic_title in topic_path[0:-1]:
            parent_topic = parent_topic.getSubtopicByTitle(subtopic_title)

        topic = DMozTopic(self._cache_path, topic_id, topic_path[-1], topic_name, topic_name, description)
        parent_topic.addSubtopic(topic)
        self._topic_map[topic_id] = topic

    def addPage(self, page):
        topic_id = page.topic_id
        topic_name = page.topic_name

        if not self.topicExists(topic_id):
            raise ValueError('Topic `' + topic_name + '` with ID `' + topic_id + '` does not exist!')

        topic = self.getTopic(topic_id)
        if topic.output_name != topic_name:
            raise ValueError('Invalid name of topic ' + str(topic) + ', page has: ' + page.topic_name)

        topic.addPage(page)

    def getTopic(self, topic_id):
        return self._topic_map[str(topic_id)]

    def topicExists(self, topic_id):
        return str(topic_id) in self._topic_map

    def writeContentXml(self, fout):
        fout.write(u'<RDF xmlns:d="http://purl.org/dc/elements/1.0/" xmlns:r="http://www.w3.org/TR/RDF/" xmlns="http://dmoz.org/rdf/">' + linesep)
        self._root_topic.writeContentToXml(fout)
        fout.write(u'</RDF>')

    def writeStructureXml(self, fout):
        topic = self._root_topic

        fout.write(u'<RDF xmlns:d="http://purl.org/dc/elements/1.0/" xmlns:r="http://www.w3.org/TR/RDF/" xmlns="http://dmoz.org/rdf/">' + linesep)
        topic.writeStructureToXml(fout)
        fout.write(u'</RDF>')
