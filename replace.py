import re
import os

template_pattern = re.compile(
    '(?ms)^#\s*REDIRECT_TEMPLATE_START(.*)^#\s*REDIRECT_TEMPLATE_END')
with open("netlify.toml", "r+") as config_file:
    # Read config file into string
    config = config_file.read()
    # Find template in config file
    template = next(template_pattern.finditer(config)).group(1).strip()

    # Remove template from config
    config = template_pattern.sub('', config)
    # For each matching environment variable, append a redirect entry to the config file
    for name, value in os.environ.items():
        if name.startswith('REDIRECT_SOURCE_'):
            redirect = template
            redirect_name = name.replace('_SOURCE_', '_')
            target_env_name = name.replace('_SOURCE_', '_TARGET_')
            redirect = redirect.replace('REDIRECT_TEMPLATE_FROM', value)
            redirect = redirect.replace(
                'REDIRECT_TEMPLATE_TO', os.getenv(target_env_name))
            config = '{}\n# {}\n{}\n'.format(config, redirect_name, redirect)

    print(config)
    config_file.seek(0)
    config_file.write(config)
    config_file.truncate()
