def get_package_name(tree, repo_structure):
    if tree.package.name:
        repo_structure['package'] = tree.package.name
    else:
        repo_structure['package'] = ''