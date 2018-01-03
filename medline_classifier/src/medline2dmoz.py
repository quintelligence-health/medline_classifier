import sys
import traceback
import os
import pickle

from sets import Set
from lxml import etree

from util.arguments import settings
from parsers.medline_xml import MedlineFileParser
from parsers.mesh_xml import MeshTree
from structs.dmoz_structs import DMozPage, DMozOntology


mesh = None
dmoz = None

topicid_map = {}
invalid_descriptor_uis = Set()


def toDmozPath(path):
    return 'Top/' + path


def processArticle(article):
    global dmoz
    global invalid_descriptor_uis

    for descriptor_ui in article.mesh_headings:
        url = article.getUrl()
        title = article.title
        description = article.getSingleAbstract()

        topic_paths = mesh.getCategoryPaths(descriptor_ui)
        if topic_paths is None:
            if descriptor_ui not in invalid_descriptor_uis:
                print 'no paths for DescriptorUI `' + descriptor_ui + '`'
            invalid_descriptor_uis.add(descriptor_ui)
            continue

        for pathN, topic_path in enumerate(topic_paths):
            topic_name = topic_path
            topic_id = topicid_map[topic_name]

            dmoz_topic_name = toDmozPath(topic_name)
            dmoz_page = DMozPage(url, title, description, topic_id, dmoz_topic_name)
            dmoz.addPage(dmoz_page)

def processArticleBatch(articles):
    for article in articles:
        processArticle(article)


if __name__ == '__main__':
    medline_path = settings['medline_path']
    mesh_path = settings['mesh_path']
    output_path = settings['output_path']
    serialize_path = lambda fname: os.path.join(settings['serialize_path'], fname)

    load_dmoz = True
    process_files = False

    write_structure_file = False
    write_content_file = True

    def serialize(object, fname):
        with open(serialize_path(fname), 'w') as f:
            pickle.dump(object, f)

    def deserialize(fname):
        with open(serialize_path(fname), 'r') as f:
            return pickle.load(f)

    # 1) load the MESH structure
    mesh = MeshTree()
    mesh.parse(mesh_path)

    # 2) create an empty DMoz ontology
    dmoz = DMozOntology(settings['cache_path'])

    if load_dmoz and os.path.isfile(serialize_path('topicid_map.pkl')):
        print 'loading topics'
        topicid_map = deserialize('topicid_map.pkl')
        dmoz = deserialize('dmoz.pkl')
        print 'loaded'
    else:
        print 'defining topics'
        path_cmp = lambda p1, p2: len(p1.split('/')) - len(p2.split('/'))
        print 'fetching all categories'
        all_categories = mesh.getAllCategories()
        print 'creating all paths'

        path_set = Set()
        for nodeN, node in enumerate(all_categories):
            if nodeN % 1000 == 0:
                print 'processing node ' + str(nodeN+1) + ' of ' + str(len(all_categories))

            node_paths = node.getCategoryPathsStr()
            for path in node_paths:
                path_set.add(path)

        all_paths = [path for path in path_set]
        all_paths.sort(cmp=path_cmp)
        curr_id = 3
        for pathN, node_path in enumerate(all_paths):
            if pathN % 1000 == 0:
                print 'processing path ' + str(pathN+1) + ' of ' + str(len(all_paths))
            topic_name = None
            try:
                topic_name = node_path
                topic_id = curr_id
                if topic_name not in topicid_map:
                    topicid_map[topic_name] = topic_id
                    dmoz.defineTopic(topic_id, toDmozPath(topic_name), 'NA')
                    curr_id += 1
            except:
                print 'exception while defining topic `' + topic_name + '`!'
                traceback.print_exc(file=sys.stdout)
                exit(1)
        print 'saving topics'
        serialize(topicid_map, 'topicid_map.pkl')
        serialize(dmoz, 'dmoz.pkl')
        print 'topics defined'

    if process_files:
        print 'clearing cache'
        dmoz.clearCacheDir()

        print 'processing all files'
        # 3) go through all the medline files and parse them one by one
        #    adding the results to the dmoz ontology
        medline_dirs = os.listdir(medline_path)
        for dirN, dirname in enumerate(medline_dirs):
            print 'processing directory ' + str(dirN+1) + ' out of ' + str(len(medline_dirs)) + ': `' + dirname + '`'
            # go through all the files in this directory
            medline_files = os.listdir(os.path.join(medline_path, dirname))
            for fileN, medline_fname in enumerate(medline_files):
                fname = os.path.join(medline_path, dirname, medline_fname)
                print 'processing file ' + str(fileN+1) + ' out of ' + str(len(medline_files)) + ': `' + fname + '`'
                parser = MedlineFileParser()
                parser.parse(fname)
                articles = parser.getArticles()
                processArticleBatch(articles)
        # done! now save the dmoz files
        print 'finished processing files!'
        print 'invalid DescriptorUIs: ' + str(invalid_descriptor_uis)

    print 'storing content and structure files'
    dmoz_content_fname = os.path.join(output_path, 'content.rdf.u8')

    if write_structure_file:
        dmoz_struct_fname = os.path.join(output_path, 'structure.rdf.u8')
        print 'writing structure file'
        with open(dmoz_struct_fname, 'w') as f:
            dmoz.writeStructureXml(f)
    if write_content_file:
        print 'writing content file'
        with open(dmoz_content_fname, 'w') as f:
            dmoz.writeContentXml(f)
    # finished
    print 'done!'
