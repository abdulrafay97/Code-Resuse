import json
import os
import rdflib
import urllib.parse
from rdflib import URIRef, Literal
from rdflib.namespace import RDF
from rdflib.namespace import Namespace
from decimal import Decimal


def read_json(file_path):
    with open(file_path, 'r') as file:
        meta_data = json.load(file)

    return meta_data


base = Namespace("http://codereuse.org/")


repo = Namespace(f"{base}repository/")
person = Namespace(f"{base}person/")
issue = Namespace(f"{base}issue/")
pull_request = Namespace(f"{base}pull_request/")
topic = Namespace(f"{base}topic/")
language_ = Namespace(f"{base}language/")
entity = Namespace(f"{base}entity/")
status = Namespace(f"{base}status/")
issue_label = Namespace(f"{base}issue_label/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")


TYPE_MAP = {
    'repo': repo,
    'person': person,
    'issue': issue,
    'pull_request': pull_request,
    'topic': topic,
    'language': language_,
    'entity': entity,
    'status': status,
    'issue_label':issue_label
}


def make_uri(type_, name):
    namespace = TYPE_MAP.get(type_)
    if namespace: 
        return namespace[name]
    else: 
        return URIRef(name)


def make_predicate(name):
    return base[name]


def parse_string(string_to_encode):
    encoded_string = urllib.parse.quote(string_to_encode)
    custom_encoded_string = encoded_string.replace('%', '-')

    return custom_encoded_string


def combine_string(string1, string2):
    return string1 + "/" + string2


def make_profile_url(username):
    return "https://github.com/" + username


def make_issue_url(repo_author, repo_name, issue_no):
    return "https://github.com/" + repo_author + "/" + repo_name + "/issues/" + issue_no 


def make_repo_url(username, reponame):
    return "https://github.com/" + username + "/" + reponame


def count_issue_ratio(data):
    closed = 0
    open = 0
    for issue in data:
        if issue['issue_status'] == 'closed':
            closed+=1
        elif issue['issue_status'] == 'open':
            open+=1

    return open, closed


def count_forks_ratio(data):
    Inactive = 0
    active = 0
    for fork in data:
        if fork['repo_status'] == 'Inactive':
            Inactive+=1
        elif fork['repo_status'] == 'active':
            active+=1

    return active, Inactive


def add_issue_labels(issue, temp_string, graph):
    if issue['labels']:
        for label in issue['labels']:
            graph.add((make_uri('repo', temp_string), make_predicate('hasLabel'), make_uri('issue_label', parse_string(label))))


def make_author_rdf(graph, data):
    graph.add((make_uri('person', data['author']), DCTERMS.type, make_uri('entity', 'author')))
    graph.add((make_uri('person', data['author']), FOAF.accountName, Literal(data['author'])))
    graph.add((make_uri('person', data['author']), FOAF.hasUrl, URIRef(make_profile_url(data['author']))))


def make_repo_rdf(data, graph):
    graph.add((make_uri('repo', data['repositoryName']), DCTERMS.type, make_uri('entity', 'repository')))
    graph.add((make_uri('repo', data['repositoryName']), FOAF.hasUrl, URIRef(data['url'])))
    graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasAuthor'), make_uri('person', data['author'])))
    make_author_rdf(graph, data)

    if data['about']:
        graph.add((make_uri('repo', data['repositoryName']), DCTERMS.description, Literal(data['about'])))

    if data['stars']:
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasStarCount'), Literal(len(data['stars']))))

    if data['watchers']:
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasWatcherCount'), Literal(len(data['watchers']))))

    if data['forks']:
        active, inactive = count_forks_ratio(data['forks'])
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasActiveForkCount'), Literal(active)))
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasInActiveForkCount'), Literal(inactive)))

        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasTotalForkCount'), Literal(len(data['forks']))))

    if data['contributors']:
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasContributorCount'), Literal(len(data['contributors']))))

    if data['issues']:
        open, closed = count_issue_ratio(data['issues'])
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasOpenIssueCount'), Literal(open)))
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasClosedIssueCount'), Literal(closed)))
        
        graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasTotalIssueCount'), Literal(len(data['issues']))))


def make_topic_rdf(data, graph):
    if data['topics']:
        for topicname in data['topics']:
            graph.add((make_uri('repo', data['repositoryName']), DCTERMS.subject, make_uri('topic', parse_string(topicname))))


def make_language_rdf(data, graph):
    if data['languages']:
        count = 1
        for prog_language in data['languages']:
            temp_string = combine_string(data['repositoryName'], "languageInfo")
            temp_string = combine_string(temp_string, str(count))

            graph.add((make_uri('repo', data['repositoryName']), DCTERMS.language, make_uri('repo', temp_string)))
            graph.add((make_uri('repo', temp_string), make_predicate('hasLanguageUsage'), Literal(Decimal(data['languages'][prog_language].strip('%')))))
            graph.add((make_uri('repo', temp_string), make_predicate('hasLanguageName'), make_uri('language', parse_string(prog_language))))
            
            count+=1


def make_star_rdf(data, graph):
    if data['stars']:
        for stargazer in data['stars']:
            graph.add((make_uri('person', stargazer['user_name']), DCTERMS.type, make_uri('entity', 'stargazer')))
            graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasStargazer'), make_uri('person', stargazer['user_name'])))
            graph.add((make_uri('person', stargazer['user_name']), FOAF.about, Literal(stargazer['user_about'])))
            graph.add((make_uri('person', stargazer['user_name']), FOAF.accountName, Literal(stargazer['user_name'])))
            graph.add((make_uri('person', stargazer['user_name']), FOAF.hasUrl, URIRef(make_profile_url(stargazer['user_name']))))


def make_watcher_rdf(data, graph):
    if data['watchers']:
        for watcher in data['watchers']:
            graph.add((make_uri('person', watcher['user_name']), DCTERMS.type, make_uri('entity', 'watcher')))
            graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasWatcher'), make_uri('person', watcher['user_name'])))
            graph.add((make_uri('person', watcher['user_name']), FOAF.about, Literal(watcher['user_about'])))
            graph.add((make_uri('person', watcher['user_name']), FOAF.accountName, Literal(watcher['user_name'])))
            graph.add((make_uri('person', watcher['user_name']), FOAF.hasUrl, URIRef(make_profile_url(watcher['user_name']))))


def make_forked_rdf(data, graph):
    if data['forks']:
        for forker in data['forks']:
            graph.add((make_uri('person', forker['user_name']), DCTERMS.type, make_uri('entity', 'forker')))
            graph.add((make_uri('person', forker['user_name']), FOAF.accountName, Literal(forker['user_name'])))
            graph.add((make_uri('person', forker['user_name']), FOAF.hasUrl, URIRef(make_profile_url(forker['user_name']))))
            
            temp_string = combine_string(data['repositoryName'], "forkedBy")
            temp_string = combine_string(temp_string, forker['user_name'])

            graph.add((make_uri('repo', data['repositoryName']), make_predicate('repoForkedAs'), make_uri('repo', temp_string)))
            graph.add((make_uri('repo', temp_string), make_predicate('forkedBy'), make_uri('person', forker['user_name'])))
            graph.add((make_uri('repo', temp_string), make_predicate('hasForkedRepoStatus'), make_uri('status', forker['repo_status'])))
            graph.add((make_uri('repo', temp_string), FOAF.hasUrl, URIRef(make_repo_url(forker['user_name'], forker['repo_forked_as']))))
            graph.add((make_uri('repo', temp_string), DCTERMS.type, make_uri('entity', 'forkedRepository')))


def make_contributes_rdf(data, graph):
    if data['contributors']:
        count = 1
        for contributor in data['contributors']:
            temp_string = combine_string(data['repositoryName'], "ContributorInfo")
            temp_string = combine_string(temp_string, str(count))

            graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasContributer'), make_uri('repo', temp_string)))

            graph.add((make_uri('repo', temp_string), make_predicate('contributedBy'), make_uri('person', contributor['user_name'])))

            graph.add((make_uri('person', contributor['user_name']), DCTERMS.type, make_uri('entity', 'contributor')))
            graph.add((make_uri('repo', temp_string), make_predicate('hasContributedCommits'), Literal(contributor['no_of_commits'])))
            graph.add((make_uri('person', contributor['user_name']), FOAF.accountName, Literal(contributor['user_name'])))
            graph.add((make_uri('person', contributor['user_name']), FOAF.hasUrl, URIRef(make_profile_url(contributor['user_name']))))
            
            count+=1
            


def make_issues_rdf(data, graph):
    if data['issues']:
        for issue in data['issues']:
            temp_string = combine_string('issue', issue['issue_id'])
            temp_string = combine_string(data['repositoryName'], temp_string)

            graph.add((make_uri('repo', data['repositoryName']), make_predicate('hasIssue'), make_uri('repo', temp_string)))
            
            graph.add((make_uri('repo', temp_string), DCTERMS.title, Literal(issue['issue_title'])))
            graph.add((make_uri('repo', temp_string), make_predicate('hasIssueStatus'), make_uri('status', issue['issue_status'])))
            graph.add((make_uri('repo', temp_string), make_predicate('issueCreatedBy'), make_uri('person', issue['issue_author'])))
            graph.add((make_uri('repo', temp_string), FOAF.hasUrl, URIRef(make_issue_url(data['author'], data['repositoryName'], issue['issue_id']))))
            
            graph.add((make_uri('person', issue['issue_author']), DCTERMS.type, make_uri('entity', 'issueAuthor')))
            graph.add((make_uri('person', issue['issue_author']), FOAF.accountName, Literal(issue['issue_author'])))
            graph.add((make_uri('person', issue['issue_author']), FOAF.hasUrl, URIRef(make_profile_url(issue['issue_author']))))

            add_issue_labels(issue, temp_string, graph)



def process_json_file(json_path, rdf_graph):
    json_data = read_json(json_path)
    
    make_repo_rdf(json_data, rdf_graph)
    make_topic_rdf(json_data, rdf_graph)
    make_language_rdf(json_data, rdf_graph)
    make_star_rdf(json_data, rdf_graph)
    make_watcher_rdf(json_data, rdf_graph)
    make_forked_rdf(json_data, rdf_graph)
    make_contributes_rdf(json_data, rdf_graph)
    make_issues_rdf(json_data, rdf_graph)


JAVA_METADATA_PATH = '/Users/abdulrafay/Desktop/GitHub-KG/github_crawl_data/CodeSearchNet/Java/metadata'
PYTHON_METADATA_PATH = '/Users/abdulrafay/Desktop/GitHub-KG/github_crawl_data/CodeSearchNet/Python/metadata'


java_files = [file for file in os.listdir(JAVA_METADATA_PATH) if file.endswith('.json')]
python_files = [file for file in os.listdir(PYTHON_METADATA_PATH) if file.endswith('.json')]

all_files = java_files + python_files
print(f"Total Repositories: {len(all_files)}")

graph = rdflib.Graph()

for file in all_files:
    if file in java_files:
        json_path = os.path.join(JAVA_METADATA_PATH, file)
    elif file in python_files:
        json_path = os.path.join(PYTHON_METADATA_PATH, file)
    else:
        print("Skiiping File")

    process_json_file(json_path, graph)


graph.serialize(destination="Knowledge_graph.nt", format="nt", encoding='UTF-8')