import json
from structs.structs import MedlineArticle


class MedlineFileParser:

    def __init__(self, fname):
        self._fname = fname
        self._articles = []

    def parse(self):
        with open(self._fname) as f:
            parsed = json.load(f)
            article_set = parsed['PubmedArticleSet']
            articles = article_set['PubmedArticle']
            for citation in articles:
                article = citation['Article']

                article_id = citation['PMID']
                title = article['ArticleTitle']['$']
                abstract = self.extractAbstract(article)

                mesh_headings = citation['MeshHeadingList']
                category_ids = [heading['DescriptorName']['@UI'] for heading in mesh_headings]

                medline_article = MedlineArticle(
                    article_id,
                    title,
                    abstract,
                    category_ids
                )
                self._articles.append(medline_article)

    def extractAbstract(self, article):
        pass

    def articles(self):
        return self._articles
