def get_package_name(tree, repo_structure):
    if getattr(tree, 'package', None) is not None and getattr(tree.package, 'name', None):
        repo_structure['package'] = tree.package.name
    else:
        repo_structure['package'] = ''