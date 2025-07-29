def get_plugin_id(domain, name):
    parts = domain.split('.')
    reversed_parts = parts[::-1]
    name_list = name.split()
    pascal_name = name_list[0].lower() + ''.join(word.capitalize() for word in name_list[1:])
    reversed_parts.append(pascal_name)
    return '.'.join(reversed_parts)