import unittest
from lxml import etree

import os
import sys
sys.path.append(os.path.join('..', 'src', 'structs'))

import structs


class TestDMozGenerator(unittest.TestCase):

    def testContentFile(self):
        topic_id = '123'
        topic_name = 'Top/Bla/Bla/Hopsasa'

        # topic = structs.DMozTopic(topic_id, topic_name, [])
        ontology = structs.DMozOntology()

        ontology.defineTopic(3, 'Top/Bla')
        ontology.defineTopic(4, 'Top/Bla/Bla')
        ontology.defineTopic(5, 'Top/Bla/Bla/Hopsasa')
        ontology.defineTopic(topic_id, topic_name)

        for page_n in range(5):
            page = structs.DMozPage(
                'url-' + str(page_n),
                'title-' + str(page_n),
                'description-' + str(page_n),
                topic_id,
                topic_name
            )
            ontology.addPage(page)

        root = ontology.getContentXml()

        expected_str = \
           '<RDF xmlns:r="http://www.w3.org/TR/RDF/" xmlns:d="http://purl.org/dc/elements/1.0/" xmlns="http://dmoz.org/rdf/">' + \
            '<Topic r:id="">' + \
             '<catid>1</catid>' + \
            '</Topic>' + \
            '<Topic r:id="Top/World">' + \
             '<catid>2</catid>' + \
            '</Topic>' + \
            '<Topic r:id="Top/Bla">' + \
             '<catid>3</catid>' + \
            '</Topic>' + \
            '<Topic r:id="Top/Bla/Bla">' + \
             '<catid>4</catid>' + \
            '</Topic>' + \
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

        print etree.tostring(root, pretty_print=True)

        expected_root = etree.fromstring(expected_str)
        self.assertEqual(etree.tostring(root), etree.tostring(expected_root))

    def testStructureFile(self):
        pass

    def testConstruction(self):
        ontology = structs.DMozOntology()

        ontology.defineTopic(3, 'Top/Pages')
        ontology.defineTopic(4, 'Top/Girlscouts')
        ontology.defineTopic(5, 'Top/Pages/Tralala')
        ontology.defineTopic(6, 'Top/Girlscouts/Hopsasa')

        page1 = structs.DMozPage('url-1', 'title-1', 'description-1', 7, 'Top/Pages/Tralala')
        page2 = structs.DMozPage('url-2', 'title-2', 'description-2', 7, 'Top/Pages/Tralala')
        page3 = structs.DMozPage('url-3', 'title-3', 'description-3', 8, 'Top/Girlscouts/Hopsasa')

        ontology.addPage(page1)
        ontology.addPage(page2)
        ontology.addPage(page3)

        root = ontology.getContentXml()

        # TODO should the "Top" topic be here???
        expected_str = \
           '<RDF xmlns:r="http://www.w3.org/TR/RDF/" xmlns:d="http://purl.org/dc/elements/1.0/" xmlns="http://dmoz.org/rdf/">' + \
            '<Topic r:id="">' + \
             '<catid>1</catid>' + \
            '</Topic>' + \
            \
            '<Topic r:id="Top/Pages/Tralala">' + \
             '<catid>5</catid>' + \
             '<link r:resource="url-1"></link>' + \
             '<link r:resource="url-2"></link>' + \
            '</Topic>' + \
            '<ExternalPage about="url-1">' + \
             '<d:Title>title-1</d:Title>' + \
             '<d:Description>description-1</d:Description>' + \
             '<topic>Top/Pages/Tralala</topic>' + \
             '<priority>1</priority>' + \
            '</ExternalPage>' + \
            '<ExternalPage about="url-2">' + \
             '<d:Title>title-2</d:Title>' + \
             '<d:Description>description-2</d:Description>' + \
             '<topic>Top/Pages/Tralala</topic>' + \
            '</ExternalPage>' + \
            \
            '<Topic r:id="Top/Girlscouts/Hopsasa">' + \
             '<catid>6</catid>' + \
             '<link r:resource="url-3"></link>' + \
            '</Topic>' + \
            '<ExternalPage about="url-3">' + \
             '<d:Title>title-3</d:Title>' + \
             '<d:Description>description-3</d:Description>' + \
             '<topic>Top/Girlscouts/Hopsasa</topic>' + \
             '<priority>1</priority>' + \
            '</ExternalPage>' + \
           '</RDF>'

        expected_root = etree.fromstring(expected_str)
        self.assertEqual(etree.tostring(root), etree.tostring(expected_root))

    def testExceptNonExistTopic(self):
        ontology = structs.DMozOntology()
        ontology.defineTopic(3, 'Top/Pages')

        with self.assertRaises(ValueError):
            structs.DMozPage('url-4', 'title-4', 'description-4', 5, 'Top/Girlscouts/Hopsasa')
        with self.assertRaises(ValueError):
            structs.DMozPage('url-1', 'title-1', 'description-1', 3, 'Top/Pages/Tralala')


if __name__ == '__main__':
    unittest.main()
