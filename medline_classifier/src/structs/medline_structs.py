

class MedlineArticle:

    def __init__(self, pmid, title, abstract, mesh_headings):
        if pmid is None or pmid == '':
            raise ValueError('PMID missing!')
        if title is None or title == '':
            raise ValueError('Title missing!')
        if abstract is None or abstract == '':
            raise ValueError('Abstract missing!')
        if mesh_headings is None or len(mesh_headings) == 0:
            raise ValueError('Topic IDs missing!')

        self.pmid = pmid
        self.title = title
        self.abstract = abstract
        self.mesh_headings = mesh_headings

    def getUrl(self):
        return 'https://www.ncbi.nlm.nih.gov/pubmed/' + self.pmid
