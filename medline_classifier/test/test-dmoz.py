import unittest
from lxml import etree

import os
import sys
sys.path.append(os.path.join('..', 'src', 'structs'))

import structs


class TestDMozGenerator(unittest.TestCase):

    def testTopic(self):
        topic_id = '123'
        topic_name = 'Top/Bla/Bla/Hopsasa'

        pages = []
        for page_n in range(5):
            pages.append(
                structs.DMozPage(
                    'url-' + str(page_n),
                    'title-' + str(page_n),
                    'description-' + str(page_n),
                    topic_name
                )
            )

        topic = structs.DMozTopic(topic_id, topic_name, pages)
        ontology = structs.DMozOntology([topic])

        root = ontology.getXml()

        expected_str = \
           '<RDF xmlns:r="http://www.w3.org/TR/RDF/" xmlns:d="http://purl.org/dc/elements/1.0/" xmlns="http://dmoz.org/rdf/">' + \
            '<Topic r:id="' + topic_name + '">' + \
             '<catid>' + topic_id + '</catid>' + \
             '<link r:resource="url-0"></link>' + \
             '<link r:resource="url-1"></link>' + \
             '<link r:resource="url-2"></link>' + \
             '<link r:resource="url-3"></link>' + \
             '<link r:resource="url-4"></link>' + \
            '</Topic>' + \
            '<ExternalPage about="url-0">' + \
             '<d:Title>title-0</d:Title>' + \
             '<d:Description>description-0</d:Description>' + \
             '<topic>' + topic_name + '</topic>' + \
             '<priority>1</priority>' + \
            '</ExternalPage>' + \
            '<ExternalPage about="url-1">' + \
             '<d:Title>title-1</d:Title>' + \
             '<d:Description>description-1</d:Description>' + \
             '<topic>' + topic_name + '</topic>' + \
            '</ExternalPage>' + \
            '<ExternalPage about="url-2">' + \
             '<d:Title>title-2</d:Title>' + \
             '<d:Description>description-2</d:Description>' + \
             '<topic>' + topic_name + '</topic>' + \
            '</ExternalPage>' + \
            '<ExternalPage about="url-3">' + \
             '<d:Title>title-3</d:Title>' + \
             '<d:Description>description-3</d:Description>' + \
             '<topic>' + topic_name + '</topic>' + \
            '</ExternalPage>' + \
            '<ExternalPage about="url-4">' + \
             '<d:Title>title-4</d:Title>' + \
             '<d:Description>description-4</d:Description>' + \
             '<topic>' + topic_name + '</topic>' + \
            '</ExternalPage>' + \
           '</RDF>'

        expected_root = etree.fromstring(expected_str)
        self.assertEqual(etree.tostring(root), etree.tostring(expected_root))


if __name__ == '__main__':
    unittest.main()
