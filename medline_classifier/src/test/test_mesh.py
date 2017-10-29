import unittest
from sets import Set
from parsers.mesh_xml import MeshParser
from util.arguments import settings


class TestMeshParser(unittest.TestCase):

    def testCategories(self):
        fname = settings['mesh_path']
        parser = MeshParser()
        parser.parse(fname)

        # TEST 1
        paths = parser.getCategoryPaths('D005266')
        expected_paths = Set([
            'Diseases/Musculoskeletal Diseases/Bone Diseases/Bone Neoplasms/Femoral Neoplasms',
            'Diseases/Neoplasms/Neoplasms by Site/Bone Neoplasms/Femoral Neoplasms'
        ])

        self.assertEqual(len(Set(paths)), len(expected_paths))
        for path in paths:
            self.assertTrue(path in expected_paths)

        # TEST 2
        paths = parser.getCategoryPaths('D009144')
        expected_paths = Set([
            'Technology, Industry, Agriculture/Non-Medical Public and Private Facilities/Information Centers/Archives/Museums',
            'Technology, Industry, Agriculture/Non-Medical Public and Private Facilities/Museums',
            'Information Science/Information Science/Information Centers/Archives/Museums',
            'Humanities/Humanities/History/Archives/Museums'
        ])

        self.assertEqual(len(Set(paths)), len(expected_paths))
        for path in paths:
            self.assertTrue(path in expected_paths)



if __name__ == '__main__':
    unittest.main()
