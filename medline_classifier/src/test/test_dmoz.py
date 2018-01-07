import unittest
import structs.dmoz_structs as structs
import xtdiff
import shutil
from io import StringIO
import os
import platform

from lxml import etree
from util.arguments import settings

# linesep = os.linesep
# linesep = u'\n'
linesep = None

is_win = platform.system() != 'Linux' and platform.system() != 'Darwin'

print 'using Windows: ' + str(is_win)

def os_path(path):
    if is_win:
        return r"\\?\%s" % path
    else:
        return path

def os_category(category):
    if is_win:
        return category.replace('/', '\\')
    else:
        return category

def xml_compare(r1, r2):
    diffs = xtdiff.diff(r1, r2)
    return len(diffs) == 0

def clear_cache():
    cache_dir = settings['cache_path']
    for file in os.listdir(cache_dir):
        path_name = os.path.join(cache_dir, file)
        shutil.rmtree(os_path(path_name))


class TestDMozGenerator(unittest.TestCase):

    def testContentFile(self):
        clear_cache()

        topic_id = '123'
        topic_name = 'Top/Bla/Bla/Hopsasa'

        # topic = structs.DMozTopic(topic_id, topic_name, [])
        ontology = structs.DMozOntology(settings['cache_path'])

        ontology.defineTopic(3, 'Top/Bla', 'description-3')
        ontology.defineTopic(4, 'Top/Bla/Bla', 'description-4')
        ontology.defineTopic(5, 'Top/Bla/Bla/Hopsasa', 'description-5')
        ontology.defineTopic(topic_id, topic_name, 'description-' + topic_id)

        for page_n in range(5):
            page = structs.DMozPage(
                'url-' + str(page_n),
                'title-' + str(page_n),
                'description-' + str(page_n),
                topic_id,
                topic_name
            )
            ontology.addPage(page)

        output = StringIO(newline=linesep)
        ontology.writeContentXml(output)
        root = etree.fromstring(output.getvalue())

        expected_str = \
           '<RDF xmlns:d="http://purl.org/dc/elements/1.0/" xmlns:r="http://www.w3.org/TR/RDF/" xmlns="http://dmoz.org/rdf/">' + \
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

        # print etree.tostring(root, pretty_print=True)

        expected_root = etree.fromstring(expected_str)

        expected_str = etree.tostring(expected_root)
        actual_str = etree.tostring(root)
        self.assertEqual(expected_str, actual_str)

    def testStructureFile(self):
        clear_cache()

        ontology = structs.DMozOntology(settings['cache_path'])

        ontology.defineTopic(3, 'Top/Pages', 'topic-3')
        ontology.defineTopic(4, 'Top/Utils', 'topic-4')

        ontology.defineTopic(5, 'Top/Pages/Book', 'topic-5')
        ontology.defineTopic(6, 'Top/Pages/Html', 'topic-6')
        ontology.defineTopic(7, 'Top/Pages/Web', 'topic-7')    # should not appear in the output because it is empty
        ontology.defineTopic(8, 'Top/Utils/Web', 'topic-8')

        page1 = structs.DMozPage('url-1', 'title-1', 'description-1', 5, 'Top/Pages/Book')
        page2 = structs.DMozPage('url-2', 'title-2', 'description-2', 5, 'Top/Pages/Book')
        page3 = structs.DMozPage('url-3', 'title-3', 'description-3', 6, 'Top/Pages/Html')
        page4 = structs.DMozPage('url-4', 'title-4', 'description-4', 8, 'Top/Utils/Web')

        ontology.addPage(page1)
        ontology.addPage(page2)
        ontology.addPage(page3)
        ontology.addPage(page4)

        output = StringIO(newline=linesep)
        ontology.writeStructureXml(output)
        root = etree.fromstring(output.getvalue())

        expected_str = \
            '<RDF xmlns:d="http://purl.org/dc/elements/1.0/" xmlns:r="http://www.w3.org/TR/RDF/" xmlns="http://dmoz.org/rdf/">' + \
              '<Topic r:id="">' + \
                  '<catid>1</catid>' + \
                  '<d:Title></d:Title>' + \
                  '<d:Description></d:Description>' + \
                  '<narrow r:resource="Top"></narrow>' + \
              '</Topic>' + \
              '<Topic r:id="Top/World">' + \
                  '<catid>2</catid>' + \
                  '<d:Title>Top</d:Title>' + \
                  '<d:Description></d:Description>' + \
                  '<narrow r:resource="Top/Utils"></narrow>' + \
                  '<narrow r:resource="Top/Pages"></narrow>' + \
              '</Topic>' + \
              '<Topic r:id="Top/Pages">' + \
                  '<catid>3</catid>' + \
                  '<d:Title>Pages</d:Title>' + \
                  '<d:Description>topic-3</d:Description>' + \
                  '<narrow r:resource="Top/Pages/Html"></narrow>' + \
                  '<narrow r:resource="Top/Pages/Book"></narrow>' + \
              '</Topic>' + \
              '<Topic r:id="Top/Pages/Book">' + \
                  '<catid>5</catid>' + \
                  '<d:Title>Book</d:Title>' + \
                  '<d:Description>topic-5</d:Description>' + \
              '</Topic>' + \
              '<Topic r:id="Top/Pages/Html">' + \
                  '<catid>6</catid>' + \
                  '<d:Title>Html</d:Title>' + \
                  '<d:Description>topic-6</d:Description>' + \
              '</Topic>' + \
              '<Topic r:id="Top/Utils">' + \
                  '<catid>4</catid>' + \
                  '<d:Title>Utils</d:Title>' + \
                  '<d:Description>topic-4</d:Description>' + \
                  '<narrow r:resource="Top/Utils/Web"></narrow>' + \
              '</Topic>' + \
              '<Topic r:id="Top/Utils/Web">' + \
                  '<catid>8</catid>' + \
                  '<d:Title>Web</d:Title>' + \
                  '<d:Description>topic-8</d:Description>' + \
              '</Topic>' + \
            '</RDF>'

        expected_root = etree.fromstring(expected_str)

        expected_str = etree.tostring(expected_root)
        actual_str = etree.tostring(root)

        eq = expected_str == actual_str
        if not eq:
            print 'expected:\n' + expected_str
            print '\nactual:\n' + actual_str

        self.assertEqual(expected_str, actual_str)

    def testConstruction(self):
        clear_cache()

        ontology = structs.DMozOntology(settings['cache_path'])

        ontology.defineTopic(3, 'Top/Pages', 'description-3')
        ontology.defineTopic(4, 'Top/Girlscouts', 'description-4')
        ontology.defineTopic(5, 'Top/Pages/Tralala', 'description-5')
        ontology.defineTopic(6, 'Top/Girlscouts/Hopsasa', 'description-6')

        page1 = structs.DMozPage('url-1', 'title-1', 'description-1', 5, 'Top/Pages/Tralala')
        page2 = structs.DMozPage('url-2', 'title-2', 'description-2', 5, 'Top/Pages/Tralala')
        page3 = structs.DMozPage('url-3', 'title-3', '<description-3 & >', 6, 'Top/Girlscouts/Hopsasa')

        ontology.addPage(page1)
        ontology.addPage(page2)
        ontology.addPage(page3)

        output = StringIO(newline=linesep)
        ontology.writeContentXml(output)
        root = etree.fromstring(output.getvalue())

        # TODO should the "Top" topic be here???
        expected_str = \
           '<RDF xmlns:d="http://purl.org/dc/elements/1.0/" xmlns:r="http://www.w3.org/TR/RDF/" xmlns="http://dmoz.org/rdf/">' + \
            '<Topic r:id="">' + \
             '<catid>1</catid>' + \
            '</Topic>' + \
            '<Topic r:id="Top/World">' + \
             '<catid>2</catid>' + \
            '</Topic>' + \
            \
            '<Topic r:id="Top/Pages">' + \
             '<catid>3</catid>' + \
            '</Topic>' + \
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
            '<Topic r:id="Top/Girlscouts">' + \
             '<catid>4</catid>' + \
            '</Topic>' + \
            '<Topic r:id="Top/Girlscouts/Hopsasa">' + \
             '<catid>6</catid>' + \
             '<link r:resource="url-3"></link>' + \
            '</Topic>' + \
            '<ExternalPage about="url-3">' + \
             '<d:Title>title-3</d:Title>' + \
             '<d:Description>&lt;description-3 &amp; &gt;</d:Description>' + \
             '<topic>Top/Girlscouts/Hopsasa</topic>' + \
             '<priority>1</priority>' + \
            '</ExternalPage>' + \
           '</RDF>'

        expected_root = etree.fromstring(expected_str)

        expected_str = etree.tostring(expected_root)
        actual_str = etree.tostring(root)

        eq = expected_str == actual_str
        if not eq:
            print 'expected:\n' + expected_str
            print '\nactual:\n' + actual_str

        self.assertEqual(expected_str, actual_str)

#         self.assertTrue(xml_compare(root, expected_root))

    def testExceptNonExistTopic(self):
        clear_cache()

        ontology = structs.DMozOntology(settings['cache_path'])
        ontology.defineTopic(3, 'Top/Pages', 'description-3')

        with self.assertRaises(ValueError):
            ontology.defineTopic(4, 'Top/Bla/Hop', 'description-4')
        with self.assertRaises(ValueError):
            page = structs.DMozPage('url-4', 'title-4', 'description-4', 5, 'Top/Girlscouts/Hopsasa')
            ontology.addPage(page)
        with self.assertRaises(ValueError):
            page = structs.DMozPage('url-1', 'title-1', 'description-1', 3, 'Top/Pages/Tralala')
            ontology.addPage(page)


if __name__ == '__main__':
    unittest.main()
