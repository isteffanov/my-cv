from jinja2 import Environment, FileSystemLoader
import yaml

# loading the environment
env = Environment(loader = FileSystemLoader('templates'))

# loading the template
template = env.get_template('cv.tex.jinja')

opa = yaml.load(open('my_data.yaml'), Loader=yaml.SafeLoader)
# print(opa)
# for key, section in opa['sections'].items():
#     print(key, section)
#     for k, entry in section.items():
#         print(k, entry)
#         break
#     break

output = template.render(opa)

# printing the output on screen
print(output)
