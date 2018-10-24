import os
from lxml import etree
from util.arguments import settings
from sets import Set

def processFile(fin, fout, target_years):
        tree = etree.parse(fin)
        articles = tree.findall('PubmedArticle')

        writtenN = 0
        article_years = Set()

        # start the file
        fout.write(u'<?xml version="1.0" encoding="utf-8"?>')
        fout.write(u'\n<!DOCTYPE PubmedArticleSet SYSTEM "http://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_170101.dtd">')
        fout.write(u'\n<PubmedArticleSet>')

        for article_el in articles:
            # find the year
            year_el = article_el.find('MedlineCitation/DateCreated/Year')
            if year_el is None:
                year_el = article_el.find('MedlineCitation/DateCompleted/Year')
                if year_el is None:
                    year_el = article_el.find('MedlineCitation/DateRevised/Year')
                    if year_el is None:
                        continue

            year_str = year_el.text
            year = int(year_str)

            article_years.add(year)

            if year in target_years:
                article_str = etree.tostring(article_el, pretty_print=True)
                fout.write(unicode(article_str, 'utf-8'))
                writtenN += 1

        # end the file
        fout.write(u'\n</PubmedArticleSet>')
        print 'File finished, written ' + str(writtenN) + ' articles! Articles years: ' + str(article_years)


if __name__ == "__main__":
    medline_path = settings['medline_path']
    out_dir = settings['out']
    target_years = Set([int(year) for year in settings['years'].split(',')])

    if out_dir is None:
        raise ValueError('out_dir missing!')
    if target_years is None or len(target_years) == 0:
        raise ValueError('invalid target years missing!')

    print 'target years: ' + str(target_years)

    medline_dirs = os.listdir(medline_path)
    for dirN, dirname in enumerate(medline_dirs):
        print 'processing directory ' + str(dirN+1) + ' out of ' + str(len(medline_dirs)) + ': `' + dirname + '`'
        # go through all the files in this directory
        medline_files = os.listdir(os.path.join(medline_path, dirname))
        for fileN, medline_fname in enumerate(medline_files):
            dirname_out = os.path.join(out_dir, dirname)
            if not os.path.exists(dirname_out):
                os.makedirs(dirname_out)

            fname_in = os.path.join(medline_path, dirname, medline_fname)
            fname_out = os.path.join(dirname_out, medline_fname)
            print 'processing file ' + str(fileN+1) + ' out of ' + str(len(medline_files)) + ': `' + fname_in + '`'

            with open(fname_in, 'r') as fin:
                with open(fname_out, 'w') as fout:
                    processFile(fin, fout, target_years)
    # done! now save the dmoz files
    print 'finished processing files!'
