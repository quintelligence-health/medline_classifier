import unittest
from parsers.medline_xml import MedlineFileParser


def getFirst(elements):
    for element in elements:
        return element

class TestMedlineParser(unittest.TestCase):

    def testMedlineFile(self):
        fname = 'test/test-files/medline-sample.xml'
        parser = MedlineFileParser()
        parser.parse(fname)

        articles = parser.getArticles()

        self.assertEqual(len(articles), 3)

        article1 = articles[0]
        article2 = articles[1]
        article3 = articles[2]

        self.assertEqual(article1.pmid, '14666039')
        self.assertEqual(article1.title, 'Resection of multifocal non-small cell lung cancer when the bronchioloalveolar subtype is involved.')
        self.assertEqual(article1.abstract, 'Abstract 1 1! Abstract 1 2! Abstract 1 3! Abstract 1 4!')
        self.assertEqual(article1.mesh_headings, ['D002282', 'D000368', 'D000369', 'D001707', 'D002289', 'D015331', 'D005260', 'D005500', 'D006801', 'D007150', 'D008175', 'D008297', 'D008875', 'D009367', 'D011013', 'D011336', 'D012189', 'D018570', 'D018709', 'D016019', 'D016896'])

        self.assertEqual(article2.pmid, '14666041')
        self.assertEqual(article2.title, 'Cisplatin augments cytotoxic T-lymphocyte-mediated antitumor immunity in poorly immunogenic murine lung cancer.')
        self.assertEqual(article2.abstract, 'Abstract 2 1! Abstract 2 2! Abstract 2 3! Abstract 2 4!')
        self.assertEqual(article2.mesh_headings, ['D000256', 'D000818', 'D019014', 'D017209', 'D023201', 'D018827', 'D002945', 'D005260', 'D005434', 'D005455', 'D018014', 'D005822', 'D016219', 'D007274', 'D051379', 'D008810', 'D011336', 'D012680', 'D018709', 'D015996', 'D013602', 'D014407', 'D015854'])

        self.assertEqual(article3.pmid, '14666042')
        self.assertEqual(article3.title, 'Efficacy and safety of single-trocar technique for minimally invasive surgery of the chest in the treatment of noncomplex pleural disease.')
        self.assertEqual(article3.abstract, 'Abstract 3 1! Abstract 3 2! Abstract 3 3! Abstract 3 4!')
        self.assertEqual(article3.mesh_headings, ['D000328', 'D000368', 'D000369', 'D015331', 'D004653', 'D005260', 'D006801', 'D007558', 'D008297', 'D008875', 'D019060', 'D010995', 'D010996', 'D011446', 'D013902', 'D018570', 'D012680', 'D020775', 'D013906', 'D014057', 'D016896'])


if __name__ == '__main__':
    unittest.main()
